"""Launch the run matrix on a rented Modal GPU, once, with provenance recorded.

The harness itself is provider-agnostic; this file is the one place that knows
about Modal. It builds a container image holding the `slm` package and the four
input CSVs plus one prior matrix summary, runs the matrix on an L4 GPU, and
keeps the results on a persistent volume.

Three properties matter more here than convenience:

- **Run once.** The container is single-use, retries are off, and the function
  refuses to start if a launcher manifest already exists in the results
  directory. An accidental retry would spend real money and produce a second run
  claiming the same identity.
- **Provenance.** The image has no `.git` directory, so the local entrypoint
  reads the commit, branch, and working-tree status and passes them in through
  the environment. Every file shipped is also hashed into a single
  `source_tree_sha256`, so the results state exactly which source produced them.
- **Honest cost accounting.** The hourly rate is the actual all-in rate, and
  hours already billed by earlier sessions are passed forward so the runner's
  deadline accounts for them rather than restarting the clock.

`resume_gpu_matrix` continues an existing run directory after an interruption.
It returns early when the earlier run already completed every planned run, so a
resume cannot become an accidental second full run.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from pathlib import Path, PurePosixPath

import modal


APP_NAME = "ivc-slm-exact-exposure"
RESULTS_VOLUME_NAME = "ivc-slm-results"
REMOTE_REPO = PurePosixPath("/root/ivc")
REMOTE_SLM = REMOTE_REPO / "slm"
REMOTE_RESULTS = PurePosixPath("/results/ivc_transfer_exact_exposure_20260712")
# The provider's actual all-in rate, and the hours already billed by earlier
# sessions. Both feed the runner's deadline, so it stops at the real spending
# ceiling rather than at a fresh clock.
ALL_IN_HOURLY_RATE_USD = 0.957456
PRIOR_BILLED_HOURS = 2.693888284034199

LOCAL_REPO = Path(__file__).resolve().parents[1]
# The exact inputs shipped into the image: the four source corpora, plus the
# earlier matrix summary that transfer-only scope reads its IVC baselines from.
DATA_FILES = (
    Path("research/data/open_prototype/lipi/metadata_filtered.csv"),
    Path("research/data/open_prototype/reports/linear_b_series_d_row_inventory.csv"),
    Path("research/data/open_prototype/known_scripts/sumtablets/sumtablets_line_sequences.csv"),
    Path("research/data/open_prototype/nonlinguistic/sproat2014/sproat2014_extracted_sequences.csv"),
    Path("research/data/slm/ivc_from_scratch_scaling_20260712/matrix_summary.json"),
)


def _build_image() -> modal.Image:
    """Build the container image with pinned packages and the inputs copied in.

    Versions are pinned exactly so a rerun months later executes the same code
    path. Files are copied rather than mounted so the image itself is the
    complete, hashable record of what ran.
    """
    image = modal.Image.debian_slim(python_version="3.11").uv_pip_install(
        "torch==2.7.1",
        "numpy==2.2.6",
        "pillow==11.3.0",
        "setuptools==80.9.0",
        "wheel==0.45.1",
    )
    image = image.add_local_dir(LOCAL_REPO / "slm", str(REMOTE_SLM), copy=True)
    for relative_path in DATA_FILES:
        image = image.add_local_file(
            LOCAL_REPO / relative_path,
            str(REMOTE_REPO / relative_path),
            copy=True,
        )
    return image


image = _build_image()
results_volume = modal.Volume.from_name(RESULTS_VOLUME_NAME, create_if_missing=True)
app = modal.App(APP_NAME)


def _tree_manifest() -> dict:
    """Hash every shipped source and data file, and fold them into one digest.

    Build artifacts are excluded — caches, packaging metadata, and earlier run
    outputs — so the digest depends only on inputs and source. Paths are hashed
    alongside contents, so moving a file changes the digest too.
    """
    remote_repo = Path(REMOTE_REPO)
    remote_slm = Path(REMOTE_SLM)
    paths = [
        path
        for path in remote_slm.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and not any(part.endswith(".egg-info") for part in path.parts)
        and "runs" not in path.parts
    ]
    paths.extend(remote_repo / path for path in DATA_FILES)
    rows = []
    aggregate = hashlib.sha256()
    for path in sorted(paths):
        relative_path = path.relative_to(remote_repo).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append({"path": relative_path, "sha256": digest, "bytes": path.stat().st_size})
        aggregate.update(relative_path.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return {"source_tree_sha256": aggregate.hexdigest(), "files": rows}


@app.function(
    image=image,
    gpu="L4",
    cpu=(2.0, 2.0),
    memory=(8192, 8192),
    timeout=22_500,
    retries=0,
    max_containers=1,
    single_use_containers=True,
    volumes={str(REMOTE_RESULTS.parent): results_volume},
)
def run_gpu_matrix(
    source_commit: str, source_branch: str, source_status: str, prior_billed_hours: float
) -> dict:
    """Run the matrix once on a GPU and return where the results landed.

    The launcher manifest doubles as a claim marker: writing it says this GPU run
    has started, and finding it already there means something is trying to run
    twice, which raises rather than spends more money.

    The volume is committed before the work, in a `finally` after it, and again
    at the end, so a crashed container still leaves its partial results behind.
    Exactly one new run directory must appear; anything else means the runner did
    not behave as expected and is treated as an error.
    """
    remote_results = Path(REMOTE_RESULTS)
    remote_slm = Path(REMOTE_SLM)
    remote_results.mkdir(parents=True, exist_ok=True)
    launcher_manifest_path = remote_results / "launcher_manifest.json"
    if launcher_manifest_path.exists():
        raise RuntimeError(
            "One-shot matrix claim already exists; refusing a retry, restart, or duplicate GPU run."
        )
    manifest = _tree_manifest()
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONUNBUFFERED": "1",
            "IVCSLM_OUTPUT_DIR": str(remote_results),
            "IVCSLM_HOURLY_RATE_USD": f"{ALL_IN_HOURLY_RATE_USD:.6f}",
            "IVCSLM_BILLED_START_UNIX": str(time.time()),
            "IVCSLM_PRIOR_BILLED_HOURS": str(prior_billed_hours),
            "IVCSLM_CONFIG": "configs/ivc_transfer_exact_exposure_20260712.json",
            "IVCSLM_RUN_SCOPE": "transfer-only",
            "IVCSLM_SOURCE_COMMIT": source_commit,
            "IVCSLM_SOURCE_BRANCH": source_branch,
            "IVCSLM_SOURCE_STATUS_PORCELAIN": source_status,
            "IVCSLM_SOURCE_TREE_SHA256": manifest["source_tree_sha256"],
        }
    )
    launcher_manifest = {
        "app": APP_NAME,
        "volume": RESULTS_VOLUME_NAME,
        "gpu": "L4",
        "cpu_cores": 2.0,
        "memory_mib": 8192,
        "function_timeout_seconds": 22_500,
        "runner_hard_runtime_hours": 6.0,
        "all_in_hourly_rate_usd": ALL_IN_HOURLY_RATE_USD,
        "prior_billed_hours": prior_billed_hours,
        "run_scope": "transfer-only",
        "source_commit": source_commit,
        "source_branch": source_branch,
        "source_status_porcelain": source_status,
        **manifest,
    }
    launcher_manifest_path.write_text(
        json.dumps(launcher_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    results_volume.commit()
    before = {path.name for path in remote_results.iterdir() if path.is_dir()}
    try:
        subprocess.run(
            ["bash", "run_gpu_matrix.sh"],
            cwd=remote_slm,
            env=environment,
            check=True,
        )
    finally:
        results_volume.commit()
    after = [path for path in remote_results.iterdir() if path.is_dir() and path.name not in before]
    if len(after) != 1:
        raise RuntimeError(f"Expected one new immutable run directory, found {[path.name for path in after]}")
    run_root = after[0]
    completion_path = run_root / "completion.json"
    if not completion_path.is_file():
        raise RuntimeError(f"Matrix returned without completion metadata: {completion_path}")
    completion = json.loads(completion_path.read_text(encoding="utf-8"))
    results_volume.commit()
    return {
        "run_root": str(run_root),
        "source_tree_sha256": manifest["source_tree_sha256"],
        "completion": completion,
    }


@app.function(
    image=image,
    gpu="L4",
    cpu=(2.0, 2.0),
    memory=(8192, 8192),
    timeout=7_200,
    retries=0,
    max_containers=1,
    single_use_containers=True,
    volumes={str(REMOTE_RESULTS.parent): results_volume},
)
def resume_gpu_matrix(
    run_name: str,
    prior_billed_hours: float,
    source_commit: str,
    source_branch: str,
    source_status: str,
) -> dict:
    """Continue an interrupted run in an existing directory, without restarting it.

    `IVCSLM_RESUME_RUN_ROOT` tells the runner to reuse that directory; the runner
    then verifies the stored config matches the current one and skips the cells
    it already completed. If the earlier run already finished every planned run,
    this returns immediately rather than allocating a GPU.

    The run name must be a bare directory name, so a caller cannot point the
    resume at an arbitrary path on the volume.
    """
    if not run_name or "/" in run_name or "\\" in run_name:
        raise ValueError("Resume run name must be one existing run-directory name.")
    run_root = Path(REMOTE_RESULTS) / run_name
    if not run_root.is_dir():
        raise FileNotFoundError(f"Resume run does not exist: {run_root}")
    completion_path = run_root / "completion.json"
    if completion_path.exists():
        completion = json.loads(completion_path.read_text(encoding="utf-8"))
        if completion.get("completed_runs") == completion.get("planned_runs"):
            return {"run_root": str(run_root), "completion": completion, "already_complete": True}

    manifest = _tree_manifest()
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONUNBUFFERED": "1",
            "IVCSLM_OUTPUT_DIR": str(REMOTE_RESULTS),
            "IVCSLM_HOURLY_RATE_USD": f"{ALL_IN_HOURLY_RATE_USD:.6f}",
            "IVCSLM_BILLED_START_UNIX": str(time.time()),
            "IVCSLM_RESUME_RUN_ROOT": str(run_root),
            "IVCSLM_PRIOR_BILLED_HOURS": str(prior_billed_hours),
            "IVCSLM_CONFIG": "configs/ivc_transfer_exact_exposure_20260712.json",
            "IVCSLM_RUN_SCOPE": "transfer-only",
            "IVCSLM_SOURCE_COMMIT": source_commit,
            "IVCSLM_SOURCE_BRANCH": source_branch,
            "IVCSLM_SOURCE_STATUS_PORCELAIN": source_status,
            "IVCSLM_RESUME_SOURCE_TREE_SHA256": manifest["source_tree_sha256"],
            "IVCSLM_RESUME_SOURCE_STATUS_PORCELAIN": source_status,
        }
    )
    try:
        subprocess.run(
            ["bash", "run_gpu_matrix.sh"],
            cwd=Path(REMOTE_SLM),
            env=environment,
            check=True,
        )
    finally:
        results_volume.commit()
    if not completion_path.is_file():
        raise RuntimeError(f"Resume returned without completion metadata: {completion_path}")
    completion = json.loads(completion_path.read_text(encoding="utf-8"))
    return {
        "run_root": str(run_root),
        "source_tree_sha256": manifest["source_tree_sha256"],
        "completion": completion,
        "already_complete": False,
    }


def _git(*arguments: str) -> str:
    """Read Git provenance locally, since the container image carries no repository."""
    return subprocess.check_output(
        ["git", *arguments], cwd=LOCAL_REPO, text=True, stderr=subprocess.DEVNULL
    ).strip()


@app.local_entrypoint()
def main(resume_run_name: str = "", prior_billed_hours: float = PRIOR_BILLED_HOURS) -> None:
    """Start a fresh GPU run, or resume one by name, and print what came back.

    The working-tree status is captured for the shipped paths only, so the
    manifest records whether the code and data that actually ran were clean.
    """
    source_commit = _git("rev-parse", "HEAD")
    source_branch = _git("branch", "--show-current")
    source_status = _git(
        "status",
        "--porcelain",
        "--",
        "slm",
        *(str(path) for path in DATA_FILES),
    )
    result = (
        resume_gpu_matrix.remote(
            resume_run_name,
            prior_billed_hours,
            source_commit,
            source_branch,
            source_status,
        )
        if resume_run_name
        else run_gpu_matrix.remote(source_commit, source_branch, source_status, prior_billed_hours)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
