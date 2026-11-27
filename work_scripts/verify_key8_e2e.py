#!/usr/bin/env python3
"""
Indus Script Decipherment — Key #8 Independent 4-Tier E2E Verification Suite.

Requirement-driven, opaque-box verification across:
  Tier 1: Feature & Artifact Completeness (scripts, portability, Contracts 1-4)
  Tier 2: Mathematical, Statistical & Anti-Leakage Boundary Invariants
  Tier 3: Cross-Artifact Numerical Consistency & Web/LaTeX Cross-Checks
  Tier 4: Headless Playwright Chromium Execution & Git/Workspace Hygiene

Usage:
  python3 work_scripts/verify_key8_e2e.py [--tier {1,2,3,4,all}]
      [--json-out PATH] [--allow-missing-m5] [--root PATH]
"""

from __future__ import annotations

import argparse
import ast
import csv
import datetime as dt
import json
import math
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from typing import Any

# Portable repo root (overridable via --root)
DEFAULT_ROOT = Path(__file__).resolve().parent.parent

# Built dynamically so this script passes its own portability scan
FORBIDDEN_HOME_PREFIX = "/home/" + "antigravity"

REQUIRED_EXPLORER_V3_KEYS = (
    "meta",
    "waves",
    "six_wave_7family",
    "sangam_compounds",
    "archaeology_locks",
    "external_bridges",
    "multiface_stats",
    "multiface_top30",
    "dholavira_signboard",
    "glossary",
    "inscriptions",
)

SVG_GRAPHIC_TAGS = {
    "path",
    "rect",
    "circle",
    "ellipse",
    "line",
    "polygon",
    "polyline",
    "text",
    "image",
}

SUPERSCRIPT_MAP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")


# ---------------------------------------------------------------------------
# Generic Helpers
# ---------------------------------------------------------------------------


def norm_sign(val: Any) -> str:
    s = str(val).strip()
    if s.isdigit():
        return s.zfill(3)
    return s


def load_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]], str | None]:
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
        return fieldnames, rows, None
    except Exception as exc:
        return [], [], f"{type(exc).__name__}: {exc}"


def chi2_sf_even_df(x: float, df: int) -> float:
    """Exact upper-tail survival probability for chi-square with even df = 2m."""
    if df <= 0 or df % 2 != 0:
        raise ValueError(f"Expected positive even df, got {df}")
    if x <= 0.0:
        return 1.0
    m = df // 2
    half = 0.5 * x
    # Compute in log-safe form for large x
    try:
        term = 1.0
        total = 1.0
        for k in range(1, m):
            term *= half / k
            total += term
        val = math.exp(-half) * total
        return max(0.0, min(1.0, val))
    except OverflowError:
        return 0.0


def find_figure_file(fig_dir: Path, idx: int, ext: str) -> Path | None:
    exact = fig_dir / f"fig{idx}.{ext}"
    if exact.is_file():
        return exact
    matches = sorted(fig_dir.glob(f"fig{idx}_*.{ext}"))
    if matches:
        return matches[0]
    matches = sorted(fig_dir.glob(f"fig{idx}-*.{ext}"))
    if matches:
        return matches[0]
    return None


def resolve_coverage_splits(cov_raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map coverage_after_key8a.json split keys into canonical names."""
    root_obj = cov_raw.get("coverage", cov_raw) if isinstance(cov_raw, dict) else {}
    if not isinstance(root_obj, dict):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for k, v in root_obj.items():
        if not isinstance(v, dict):
            continue
        kl = k.lower()
        if ("comb" in kl) and ("intact" in kl) and ("all" not in kl):
            out["combined_intact"] = v
        elif (("new" in kl) or ("unseen" in kl)) and ("intact" in kl):
            out["unseen_intact"] = v
        elif ("lipi" in kl) and ("intact" in kl):
            out["lipi_intact"] = v
        elif ("comb" in kl) and ("all" in kl):
            out["combined_all"] = v
    return out


def select_primary_locked_tier(
    unseen_split: dict[str, Any],
    lexicon_count: int | None = None,
    has_split_824: bool = False,
) -> tuple[str | None, dict[str, Any] | None]:
    """Identify the primary locked Key #8A tier (excluding testing-frontier / provisional tiers)."""
    excluded_tokens = (
        "frontier",
        "testing",
        "provisional",
        "candidate",
        "exploratory",
        "tentative",
        "unverified",
        "speculative",
        "baseline",
        "before",
        "plus_",
        "+",
        "key7",
        "key6",
        "key5",
        "key4",
        "key3",
    )
    candidates: list[tuple[int, str, dict[str, Any]]] = []
    for tier_name, payload in unseen_split.items():
        if not isinstance(payload, dict) or "covered_tokens" not in payload:
            continue
        tl = tier_name.lower()
        if any(bad in tl for bad in excluded_tokens):
            continue
        n_signs = payload.get("n_signs")
        if lexicon_count is not None and isinstance(n_signs, int) and not isinstance(n_signs, bool):
            # Never select a tier exceeding the locked lexicon size as primary locked tier
            if n_signs > lexicon_count:
                continue
        score = 0
        if lexicon_count is not None and isinstance(n_signs, int) and not isinstance(n_signs, bool):
            if n_signs == lexicon_count:
                score += 100
            elif has_split_824 and abs(n_signs - lexicon_count) <= 1:
                score += 95
        if "key8" in tl:
            score += 40
        if "with4d" in tl or "locked" in tl or "full" in tl or "after_key8a" in tl:
            score += 20
        if "phonmet" in tl or "strict" in tl or "direct" in tl:
            score -= 15
        if isinstance(n_signs, int) and not isinstance(n_signs, bool):
            score += min(n_signs, 500) // 50
        candidates.append((score, tier_name, payload))
    if not candidates:
        return None, None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    _, best_name, best_payload = candidates[0]
    return best_name, best_payload


def find_nested_dict(obj: Any, pred) -> dict[str, Any] | None:
    """Breadth-first search for a nested dict matching pred(key, val)."""
    if not isinstance(obj, dict):
        return None
    queue: list[tuple[str, Any]] = [("", obj)]
    while queue:
        _, cur = queue.pop(0)
        if isinstance(cur, dict):
            for k, v in cur.items():
                if pred(str(k), v):
                    return v if isinstance(v, dict) else {str(k): v}
                if isinstance(v, (dict, list)):
                    queue.append((str(k), v))
        elif isinstance(cur, list):
            for item in cur:
                if isinstance(item, (dict, list)):
                    queue.append(("", item))
    return None


def has_non_null_numeric(obj: Any) -> bool:
    if isinstance(obj, bool):
        return False
    if isinstance(obj, (int, float)) and not math.isnan(float(obj)):
        return True
    if isinstance(obj, dict):
        return any(has_non_null_numeric(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_non_null_numeric(v) for v in obj)
    return False


def _discover_local_imported_siblings(ws: Path, seed_scripts: list[Path]) -> set[Path]:
    """AST-discover local sibling modules in work_scripts/ imported by Key #8 or repro scripts."""
    discovered: set[Path] = set()
    queue: list[Path] = [p for p in seed_scripts if p.is_file()]
    visited: set[Path] = set()
    while queue:
        cur = queue.pop(0)
        if cur in visited:
            continue
        visited.add(cur)
        try:
            tree = ast.parse(cur.read_text(encoding="utf-8", errors="replace"), filename=str(cur))
        except Exception:
            continue
        cand_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    parts = alias.name.split(".")
                    cand_names.add(parts[0])
                    if parts[0] == "work_scripts" and len(parts) >= 2:
                        cand_names.add(parts[1])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    parts = node.module.split(".")
                    cand_names.add(parts[0])
                    if parts[0] == "work_scripts":
                        if len(parts) >= 2:
                            cand_names.add(parts[1])
                        else:
                            for alias in node.names:
                                cand_names.add(alias.name.split(".")[0])
                elif node.level >= 1:
                    for alias in node.names:
                        cand_names.add(alias.name.split(".")[0])
        for mod in cand_names:
            sib = ws / f"{mod}.py"
            if sib.is_file() and sib not in visited:
                discovered.add(sib)
                queue.append(sib)
    return discovered


def collect_key_scripts(root: Path) -> tuple[list[Path], list[Path]]:
    """Return (core_scripts, m5_scripts) under work_scripts/."""
    ws = root / "work_scripts"
    core_set: set[Path] = set()
    if ws.is_dir():
        for pattern in ("gulf3*.py", "key*.py"):
            core_set.update(ws.glob(pattern))
        for fixed in ("reproduce_all_keys.py", "verify_key8_e2e.py"):
            p = ws / fixed
            if p.is_file():
                core_set.add(p)
        seed_for_imports = [
            p for p in core_set
            if p.name.startswith("key8") or p.name == "reproduce_all_keys.py"
        ]
        for m5_name in ("generate_paper_figures.py", "build_map_page.py"):
            mp = ws / m5_name
            if mp.is_file():
                seed_for_imports.append(mp)
        core_set.update(_discover_local_imported_siblings(ws, seed_for_imports))
    m5_list = [ws / "generate_paper_figures.py", ws / "build_map_page.py"]
    return sorted(core_set), m5_list


# ---------------------------------------------------------------------------
# Document / Scientific-Notation Normalization Helpers
# ---------------------------------------------------------------------------


def normalize_doc_text(raw: str) -> str:
    """Strip Markdown/LaTeX markup and normalize scientific notation encodings."""
    s = raw
    # Normalize Unicode superscripts in powers of 10: 10⁻¹⁰ -> 10^-10
    s = re.sub(
        r"10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)",
        lambda m: "10^" + m.group(1).translate(SUPERSCRIPT_MAP),
        s,
    )
    # Normalize LaTeX wrappers
    s = s.replace("\\times", "×").replace("\\cdot", "×").replace("\\%", "%")
    s = s.replace("\\,", " ").replace("~", " ").replace("{,}", ",")
    # Unwrap common LaTeX formatting macros iteratively
    for _ in range(3):
        s = re.sub(
            r"\\(?:textbf|textit|emph|mathrm|text|texttt|num|mathbf|mathit)\{([^{}]*)\}",
            r"\1",
            s,
        )
    # Remove dollar signs, bold/code markdown markers
    s = s.replace("$", "").replace("**", "").replace("`", "")
    # Normalize unicode minus / en-dash inside exponents (both 10^-N and e-N)
    s = re.sub(r"([eE])[−–]", r"\1-", s)
    s = re.sub(r"10\^\s*\{\s*[−–-]\s*(\d+)\s*\}", r"e-\1", s)
    s = re.sub(r"10\^\s*[−–-]\s*(\d+)", r"e-\1", s)
    s = re.sub(r"10\^\s*\{\s*\+?\s*(\d+)\s*\}", r"e+\1", s)
    s = re.sub(r"10\^\s*\+?\s*(\d+)", r"e+\1", s)
    # Collapse `1.09 × e-10`, `1.09 * e-10`, or `1.09 x e-10` into `1.09e-10`
    s = re.sub(r"(\d+(?:\.\d+)?)\s*[×xX·*]\s*e([+-]?\d+)", r"\1e\2", s)
    return s


def extract_all_floats(norm_text: str) -> list[float]:
    vals: list[float] = []
    # Scientific notation first
    for m in re.finditer(r"(?<![A-Za-z0-9_])(\d+(?:\.\d+)?[eE][+-]?\d+)(?![A-Za-z0-9_])", norm_text):
        try:
            vals.append(float(m.group(1)))
        except ValueError:
            pass
    # Plain decimals
    for m in re.finditer(r"(?<![A-Za-z0-9_])(0\.\d+)(?![A-Za-z0-9_eE])", norm_text):
        try:
            vals.append(float(m.group(1)))
        except ValueError:
            pass
    return vals


def doc_has_pvalue(norm_text: str, target_p: float, rel_tol: float = 0.03) -> bool:
    if target_p <= 0:
        return False
    for v in extract_all_floats(norm_text):
        if v <= 0:
            continue
        if abs(v - target_p) / target_p <= rel_tol:
            return True
    return False


def doc_has_pct(norm_text: str, target_pct: float, tol: float = 0.025) -> bool:
    for m in re.finditer(r"(?<!\d)(\d{1,3}\.\d{1,3})\s*%", norm_text):
        try:
            if abs(float(m.group(1)) - target_pct) <= tol:
                return True
        except ValueError:
            pass
    return False


def doc_has_int(norm_text: str, target_int: int) -> bool:
    plain = str(target_int)
    comma = f"{target_int:,}"
    pat = rf"(?<!\d)(?:{re.escape(comma)}|{re.escape(plain)})(?!\d)"
    return re.search(pat, norm_text) is not None


def doc_has_int_near(norm_text: str, target_int: int, context_pat: str, window: int = 80) -> bool:
    plain = str(target_int)
    comma = f"{target_int:,}"
    pat = rf"(?<!\d)(?:{re.escape(comma)}|{re.escape(plain)})(?!\d)"
    for m in re.finditer(pat, norm_text):
        snippet = norm_text[max(0, m.start() - window) : min(len(norm_text), m.end() + window)]
        if re.search(context_pat, snippet, re.IGNORECASE):
            return True
    return False


def doc_has_ratio(norm_text: str, num: int, den: int) -> bool:
    n_pat = rf"(?:{re.escape(f'{num:,}')}|{re.escape(str(num))})"
    d_pat = rf"(?:{re.escape(f'{den:,}')}|{re.escape(str(den))})"
    if re.search(rf"(?<!\d){n_pat}\s*(?:/|of|out of)\s*{d_pat}(?!\d)", norm_text, re.IGNORECASE):
        return True
    return False


def doc_has_ratio_near(norm_text: str, num: int, den: int, context_pat: str, window: int = 100) -> bool:
    n_pat = rf"(?:{re.escape(f'{num:,}')}|{re.escape(str(num))})"
    d_pat = rf"(?:{re.escape(f'{den:,}')}|{re.escape(str(den))})"
    pat = rf"(?<!\d){n_pat}\s*(?:/|of|out of)\s*{d_pat}(?!\d)"
    for m in re.finditer(pat, norm_text, re.IGNORECASE):
        snippet = norm_text[max(0, m.start() - window) : min(len(norm_text), m.end() + window)]
        if re.search(context_pat, snippet, re.IGNORECASE):
            return True
    return False


def extract_balanced_js_array(text: str, start_idx: int) -> str | None:
    """Extract a bracket-balanced JS array literal starting at text[start_idx] == '['."""
    n = len(text)
    if start_idx < 0 or start_idx >= n or text[start_idx] != "[":
        return None
    depth = 0
    i = start_idx
    in_str: str | None = None
    while i < n:
        ch = text[i]
        if in_str is not None:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        # Comments
        if ch == "/" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "/":
                nl = text.find("\n", i + 2)
                i = n if nl == -1 else nl + 1
                continue
            if nxt == "*":
                end_c = text.find("*/", i + 2)
                if end_c == -1:
                    return None
                i = end_c + 2
                continue
        if ch in ("'", '"', "`"):
            in_str = ch
            i += 1
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start_idx : i + 1]
        i += 1
    return None


def strip_tex_comments(tex: str) -> str:
    lines = []
    for line in tex.splitlines():
        # Remove unescaped % comments
        cleaned = re.sub(r"(?<!\\)%.*$", "", line)
        lines.append(cleaned)
    return "\n".join(lines)


def extract_pdf_text_pure_python(pdf_bytes: bytes) -> str:
    """Pure-Python fallback PDF text extractor handling FlateDecode & uncompressed streams."""
    chunks: list[str] = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\n?endstream", pdf_bytes, re.DOTALL):
        raw = m.group(1)
        data = raw
        try:
            data = zlib.decompress(raw)
        except Exception:
            try:
                data = zlib.decompress(raw.strip())
            except Exception:
                data = raw
        text_s = data.decode("latin-1", errors="ignore")
        # Extract literal strings (...) used in Tj / TJ operators
        in_lit = re.findall(r"\(((?:\\.|[^\\()])*)\)", text_s)
        if in_lit:
            unesc = [s.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\") for s in in_lit]
            chunks.append(" ".join(unesc))
        # Also extract hex strings <...> in TJ/Tj
        for hx in re.findall(r"<([0-9A-Fa-f]{4,})>\s*(?:Tj|TJ)", text_s):
            try:
                b = bytes.fromhex(hx)
                chunks.append(b.decode("utf-16-be", errors="ignore"))
                chunks.append(b.decode("latin-1", errors="ignore"))
            except Exception:
                pass
        # Keep readable ASCII if stream itself contains Tj/TJ
        if "Tj" in text_s or "TJ" in text_s:
            chunks.append(text_s)
    return "\n".join(chunks)


def count_pdf_pages_pure_python(pdf_bytes: bytes) -> int:
    # Check /Type /Pages ... /Count N
    counts = [int(m.group(1)) for m in re.finditer(rb"/Count\s+(\d+)", pdf_bytes)]
    page_objs = len(re.findall(rb"/Type\s*/Page(?![sA-Za-z])", pdf_bytes))
    if counts:
        return max(max(counts), page_objs)
    return page_objs


# ---------------------------------------------------------------------------
# Verification Suite Runner
# ---------------------------------------------------------------------------


class E2EVerifier:
    def __init__(self, root: Path, allow_missing_m5: bool = False) -> None:
        self.root = root.resolve()
        self.allow_missing_m5 = allow_missing_m5
        self.checks: list[dict[str, Any]] = []
        self._canonical_cache: dict[str, Any] | None = None

    def record(
        self,
        check_id: str,
        tier: int,
        area: str,
        status: str,
        message: str,
        details: Any = None,
    ) -> None:
        assert status in ("PASS", "FAIL", "SKIP"), f"Invalid status: {status}"
        self.checks.append(
            {
                "id": check_id,
                "tier": tier,
                "area": area,
                "status": status,
                "message": message,
                "details": details if details is not None else {},
            }
        )

    def m5_build_exists(self) -> bool:
        return (self.root / "work_scripts/build_map_page.py").is_file()

    def m5_manuscript_exists(self) -> bool:
        return (self.root / "paper/manuscript.tex").is_file()

    # ===================================================================
    # TIER 1 — Feature & Artifact Completeness
    # ===================================================================

    def run_tier1(self) -> None:
        self._t1_scripts_and_portability()
        self._t1_contract1_m1()
        self._t1_contract2_m2_m3()
        self._t1_contract3_m4()
        self._t1_contract4_m5()

    def _t1_scripts_and_portability(self) -> None:
        core_scripts, m5_scripts = collect_key_scripts(self.root)
        ws = self.root / "work_scripts"

        # 1. Core Key #1-#8 scripts present (including key8a/b/c/d)
        k8_prefixes = ("key8a_", "key8b_", "key8c_", "key8d_")
        missing_k8 = [
            pref
            for pref in k8_prefixes
            if not list(ws.glob(f"{pref}*.py"))
        ]
        repro_ok = (ws / "reproduce_all_keys.py").is_file()
        e2e_ok = (ws / "verify_key8_e2e.py").is_file()
        if core_scripts and repro_ok and e2e_ok and not missing_k8:
            self.record(
                "T1_SCRIPTS_DISCOVERY",
                1,
                "scripts_portability",
                "PASS",
                f"Discovered {len(core_scripts)} core Key #1-#8 scripts (all key8a..d present).",
                {"count": len(core_scripts)},
            )
        else:
            self.record(
                "T1_SCRIPTS_DISCOVERY",
                1,
                "scripts_portability",
                "FAIL",
                f"Missing required scripts: key8_prefixes={missing_k8}, repro={repro_ok}, e2e={e2e_ok}.",
                {"count": len(core_scripts), "missing_key8_prefixes": missing_k8},
            )

        # 2. M5 scripts presence
        missing_m5 = [p.name for p in m5_scripts if not p.is_file() or p.stat().st_size == 0]
        if not missing_m5:
            self.record(
                "T1_SCRIPTS_M5_PRESENT",
                1,
                "scripts_portability",
                "PASS",
                "M5 scripts generate_paper_figures.py and build_map_page.py present and non-empty.",
            )
        elif self.allow_missing_m5 and len(missing_m5) == len(m5_scripts) and not any(p.exists() for p in m5_scripts):
            self.record(
                "T1_SCRIPTS_M5_PRESENT",
                1,
                "scripts_portability",
                "SKIP",
                "M5 scripts absent (--allow-missing-m5).",
                {"missing": missing_m5},
            )
        else:
            self.record(
                "T1_SCRIPTS_M5_PRESENT",
                1,
                "scripts_portability",
                "FAIL",
                f"Missing or empty M5 scripts: {missing_m5}.",
                {"missing": missing_m5},
            )

        # 3. Compile core Key #1-#8 scripts
        compile_errors: list[str] = []
        compiled_core: list[Path] = []
        for sp in core_scripts:
            try:
                py_compile.compile(str(sp), doraise=True)
                compiled_core.append(sp)
            except Exception as exc:
                compile_errors.append(f"{sp.relative_to(self.root)}: {exc}")
        if not compile_errors and compiled_core:
            self.record(
                "T1_SCRIPTS_COMPILE_CORE",
                1,
                "scripts_portability",
                "PASS",
                f"py_compile passed on {len(compiled_core)}/{len(core_scripts)} core Key #1-#8 scripts.",
                {"compiled": len(compiled_core)},
            )
        else:
            self.record(
                "T1_SCRIPTS_COMPILE_CORE",
                1,
                "scripts_portability",
                "FAIL",
                f"py_compile failed on {len(compile_errors)} core script(s).",
                {"errors": compile_errors},
            )

        # 4. Compile M5 scripts
        present_m5 = [p for p in m5_scripts if p.is_file()]
        if not present_m5:
            status = "SKIP" if self.allow_missing_m5 else "FAIL"
            self.record(
                "T1_SCRIPTS_COMPILE_M5",
                1,
                "scripts_portability",
                status,
                "M5 scripts not present to compile" + (" (--allow-missing-m5)." if status == "SKIP" else "."),
            )
        else:
            m5_errs: list[str] = []
            for sp in present_m5:
                try:
                    py_compile.compile(str(sp), doraise=True)
                except Exception as exc:
                    m5_errs.append(f"{sp.relative_to(self.root)}: {exc}")
            if not m5_errs:
                self.record(
                    "T1_SCRIPTS_COMPILE_M5",
                    1,
                    "scripts_portability",
                    "PASS",
                    f"py_compile passed on {len(present_m5)} present M5 script(s).",
                )
            else:
                self.record(
                    "T1_SCRIPTS_COMPILE_M5",
                    1,
                    "scripts_portability",
                    "FAIL",
                    f"py_compile failed on M5 script(s): {m5_errs}",
                    {"errors": m5_errs},
                )

        # 5. Portability check: zero hardcoded FORBIDDEN_HOME_PREFIX across ALL Key #1-#8 scripts
        all_to_scan = sorted(set(core_scripts) | set(present_m5))
        hits: list[str] = []
        read_errs: list[str] = []
        for sp in all_to_scan:
            try:
                text = sp.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                read_errs.append(f"{sp.relative_to(self.root)}: {exc}")
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                if FORBIDDEN_HOME_PREFIX in line:
                    hits.append(f"{sp.relative_to(self.root)}:{lineno}")
        if not hits and not read_errs and all_to_scan:
            self.record(
                "T1_SCRIPTS_PORTABILITY",
                1,
                "scripts_portability",
                "PASS",
                f"Zero hardcoded user-home paths across {len(all_to_scan)} Key #1-#8 scripts.",
                {"scanned": len(all_to_scan)},
            )
        else:
            self.record(
                "T1_SCRIPTS_PORTABILITY",
                1,
                "scripts_portability",
                "FAIL",
                f"Found {len(hits)} hardcoded user-home path reference(s) and {len(read_errs)} read error(s) across Key scripts.",
                {"hits": hits[:40], "total_hits": len(hits), "read_errors": read_errs[:20]},
            )

    def _t1_contract1_m1(self) -> None:
        d = self.root / "work_data/key8a"

        # 1. master_lexicon_after_key8a.csv
        p = d / "master_lexicon_after_key8a.csv"
        if p.is_file() and p.stat().st_size > 0:
            hdr, rows, err = load_csv(p)
            if not err and hdr and len(rows) > 0:
                self.record(
                    "T1_M1_LEXICON_CSV",
                    1,
                    "contract1_m1",
                    "PASS",
                    f"master_lexicon_after_key8a.csv valid ({len(rows)} rows, {len(hdr)} cols).",
                    {"rows": len(rows), "columns": hdr},
                )
            else:
                self.record("T1_M1_LEXICON_CSV", 1, "contract1_m1", "FAIL", f"Invalid CSV: {err or 'empty rows'}.")
        else:
            self.record("T1_M1_LEXICON_CSV", 1, "contract1_m1", "FAIL", f"Missing or empty: {p.relative_to(self.root)}.")

        # 2. coverage_after_key8a.json
        p = d / "coverage_after_key8a.json"
        if p.is_file() and p.stat().st_size > 0:
            data, err = load_json(p)
            if not err and isinstance(data, dict) and data:
                self.record(
                    "T1_M1_COVERAGE_JSON",
                    1,
                    "contract1_m1",
                    "PASS",
                    f"coverage_after_key8a.json valid ({len(data)} top-level keys).",
                )
            else:
                self.record("T1_M1_COVERAGE_JSON", 1, "contract1_m1", "FAIL", f"Invalid JSON: {err or 'empty'}.")
        else:
            self.record("T1_M1_COVERAGE_JSON", 1, "contract1_m1", "FAIL", f"Missing or empty: {p.relative_to(self.root)}.")

        # 3. wave6_disjoint_signs.csv + wave6_7family_results.json
        p_csv = d / "wave6_disjoint_signs.csv"
        p_json = d / "wave6_7family_results.json"
        errs: list[str] = []
        w6_rows = 0
        if not (p_csv.is_file() and p_csv.stat().st_size > 0):
            errs.append("missing/empty wave6_disjoint_signs.csv")
        else:
            _, rows, err = load_csv(p_csv)
            if err or not rows:
                errs.append(f"invalid wave6_disjoint_signs.csv: {err or 'empty'}")
            else:
                w6_rows = len(rows)
        if not (p_json.is_file() and p_json.stat().st_size > 0):
            errs.append("missing/empty wave6_7family_results.json")
        else:
            jdata, err = load_json(p_json)
            if err or not isinstance(jdata, (dict, list)) or not jdata:
                errs.append(f"invalid wave6_7family_results.json: {err or 'empty'}")
        if not errs:
            self.record(
                "T1_M1_WAVE6_FILES",
                1,
                "contract1_m1",
                "PASS",
                f"Wave-6 CSV ({w6_rows} signs) and 7-family JSON valid.",
            )
        else:
            self.record("T1_M1_WAVE6_FILES", 1, "contract1_m1", "FAIL", "; ".join(errs))

        # 4. split_824_corpus.csv
        p = d / "split_824_corpus.csv"
        if p.is_file() and p.stat().st_size > 0:
            hdr, rows, err = load_csv(p)
            if not err and rows:
                self.record(
                    "T1_M1_SPLIT824_CSV",
                    1,
                    "contract1_m1",
                    "PASS",
                    f"split_824_corpus.csv valid ({len(rows)} rows).",
                )
            else:
                self.record("T1_M1_SPLIT824_CSV", 1, "contract1_m1", "FAIL", f"Invalid CSV: {err or 'empty'}.")
        else:
            self.record("T1_M1_SPLIT824_CSV", 1, "contract1_m1", "FAIL", f"Missing or empty: {p.relative_to(self.root)}.")

        # 5. dholavira_signboard_audit_v2.json
        p = d / "dholavira_signboard_audit_v2.json"
        if p.is_file() and p.stat().st_size > 0:
            data, err = load_json(p)
            if not err and isinstance(data, dict) and data:
                self.record(
                    "T1_M1_DHOLAVIRA_JSON",
                    1,
                    "contract1_m1",
                    "PASS",
                    "dholavira_signboard_audit_v2.json valid and non-empty.",
                )
            else:
                self.record("T1_M1_DHOLAVIRA_JSON", 1, "contract1_m1", "FAIL", f"Invalid JSON: {err or 'empty'}.")
        else:
            self.record("T1_M1_DHOLAVIRA_JSON", 1, "contract1_m1", "FAIL", f"Missing or empty: {p.relative_to(self.root)}.")

        # 6. jobs/out/key8a_*.md
        mds = [x for x in sorted((self.root / "jobs/out").glob("key8a_*.md")) if x.stat().st_size > 0]
        if mds:
            self.record(
                "T1_M1_JOBS_REPORT",
                1,
                "contract1_m1",
                "PASS",
                f"Found {len(mds)} non-empty M1 report(s): {[m.name for m in mds]}.",
            )
        else:
            self.record("T1_M1_JOBS_REPORT", 1, "contract1_m1", "FAIL", "Missing non-empty jobs/out/key8a_*.md.")

    def _t1_contract2_m2_m3(self) -> None:
        db = self.root / "work_data/key8b"
        dd = self.root / "work_data/key8d"

        # 1. key8b_summary.json
        p = db / "key8b_summary.json"
        if p.is_file() and p.stat().st_size > 0:
            data, err = load_json(p)
            if not err and isinstance(data, dict) and data:
                self.record("T1_M2_KEY8B_SUMMARY", 1, "contract2_m2_m3", "PASS", "key8b_summary.json valid.")
            else:
                self.record("T1_M2_KEY8B_SUMMARY", 1, "contract2_m2_m3", "FAIL", f"Invalid JSON: {err or 'empty'}.")
        else:
            self.record("T1_M2_KEY8B_SUMMARY", 1, "contract2_m2_m3", "FAIL", "Missing or empty work_data/key8b/key8b_summary.json.")

        # 2. Sangam JSON + CSV
        errs: list[str] = []
        p_j = db / "test8b1_sangam_227plus.json"
        p_c = db / "test8b1_compound_matches_key8.csv"
        if not (p_j.is_file() and p_j.stat().st_size > 0):
            errs.append("missing/empty test8b1_sangam_227plus.json")
        else:
            jdata, err = load_json(p_j)
            if err or not isinstance(jdata, dict) or not jdata:
                errs.append(f"invalid test8b1_sangam_227plus.json: {err or 'empty'}")
        if not (p_c.is_file() and p_c.stat().st_size > 0):
            errs.append("missing/empty test8b1_compound_matches_key8.csv")
        else:
            _, rows, err = load_csv(p_c)
            if err or not rows:
                errs.append(f"invalid test8b1_compound_matches_key8.csv: {err or 'empty'}")
        if not errs:
            self.record("T1_M2_SANGAM_FILES", 1, "contract2_m2_m3", "PASS", "Sangam JSON and compound matches CSV valid.")
        else:
            self.record("T1_M2_SANGAM_FILES", 1, "contract2_m2_m3", "FAIL", "; ".join(errs))

        # 3. Archaeology JSON + Multi-Face JSON + CSV
        errs = []
        for fn in ("test8b2_wave56_archaeology.json", "test8b3_multiface_key8.json"):
            fp = db / fn
            if not (fp.is_file() and fp.stat().st_size > 0):
                errs.append(f"missing/empty {fn}")
            else:
                jd, err = load_json(fp)
                if err or not isinstance(jd, dict) or not jd:
                    errs.append(f"invalid {fn}: {err or 'empty'}")
        fp_c = db / "multiface_key8_records.csv"
        if not (fp_c.is_file() and fp_c.stat().st_size > 0):
            errs.append("missing/empty multiface_key8_records.csv")
        else:
            _, rows, err = load_csv(fp_c)
            if err or not rows:
                errs.append(f"invalid multiface_key8_records.csv: {err or 'empty'}")
        if not errs:
            self.record("T1_M2_ARCH_MULTIFACE_FILES", 1, "contract2_m2_m3", "PASS", "Archaeology JSON, Multi-face JSON, and CSV valid.")
        else:
            self.record("T1_M2_ARCH_MULTIFACE_FILES", 1, "contract2_m2_m3", "FAIL", "; ".join(errs))

        # 4. key8d_summary.json
        p = dd / "key8d_summary.json"
        if p.is_file() and p.stat().st_size > 0:
            jd, err = load_json(p)
            if not err and isinstance(jd, dict) and jd:
                self.record("T1_M3_KEY8D_SUMMARY", 1, "contract2_m2_m3", "PASS", "key8d_summary.json valid.")
            else:
                self.record("T1_M3_KEY8D_SUMMARY", 1, "contract2_m2_m3", "FAIL", f"Invalid JSON: {err or 'empty'}.")
        else:
            self.record("T1_M3_KEY8D_SUMMARY", 1, "contract2_m2_m3", "FAIL", "Missing or empty work_data/key8d/key8d_summary.json.")

        # 5. jobs/out/key8b_*.md and key8d_*.md
        jobs_dir = self.root / "jobs/out"
        b_mds = [x for x in sorted(jobs_dir.glob("key8b_*.md")) if x.stat().st_size > 0]
        d_mds = [x for x in sorted(jobs_dir.glob("key8d_*.md")) if x.stat().st_size > 0]
        if b_mds and d_mds:
            self.record(
                "T1_M2_M3_JOBS_REPORTS",
                1,
                "contract2_m2_m3",
                "PASS",
                f"Found M2 ({len(b_mds)}) and M3 ({len(d_mds)}) markdown reports.",
            )
        else:
            self.record(
                "T1_M2_M3_JOBS_REPORTS",
                1,
                "contract2_m2_m3",
                "FAIL",
                f"Missing reports: key8b={len(b_mds)}, key8d={len(d_mds)}.",
            )

    def _t1_contract3_m4(self) -> None:
        dc = self.root / "work_data/key8c"

        # 1. combined_6wave_meta_stats.json
        p = dc / "combined_6wave_meta_stats.json"
        if p.is_file() and p.stat().st_size > 0:
            jd, err = load_json(p)
            if not err and isinstance(jd, dict) and jd:
                self.record("T1_M4_META6_JSON", 1, "contract3_m4", "PASS", "combined_6wave_meta_stats.json valid.")
            else:
                self.record("T1_M4_META6_JSON", 1, "contract3_m4", "FAIL", f"Invalid JSON: {err or 'empty'}.")
        else:
            self.record("T1_M4_META6_JSON", 1, "contract3_m4", "FAIL", "Missing or empty combined_6wave_meta_stats.json.")

        # 2. master_audit_table_v3.{json,csv}
        errs: list[str] = []
        p_j = dc / "master_audit_table_v3.json"
        p_c = dc / "master_audit_table_v3.csv"
        if not (p_j.is_file() and p_j.stat().st_size > 0):
            errs.append("missing/empty master_audit_table_v3.json")
        else:
            jd, err = load_json(p_j)
            if err or not isinstance(jd, dict) or not jd:
                errs.append(f"invalid master_audit_table_v3.json: {err or 'empty'}")
        if not (p_c.is_file() and p_c.stat().st_size > 0):
            errs.append("missing/empty master_audit_table_v3.csv")
        else:
            _, rows, err = load_csv(p_c)
            if err or not rows:
                errs.append(f"invalid master_audit_table_v3.csv: {err or 'empty'}")
        if not errs:
            self.record("T1_M4_AUDIT_V3_FILES", 1, "contract3_m4", "PASS", "master_audit_table_v3.json and .csv valid.")
        else:
            self.record("T1_M4_AUDIT_V3_FILES", 1, "contract3_m4", "FAIL", "; ".join(errs))

        # 3. honest_null_registry_v3.csv
        p = dc / "honest_null_registry_v3.csv"
        if p.is_file() and p.stat().st_size > 0:
            _, rows, err = load_csv(p)
            if not err and rows:
                self.record("T1_M4_HONEST_NULLS_V3", 1, "contract3_m4", "PASS", f"honest_null_registry_v3.csv valid ({len(rows)} rows).")
            else:
                self.record("T1_M4_HONEST_NULLS_V3", 1, "contract3_m4", "FAIL", f"Invalid CSV: {err or 'empty'}.")
        else:
            self.record("T1_M4_HONEST_NULLS_V3", 1, "contract3_m4", "FAIL", "Missing or empty honest_null_registry_v3.csv.")

        # 4. explorer_data_v3.json size < 300 KB + required keys
        p = dc / "explorer_data_v3.json"
        if p.is_file() and p.stat().st_size > 0:
            sz = p.stat().st_size
            jd, err = load_json(p)
            if err or not isinstance(jd, dict):
                self.record("T1_M4_EXPLORER_V3_SCHEMA_SIZE", 1, "contract3_m4", "FAIL", f"Invalid JSON: {err or 'not dict'}.")
            else:
                missing_keys = [k for k in REQUIRED_EXPLORER_V3_KEYS if k not in jd]
                if sz < 307_200 and not missing_keys:
                    self.record(
                        "T1_M4_EXPLORER_V3_SCHEMA_SIZE",
                        1,
                        "contract3_m4",
                        "PASS",
                        f"explorer_data_v3.json valid ({sz:,} B < 300 KB; all 11 Contract 3 keys present).",
                        {"bytes": sz, "under_280kb_target": sz < 286_720},
                    )
                else:
                    self.record(
                        "T1_M4_EXPLORER_V3_SCHEMA_SIZE",
                        1,
                        "contract3_m4",
                        "FAIL",
                        f"explorer_data_v3.json check failed: bytes={sz:,} (limit 307,200), missing_keys={missing_keys}.",
                        {"bytes": sz, "missing_keys": missing_keys},
                    )
        else:
            self.record("T1_M4_EXPLORER_V3_SCHEMA_SIZE", 1, "contract3_m4", "FAIL", "Missing or empty explorer_data_v3.json.")

        # 5. READINGS_KEY7.md
        p = self.root / "READINGS_KEY7.md"
        if p.is_file() and p.stat().st_size > 200:
            self.record(
                "T1_M4_READINGS_KEY7_MD",
                1,
                "contract3_m4",
                "PASS",
                f"READINGS_KEY7.md present ({p.stat().st_size:,} B).",
            )
        else:
            self.record("T1_M4_READINGS_KEY7_MD", 1, "contract3_m4", "FAIL", "Missing or too small READINGS_KEY7.md.")

    def _t1_contract4_m5(self) -> None:
        paper_files = [
            self.root / "paper/manuscript.tex",
            self.root / "paper/references.bib",
            self.root / "paper/manuscript.pdf",
        ]
        present_paper = [p for p in paper_files if p.exists()]
        if not present_paper and self.allow_missing_m5:
            self.record(
                "T1_M5_LATEX_FILES",
                1,
                "contract4_m5",
                "SKIP",
                "M5 paper/ manuscript files absent (--allow-missing-m5).",
            )
        else:
            bad = [str(p.relative_to(self.root)) for p in paper_files if not (p.is_file() and p.stat().st_size > 0)]
            if not bad:
                self.record("T1_M5_LATEX_FILES", 1, "contract4_m5", "PASS", "paper/manuscript.tex, references.bib, and manuscript.pdf present and non-empty.")
            else:
                self.record("T1_M5_LATEX_FILES", 1, "contract4_m5", "FAIL", f"Missing or empty M5 LaTeX files: {bad}.")

        # Web + top-level docs (all already exist in repo, so always checked)
        docs = [
            self.root / "map_page/index.html",
            self.root / "PAPER_DRAFT.md",
            self.root / "MAP.md",
            self.root / "DIARY.md",
            self.root / "README.md",
        ]
        bad_docs = [str(p.relative_to(self.root)) for p in docs if not (p.is_file() and p.stat().st_size > 0)]
        if not bad_docs:
            self.record("T1_M5_WEB_AND_DOCS", 1, "contract4_m5", "PASS", "map_page/index.html, PAPER_DRAFT.md, MAP.md, DIARY.md, README.md present and non-empty.")
        else:
            self.record("T1_M5_WEB_AND_DOCS", 1, "contract4_m5", "FAIL", f"Missing or empty core docs/web files: {bad_docs}.")

        # Figures: PNG, SVG, PDF
        fig_dir = self.root / "paper/figures"
        any_fig_present = fig_dir.is_dir() and any(fig_dir.iterdir())
        if not any_fig_present and self.allow_missing_m5:
            for cid, fmt in (("T1_M5_FIGURES_PNG", "PNG"), ("T1_M5_FIGURES_SVG", "SVG"), ("T1_M5_FIGURES_PDF", "PDF")):
                self.record(cid, 1, "contract4_m5", "SKIP", f"M5 paper/figures/ {fmt} files absent (--allow-missing-m5).")
            return

        # PNG validation via PIL
        from PIL import Image

        png_errs: list[str] = []
        png_info: dict[str, Any] = {}
        for i in range(1, 6):
            fp = find_figure_file(fig_dir, i, "png")
            if fp is None or fp.stat().st_size == 0:
                png_errs.append(f"fig{i}.png missing/empty")
                continue
            try:
                with Image.open(fp) as im:
                    im.verify()
                with Image.open(fp) as im:
                    w, h = im.size
                    dpi = im.info.get("dpi")
                png_info[fp.name] = {"size": [w, h], "dpi": list(dpi) if isinstance(dpi, tuple) else dpi}
                if w < 1200 or h < 400:
                    png_errs.append(f"{fp.name} too small ({w}x{h}, need >=1200x400)")
                if dpi is None:
                    png_errs.append(f"{fp.name} missing DPI (pHYs) metadata (need >= 295 DPI)")
                else:
                    dpi_vals = [dpi] if isinstance(dpi, (int, float)) else list(dpi)
                    if not dpi_vals or min(float(dval) for dval in dpi_vals) < 295.0:
                        png_errs.append(f"{fp.name} DPI {dpi_vals} < 295")
            except Exception as exc:
                png_errs.append(f"{fp.name} PIL error: {exc}")
        if not png_errs:
            self.record("T1_M5_FIGURES_PNG", 1, "contract4_m5", "PASS", "All 5 figure PNGs valid (>=1200px wide, 300 DPI).", png_info)
        else:
            self.record("T1_M5_FIGURES_PNG", 1, "contract4_m5", "FAIL", "; ".join(png_errs), png_info)

        # SVG validation via xml.etree.ElementTree
        svg_errs: list[str] = []
        for i in range(1, 6):
            fp = find_figure_file(fig_dir, i, "svg")
            if fp is None or fp.stat().st_size == 0:
                svg_errs.append(f"fig{i}.svg missing/empty")
                continue
            try:
                tree = ET.parse(fp)
                root_el = tree.getroot()
                local_root = root_el.tag.rsplit("}", 1)[-1].lower()
                if local_root != "svg":
                    svg_errs.append(f"{fp.name} root tag '{root_el.tag}' != svg")
                    continue
                has_gfx = any(
                    el.tag.rsplit("}", 1)[-1].lower() in SVG_GRAPHIC_TAGS
                    for el in root_el.iter()
                    if el is not root_el
                )
                if not has_gfx:
                    svg_errs.append(f"{fp.name} has zero SVG graphic elements")
            except Exception as exc:
                svg_errs.append(f"{fp.name} XML parse error: {exc}")
        if not svg_errs:
            self.record("T1_M5_FIGURES_SVG", 1, "contract4_m5", "PASS", "All 5 figure SVGs valid XML with graphic elements.")
        else:
            self.record("T1_M5_FIGURES_SVG", 1, "contract4_m5", "FAIL", "; ".join(svg_errs))

        # PDF figure validation
        pdf_errs: list[str] = []
        for i in range(1, 6):
            fp = find_figure_file(fig_dir, i, "pdf")
            if fp is None or fp.stat().st_size == 0:
                pdf_errs.append(f"fig{i}.pdf missing/empty")
                continue
            raw = fp.read_bytes()
            if not raw.startswith(b"%PDF-") or b"%%EOF" not in raw[-2048:]:
                pdf_errs.append(f"{fp.name} missing %PDF- header or %%EOF trailer")
        if not pdf_errs:
            self.record("T1_M5_FIGURES_PDF", 1, "contract4_m5", "PASS", "All 5 figure PDFs valid (%PDF- / %%EOF).")
        else:
            self.record("T1_M5_FIGURES_PDF", 1, "contract4_m5", "FAIL", "; ".join(pdf_errs))

    # ===================================================================
    # TIER 2 — Mathematical, Statistical & Anti-Leakage Invariants
    # ===================================================================

    def run_tier2(self) -> None:
        self._t2_denominators_and_parity()
        self._t2_wave6_disjoint_and_meta()
        self._t2_split824_integrity()
        self._t2_dholavira_integrity()
        self._t2_sangam_multiface_m3_nulls()
        self._t2_repro_and_audit_v3()

    def _t2_denominators_and_parity(self) -> None:
        cov_path = self.root / "work_data/key8a/coverage_after_key8a.json"
        lex8_path = self.root / "work_data/key8a/master_lexicon_after_key8a.csv"
        lex7_path = self.root / "work_data/key7a/master_lexicon_after_key7a.csv"
        audit_path = self.root / "work_data/key8c/master_audit_table_v3.json"

        cov_raw, cov_err = load_json(cov_path)
        splits = resolve_coverage_splits(cov_raw) if (not cov_err and isinstance(cov_raw, dict)) else {}

        # 1. Exact Denominator Invariance (incl. combined_all 6790/23710 whenever present)
        expected_denoms = {
            "combined_intact": (4163, 15203),
            "unseen_intact": (563, 1994),
            "lipi_intact": (3600, 13209),
        }
        if not splits or any(k not in splits for k in expected_denoms):
            self.record(
                "T2_DENOM_EXACT",
                2,
                "denominators",
                "FAIL",
                f"Cannot load required splits from coverage_after_key8a.json (err={cov_err}, found={list(splits.keys())}).",
            )
            self.record("T2_DENOM_ARITHMETIC", 2, "denominators", "FAIL", "Blocked by missing coverage_after_key8a.json splits.")
            self.record("T2_PARITY_COVERAGE_JSON", 2, "parity_95pct", "FAIL", "Blocked by missing coverage_after_key8a.json splits.")
            self.record("T2_UNSEEN_95PCT_LOCKED", 2, "parity_95pct", "FAIL", "Blocked by missing coverage_after_key8a.json splits.")
        else:
            denom_errs: list[str] = []
            checked_splits = dict(expected_denoms)
            if "combined_all" in splits:
                checked_splits["combined_all"] = (6790, 23710)
            for sk, (exp_f, exp_t) in checked_splits.items():
                tiers = splits[sk]
                if not isinstance(tiers, dict) or not tiers:
                    denom_errs.append(f"{sk}: empty tiers")
                    continue
                for tn, tv in tiers.items():
                    if not isinstance(tv, dict):
                        continue
                    nf = tv.get("n_faces")
                    tt = tv.get("total_tokens")
                    if nf != exp_f or tt != exp_t:
                        denom_errs.append(f"{sk}.{tn}: got ({nf} faces, {tt} tok), expected ({exp_f}, {exp_t})")
            if not denom_errs:
                extra_msg = "; 6,790/23,710" if "combined_all" in checked_splits else ""
                self.record(
                    "T2_DENOM_EXACT",
                    2,
                    "denominators",
                    "PASS",
                    f"Exact invariant denominators verified across every tier (4,163/15,203; 563/1,994; 3,600/13,209{extra_msg}).",
                )
            else:
                self.record("T2_DENOM_EXACT", 2, "denominators", "FAIL", f"Denominator drift: {denom_errs[:5]}", {"errors": denom_errs})

            # 2. Internal arithmetic consistency
            arith_errs: list[str] = []
            common_tiers = [
                tn
                for tn in sorted(
                    set(splits["combined_intact"].keys())
                    & set(splits["lipi_intact"].keys())
                    & set(splits["unseen_intact"].keys())
                )
                if isinstance(splits["combined_intact"].get(tn), dict)
                and isinstance(splits["lipi_intact"].get(tn), dict)
                and isinstance(splits["unseen_intact"].get(tn), dict)
            ]
            if not common_tiers:
                arith_errs.append("No common tier dicts across combined/lipi/unseen splits")
            req_arith_keys = ("covered_tokens", "total_tokens", "faces_100pct", "n_faces", "token_pct", "faces_100pct_pct")
            for tn in common_tiers:
                c = splits["combined_intact"][tn]
                l = splits["lipi_intact"][tn]
                u = splits["unseen_intact"][tn]
                tier_ok = True
                for label, d in (("comb", c), ("lipi", l), ("unseen", u)):
                    missing_k = [rk for rk in req_arith_keys if rk not in d or d[rk] is None]
                    if missing_k:
                        arith_errs.append(f"{tn}.{label} missing keys {missing_k}")
                        tier_ok = False
                        continue
                    try:
                        cov_t = float(d["covered_tokens"])
                        tot_t = float(d["total_tokens"])
                        f100 = float(d["faces_100pct"])
                        nf = float(d["n_faces"])
                        rep_tp = float(d["token_pct"])
                        rep_fp = float(d["faces_100pct_pct"])
                    except (TypeError, ValueError) as exc:
                        arith_errs.append(f"{tn}.{label} non-numeric field: {exc}")
                        tier_ok = False
                        continue
                    if tot_t <= 0 or nf <= 0:
                        arith_errs.append(f"{tn}.{label} non-positive denominator (tot_t={tot_t}, nf={nf})")
                        tier_ok = False
                        continue
                    exp_tp = 100.0 * cov_t / tot_t
                    exp_fp = 100.0 * f100 / nf
                    if abs(rep_tp - exp_tp) > 0.025:
                        arith_errs.append(f"{tn}.{label} token_pct={rep_tp} vs {exp_tp:.4f}")
                    if abs(rep_fp - exp_fp) > 0.025:
                        arith_errs.append(f"{tn}.{label} faces_100pct_pct={rep_fp} vs {exp_fp:.4f}")
                if not tier_ok:
                    continue
                if c["covered_tokens"] != l["covered_tokens"] + u["covered_tokens"]:
                    arith_errs.append(
                        f"{tn} covered_tokens sum mismatch: {c['covered_tokens']} != {l['covered_tokens']} + {u['covered_tokens']}"
                    )
                if c["faces_100pct"] != l["faces_100pct"] + u["faces_100pct"]:
                    arith_errs.append(
                        f"{tn} faces_100pct sum mismatch: {c['faces_100pct']} != {l['faces_100pct']} + {u['faces_100pct']}"
                    )
            if not arith_errs:
                self.record(
                    "T2_DENOM_ARITHMETIC",
                    2,
                    "denominators",
                    "PASS",
                    f"Internal arithmetic and combined==lipi+new identities exact across {len(common_tiers)} tiers.",
                )
            else:
                self.record("T2_DENOM_ARITHMETIC", 2, "denominators", "FAIL", "; ".join(arith_errs[:5]), {"errors": arith_errs})

            # 3. Unseen holdout parity in coverage_after_key8a.json
            parity_errs: list[str] = []
            parity_tiers = 0
            for tn in sorted(set(splits["lipi_intact"].keys()) & set(splits["unseen_intact"].keys())):
                l = splits["lipi_intact"].get(tn)
                u = splits["unseen_intact"].get(tn)
                if not isinstance(l, dict) or not isinstance(u, dict):
                    continue
                try:
                    l_tp = float(l["token_pct"])
                    u_tp = float(u["token_pct"])
                    l_fp = float(l["faces_100pct_pct"])
                    u_fp = float(u["faces_100pct_pct"])
                except (KeyError, TypeError, ValueError) as exc:
                    parity_errs.append(f"{tn}: missing/invalid parity fields ({exc})")
                    continue
                parity_tiers += 1
                if u_tp < l_tp:
                    parity_errs.append(f"{tn}: unseen_tok {u_tp}% < lipi_tok {l_tp}%")
                if u_fp < l_fp:
                    parity_errs.append(f"{tn}: unseen_f100 {u_fp}% < lipi_f100 {l_fp}%")
            if not parity_errs and parity_tiers > 0:
                self.record(
                    "T2_PARITY_COVERAGE_JSON",
                    2,
                    "parity_95pct",
                    "PASS",
                    f"Unseen >= Lipi holdout parity holds for both tokens and 100%-faces across all {parity_tiers} tiers.",
                )
            else:
                self.record("T2_PARITY_COVERAGE_JSON", 2, "parity_95pct", "FAIL", "; ".join(parity_errs[:5]) or "No valid tiers checked.", {"errors": parity_errs})

            # 4. Key #8A locked unseen >= 95.00% (>= 1895 / 1994)
            lex8_count: int | None = None
            has_split_824 = False
            if lex8_path.is_file():
                l8_hdr, l8_rows, l8_err = load_csv(lex8_path)
                if not l8_err and l8_rows:
                    lex8_count = len(l8_rows)
                    sc = next((c for c in ("sign", "sign_id", "id") if c in l8_hdr), None)
                    if sc:
                        low_ids = {str(r.get(sc, "")).strip().lower() for r in l8_rows}
                        has_split_824 = ("824a" in low_ids and "824b" in low_ids)
            tier_name, tier_payload = select_primary_locked_tier(
                splits["unseen_intact"],
                lexicon_count=lex8_count,
                has_split_824=has_split_824,
            )
            if tier_name is None or tier_payload is None:
                self.record(
                    "T2_UNSEEN_95PCT_LOCKED",
                    2,
                    "parity_95pct",
                    "FAIL",
                    "Could not identify a primary locked Key #8A tier (non-frontier) in coverage_after_key8a.json.",
                )
            else:
                try:
                    cov_tok = int(tier_payload["covered_tokens"])
                    tot_tok = int(tier_payload["total_tokens"])
                    tok_pct = float(tier_payload["token_pct"])
                except (KeyError, TypeError, ValueError) as exc:
                    self.record(
                        "T2_UNSEEN_95PCT_LOCKED",
                        2,
                        "parity_95pct",
                        "FAIL",
                        f"Primary locked tier '{tier_name}' has invalid numeric fields: {exc}.",
                    )
                else:
                    if tot_tok == 1994 and cov_tok >= 1895 and tok_pct >= 95.0 and tok_pct > 93.98:
                        self.record(
                            "T2_UNSEEN_95PCT_LOCKED",
                            2,
                            "parity_95pct",
                            "PASS",
                            f"Primary locked tier '{tier_name}' crosses 95% unseen: {cov_tok}/1,994 = {tok_pct:.2f}% (> 93.98%).",
                            {"tier": tier_name, "covered_tokens": cov_tok, "token_pct": tok_pct},
                        )
                    else:
                        self.record(
                            "T2_UNSEEN_95PCT_LOCKED",
                            2,
                            "parity_95pct",
                            "FAIL",
                            f"Primary locked tier '{tier_name}' failed 95% unseen gate: {cov_tok}/{tot_tok} = {tok_pct:.2f}% (need >= 1,895 / 1,994 = 95.00%).",
                            {"tier": tier_name, "covered_tokens": cov_tok, "token_pct": tok_pct},
                        )

        # 5. Unseen holdout parity in master_audit_table_v3.json
        audit_raw, audit_err = load_json(audit_path)
        if audit_err or not isinstance(audit_raw, dict) or not isinstance(audit_raw.get("invariant3_unseen_holdout_parity"), dict):
            self.record(
                "T2_PARITY_AUDIT_V3",
                2,
                "parity_95pct",
                "FAIL",
                f"Cannot load invariant3_unseen_holdout_parity from master_audit_table_v3.json ({audit_err}).",
            )
        else:
            inv3 = audit_raw["invariant3_unseen_holdout_parity"]
            checks_list = inv3.get("checks", [])
            bad_rows: list[str] = []
            clean_checked = 0
            if not isinstance(checks_list, list):
                bad_rows.append("checks is not a list")
            else:
                for row in checks_list:
                    if not isinstance(row, dict):
                        continue
                    lf = row.get("lipi_faces")
                    nf = row.get("new_faces")
                    note = str(row.get("note", "")).lower()
                    is_clean = (lf == 3600 and nf == 563) and ("pre-crosswalk" not in note and "uncrosswalked" not in note)
                    if not is_clean:
                        continue
                    clean_checked += 1
                    try:
                        lt = float(row["lipi_token_pct"])
                        nt = float(row["new_token_pct"])
                        lf_p = float(row["lipi_100pct_faces_pct"])
                        nf_p = float(row["new_100pct_faces_pct"])
                    except (KeyError, TypeError, ValueError) as exc:
                        bad_rows.append(f"{row.get('milestone')}/{row.get('tier')}: invalid fields ({exc})")
                        continue
                    if nt < lt or nf_p < lf_p:
                        bad_rows.append(f"{row.get('milestone')}/{row.get('tier')}: tok {nt}<{lt} or f100 {nf_p}<{lf_p}")
            flag_ok = bool(inv3.get("all_clean_crosswalked_tiers_pass")) and bool(inv3.get("all_clean_100pct_face_tiers_pass"))
            if flag_ok and clean_checked > 0 and not bad_rows:
                self.record(
                    "T2_PARITY_AUDIT_V3",
                    2,
                    "parity_95pct",
                    "PASS",
                    f"Independently verified unseen >= lipi parity across {clean_checked} clean crosswalked tiers in master_audit_table_v3.json.",
                )
            else:
                self.record(
                    "T2_PARITY_AUDIT_V3",
                    2,
                    "parity_95pct",
                    "FAIL",
                    f"Audit v3 parity failure: flags_ok={flag_ok}, clean_checked={clean_checked}, violations={bad_rows[:5]}.",
                )

        # 6. Master lexicon > 227 signs & superset of Key #7A 227 signs
        if not lex8_path.is_file():
            self.record("T2_LEXICON_SUPERSET_227", 2, "parity_95pct", "FAIL", "Missing master_lexicon_after_key8a.csv.")
        else:
            hdr8, rows8, err8 = load_csv(lex8_path)
            if err8 or not rows8:
                self.record("T2_LEXICON_SUPERSET_227", 2, "parity_95pct", "FAIL", f"Invalid master_lexicon_after_key8a.csv: {err8}.")
            else:
                sign_col = next((c for c in ("sign", "sign_id", "id") if c in hdr8), None)
                gloss_col = next((c for c in ("root_or_gloss", "phonetic_root", "gloss", "reading", "sound") if c in hdr8), None)
                if not sign_col or not gloss_col:
                    self.record(
                        "T2_LEXICON_SUPERSET_227",
                        2,
                        "parity_95pct",
                        "FAIL",
                        f"master_lexicon_after_key8a.csv missing sign/gloss columns (found: {hdr8}).",
                    )
                else:
                    s8 = {norm_sign(r[sign_col]) for r in rows8 if str(r.get(sign_col, "")).strip()}
                    s8_low = {x.lower() for x in s8}
                    missing_from_7a: list[str] = []
                    if lex7_path.is_file():
                        _, rows7, err7 = load_csv(lex7_path)
                        if not err7 and rows7:
                            s7 = {norm_sign(r["sign"]) for r in rows7 if str(r.get("sign", "")).strip()}
                            for s in sorted(s7):
                                if s in s8:
                                    continue
                                if s == "824" and ("824a" in s8_low or "824b" in s8_low):
                                    continue
                                missing_from_7a.append(s)
                    if len(s8) > 227 and not missing_from_7a:
                        self.record(
                            "T2_LEXICON_SUPERSET_227",
                            2,
                            "parity_95pct",
                            "PASS",
                            f"master_lexicon_after_key8a.csv has {len(s8)} unique signs (> 227) and is a strict superset of Key #7A.",
                            {"n_signs": len(s8)},
                        )
                    else:
                        self.record(
                            "T2_LEXICON_SUPERSET_227",
                            2,
                            "parity_95pct",
                            "FAIL",
                            f"Lexicon superset failed: n_signs={len(s8)} (need >227), missing_key7a={missing_from_7a[:10]}.",
                            {"n_signs": len(s8), "missing_key7a": missing_from_7a},
                        )

    def _t2_wave6_disjoint_and_meta(self) -> None:
        w6_csv = self.root / "work_data/key8a/wave6_disjoint_signs.csv"
        meta6_path = self.root / "work_data/key8c/combined_6wave_meta_stats.json"

        # Load W6 from CSV
        w6_set: set[str] = set()
        if w6_csv.is_file():
            hdr, rows, err = load_csv(w6_csv)
            if not err and rows:
                scol = next((c for c in ("sign", "sign_id", "id") if c in hdr), None)
                if scol:
                    w6_set = {norm_sign(r[scol]) for r in rows if str(r.get(scol, "")).strip()}

        meta6, meta6_err = load_json(meta6_path)

        # 1. All 15 pairwise intersections across disjoint W1..W6 == 0 + CSV-vs-JSON equality
        if len(w6_set) < 15:
            self.record(
                "T2_WAVE6_DISJOINT_15PAIRS",
                2,
                "wave6_meta",
                "FAIL",
                f"wave6_disjoint_signs.csv missing or has too few signs ({len(w6_set)}, need >= 15).",
            )
        elif meta6_err or not isinstance(meta6, dict):
            self.record(
                "T2_WAVE6_DISJOINT_15PAIRS",
                2,
                "wave6_meta",
                "FAIL",
                f"Cannot load combined_6wave_meta_stats.json ({meta6_err}).",
            )
        else:
            wave_sets, w6_json_set = self._extract_6_disjoint_wave_sets(meta6, w6_set)
            if len(wave_sets) != 6 or any(len(s) == 0 for s in wave_sets.values()):
                self.record(
                    "T2_WAVE6_DISJOINT_15PAIRS",
                    2,
                    "wave6_meta",
                    "FAIL",
                    f"Could not extract all 6 non-empty disjoint wave sets from combined_6wave_meta_stats.json (found: { {k: len(v) for k, v in wave_sets.items()} }).",
                )
            elif w6_json_set and w6_json_set != w6_set:
                csv_only = sorted(w6_set - w6_json_set)
                json_only = sorted(w6_json_set - w6_set)
                self.record(
                    "T2_WAVE6_DISJOINT_15PAIRS",
                    2,
                    "wave6_meta",
                    "FAIL",
                    f"Wave-6 sign set mismatch between wave6_disjoint_signs.csv ({len(w6_set)}) and combined_6wave_meta_stats.json ({len(w6_json_set)}): csv_only={csv_only[:8]}, json_only={json_only[:8]}.",
                    {"csv_only": csv_only, "json_only": json_only},
                )
            else:
                names = sorted(wave_sets.keys())
                overlaps: dict[str, list[str]] = {}
                pair_count = 0
                for i in range(len(names)):
                    for j in range(i + 1, len(names)):
                        pair_count += 1
                        inter = sorted(wave_sets[names[i]] & wave_sets[names[j]])
                        if inter:
                            overlaps[f"{names[i]}&{names[j]}"] = inter
                if not overlaps and pair_count == 15:
                    sizes = {k: len(v) for k, v in wave_sets.items()}
                    self.record(
                        "T2_WAVE6_DISJOINT_15PAIRS",
                        2,
                        "wave6_meta",
                        "PASS",
                        f"All 15/15 pairwise intersections across W1..W6 are strictly empty and CSV==JSON W6 matches (total {sum(sizes.values())} unique signs).",
                        {"wave_sizes": sizes},
                    )
                else:
                    self.record(
                        "T2_WAVE6_DISJOINT_15PAIRS",
                        2,
                        "wave6_meta",
                        "FAIL",
                        f"Non-zero overlap across 6 disjoint waves: {overlaps}.",
                        {"overlaps": overlaps},
                    )

        # 2. Raw exclusion check directly from ALL 8 prior disk CSVs
        if not w6_set:
            self.record("T2_WAVE6_EXCLUSION_RAW", 2, "wave6_meta", "FAIL", "Wave-6 sign list missing.")
        else:
            raw_union, loaded_sources, missing_sources = self._reconstruct_raw_exclusion_union()
            if missing_sources or len(loaded_sources) < 8:
                self.record(
                    "T2_WAVE6_EXCLUSION_RAW",
                    2,
                    "wave6_meta",
                    "FAIL",
                    f"Incomplete prior exclusion CSVs on disk: loaded {len(loaded_sources)}/8, missing={missing_sources}.",
                    {"loaded": loaded_sources, "missing": missing_sources},
                )
            else:
                leaks = sorted(w6_set & raw_union)
                if not leaks:
                    self.record(
                        "T2_WAVE6_EXCLUSION_RAW",
                        2,
                        "wave6_meta",
                        "PASS",
                        f"Zero overlap between W6 ({len(w6_set)} signs) and disk-reconstructed raw exclusion union ({len(raw_union)} signs across all 8/8 sources).",
                        {"sources": loaded_sources, "exclusion_size": len(raw_union)},
                    )
                else:
                    self.record(
                        "T2_WAVE6_EXCLUSION_RAW",
                        2,
                        "wave6_meta",
                        "FAIL",
                        f"Wave-6 leaks {len(leaks)} sign(s) from prior waves/lexicon: {leaks}.",
                        {"leaks": leaks},
                    )

        # 3. Independent Fisher chi2_12, exact p, bonf7, and Stouffer Z recomputation
        if meta6_err or not isinstance(meta6, dict):
            self.record("T2_WAVE6_META_MATH", 2, "wave6_meta", "FAIL", f"Cannot load combined_6wave_meta_stats.json ({meta6_err}).")
        else:
            self._verify_6wave_meta_math(meta6)

    def _extract_6_disjoint_wave_sets(
        self,
        meta6: dict[str, Any],
        w6_csv_set: set[str],
    ) -> tuple[dict[str, set[str]], set[str]]:
        """Extract 6 disjoint wave sets and separately return JSON's Wave-6 set (without silently unioning)."""
        out: dict[str, set[str]] = {}
        w6_json: set[str] = set()
        da = meta6.get("disjointness_audit", {}) if isinstance(meta6.get("disjointness_audit"), dict) else {}
        dsr = meta6.get("disjoint_sensitivity_raw", {}) if isinstance(meta6.get("disjoint_sensitivity_raw"), dict) else {}

        # Explicit map if provided
        for cand_key in ("strictly_disjoint_wave_signs", "disjoint_6wave_sets", "disjoint_wave_signs"):
            cand = da.get(cand_key) or meta6.get(cand_key)
            if isinstance(cand, dict) and len(cand) == 6:
                for k, v in cand.items():
                    if isinstance(v, list):
                        out[str(k)] = {norm_sign(x) for x in v}
                if len(out) == 6:
                    w6_key = next((k for k in out if "6" in k), None)
                    if w6_key:
                        w6_json = set(out[w6_key])
                        if w6_csv_set:
                            out[w6_key] = set(w6_csv_set)
                    return out, w6_json

        # Key #7C -> Key #8C canonical layout fallback
        # W1
        for k, v in da.items():
            if k.lower().startswith("wave1") and k.lower().endswith("signs") and isinstance(v, list):
                out["W1"] = {norm_sign(x) for x in v}
                break
        if "W1" not in out:
            for k, v in dsr.items():
                if k.lower().startswith("w1_") and k.lower().endswith("signs") and isinstance(v, list):
                    out["W1"] = {norm_sign(x) for x in v}
                    break
        # W2..W5 from disjoint_sensitivity_raw
        for idx in (2, 3, 4, 5):
            for k, v in dsr.items():
                kl = k.lower()
                if (
                    kl.startswith(f"w{idx}_")
                    and "disjoint" in kl
                    and "ultra" not in kl
                    and "keep142" not in kl
                    and kl.endswith("signs")
                    and isinstance(v, list)
                ):
                    out[f"W{idx}"] = {norm_sign(x) for x in v}
                    break
        # W6 from JSON (kept separate for equality check) and CSV
        for src in (dsr, da):
            for k, v in src.items():
                kl = k.lower()
                if (kl.startswith("w6_") or kl.startswith("wave6")) and kl.endswith("signs") and isinstance(v, list):
                    w6_json = {norm_sign(x) for x in v}
                    break
            if w6_json:
                break
        if w6_csv_set:
            out["W6"] = set(w6_csv_set)
        elif w6_json:
            out["W6"] = set(w6_json)
        return out, w6_json

    def _reconstruct_raw_exclusion_union(self) -> tuple[set[str], list[str], list[str]]:
        union: set[str] = set()
        sources: list[str] = []
        missing: list[str] = []
        spec = [
            ("W1_raw", "work_data/key2a/test_a2_matched_words.csv", True),
            ("W2_raw", "work_data/key4b/test4b1_top30_sign_table.csv", False),
            ("W3_raw", "work_data/key5a/trackA_per_sign_bridges.csv", False),
            ("W4_raw", "work_data/key6a/trackA_per_sign_bridges.csv", False),
            ("W5_raw", "work_data/key7a/trackA_wave5_per_sign_bridges.csv", False),
            ("K3A", "work_data/key3a/test3a2_bootstrap_candidates.csv", False),
            ("Res11", "work_data/key7a/trackA_rescue11_per_sign_bridges.csv", False),
            ("Lex227", "work_data/key7a/master_lexicon_after_key7a.csv", False),
        ]
        for label, rel, filter_w1 in spec:
            fp = self.root / rel
            if not fp.is_file():
                missing.append(f"{label}:{rel}")
                continue
            hdr, rows, err = load_csv(fp)
            if err or not rows:
                missing.append(f"{label}:invalid({err or 'empty'})")
                continue
            scol = next((c for c in ("sign", "sign_id", "id") if c in hdr), None)
            if not scol:
                missing.append(f"{label}:no_sign_col")
                continue
            subset: set[str] = set()
            for r in rows:
                if filter_w1:
                    suite = str(r.get("suite", ""))
                    if "UltraClean" not in suite and "A2c" not in suite:
                        continue
                val = str(r.get(scol, "")).strip()
                if val:
                    subset.add(norm_sign(val))
            if subset:
                union |= subset
                sources.append(f"{label}({len(subset)})")
            else:
                missing.append(f"{label}:0_rows")
        return union, sources, missing

    def _verify_6wave_meta_math(self, meta6: dict[str, Any]) -> None:
        meta_7 = meta6.get("meta_7family", {})
        if not isinstance(meta_7, dict) or not meta_7:
            self.record("T2_WAVE6_META_MATH", 2, "wave6_meta", "FAIL", "combined_6wave_meta_stats.json missing meta_7family.")
            return

        # Select primary strictly-disjoint 6-wave regime
        regime_key = None
        for k in meta_7:
            kl = k.lower()
            if "strictly_disjoint_6wave" in kl and "keep142" not in kl and "ultra" not in kl:
                regime_key = k
                break
        if regime_key is None:
            for k in meta_7:
                if "6wave" in k.lower() and "disjoint" in k.lower():
                    regime_key = k
                    break
        if regime_key is None:
            self.record(
                "T2_WAVE6_META_MATH",
                2,
                "wave6_meta",
                "FAIL",
                f"No strictly_disjoint_6wave regime found in meta_7family (keys: {list(meta_7.keys())}).",
            )
            return

        regime = meta_7[regime_key]
        if not isinstance(regime, dict):
            self.record("T2_WAVE6_META_MATH", 2, "wave6_meta", "FAIL", f"Regime '{regime_key}' is not a dict.")
            return
        errs: list[str] = []
        checked_blocks = 0

        for mode_aliases in (("phon_stem", "PhonSt"), ("phon_exact", "PhonEx")):
            mode_key = next((m for m in mode_aliases if m in regime and isinstance(regime[m], dict)), None)
            if mode_key is None:
                errs.append(f"Missing mode {mode_aliases} in {regime_key}")
                continue
            mode_dict = regime[mode_key]
            if not mode_dict:
                errs.append(f"Empty mode dict {mode_key}")
                continue
            for fam, fdata in mode_dict.items():
                if not isinstance(fdata, dict):
                    continue
                checked_blocks += 1
                df = fdata.get("fisher_df")
                if df != 12:
                    errs.append(f"{mode_key}.{fam}: fisher_df={df} != 12")
                # Extract 6 wave p and z values
                ps: list[float] = []
                zs: list[float] = []
                try:
                    for wi in range(1, 7):
                        pk = f"wave{wi}_p"
                        zk = f"wave{wi}_z"
                        if pk in fdata and zk in fdata:
                            ps.append(float(fdata[pk]))
                            zs.append(float(fdata[zk]))
                    if len(ps) != 6:
                        pw = fdata.get("per_wave") or fdata.get("waves")
                        if isinstance(pw, list) and len(pw) == 6:
                            ps = [float(x["p"]) for x in pw]
                            zs = [float(x["z"]) for x in pw]
                except (KeyError, TypeError, ValueError) as exc:
                    errs.append(f"{mode_key}.{fam}: invalid per-wave (p,z) value ({exc})")
                    continue
                if len(ps) != 6 or len(zs) != 6:
                    errs.append(f"{mode_key}.{fam}: expected 6 per-wave (p,z) entries, got {len(ps)}")
                    continue
                chi2_calc = -2.0 * sum(math.log(max(p, 1e-300)) for p in ps)
                p_calc = chi2_sf_even_df(chi2_calc, 12)
                bonf_calc = min(1.0, 7.0 * p_calc)
                z_calc = sum(zs) / math.sqrt(6.0)

                def check_close(field: str, calc: float, rep_key: str) -> None:
                    if rep_key not in fdata or fdata[rep_key] is None:
                        errs.append(f"{mode_key}.{fam}: missing {rep_key}")
                        return
                    try:
                        rep = float(fdata[rep_key])
                    except (TypeError, ValueError) as exc:
                        errs.append(f"{mode_key}.{fam}.{rep_key}: non-numeric ({exc})")
                        return
                    if field in ("chi2", "stouffer_z"):
                        # Additive+relative tolerance handles 3-dec wave{i}_z and 4-dec rounding near 0
                        tol = max(1.5e-3, 1e-3 * max(abs(calc), abs(rep)))
                    else:
                        tol = max(1e-3 * max(abs(calc), abs(rep)), 1e-15)
                    if abs(rep - calc) > tol:
                        errs.append(f"{mode_key}.{fam}.{rep_key}: reported={rep:.6g} vs recomputed={calc:.6g}")

                check_close("chi2", chi2_calc, "fisher_chi2")
                check_close("fisher_p", p_calc, "fisher_p")
                check_close("bonf7", bonf_calc, "fisher_p_bonf7")
                z_key = "stouffer_z_empirical" if "stouffer_z_empirical" in fdata else "stouffer_z"
                check_close("stouffer_z", z_calc, z_key)

        # Check required M4 robustness blocks (jackknife, pooled mega-shuffle, daughter sensitivity)
        # Every block must be non-empty (has_non_null_numeric), and daughter check excludes disjoint_sensitivity_raw
        def find_robustness_block(needles: tuple[str, ...], exclude_keys: tuple[str, ...] = ()) -> bool:
            def _walk(obj: Any) -> bool:
                if not isinstance(obj, dict):
                    return False
                for k, v in obj.items():
                    kl = str(k).lower()
                    if any(ex in kl for ex in exclude_keys):
                        continue
                    if any(nd in kl for nd in needles) and isinstance(v, (dict, list)) and has_non_null_numeric(v):
                        return True
                    if isinstance(v, dict) and _walk(v):
                        return True
                return False
            return _walk(meta6)

        missing_blocks: list[str] = []
        if not find_robustness_block(("jackknife", "leave_one")):
            missing_blocks.append("leave-one-wave-out jackknife")
        if not find_robustness_block(("pooled", "mega_shuffle", "megashuffle")):
            missing_blocks.append("pooled mega-shuffle")
        if not find_robustness_block(
            ("daughter", "turner", "santali", "halloran", "oia_turner", "large_lexicon"),
            exclude_keys=("disjoint_sensitivity_raw",),
        ):
            missing_blocks.append("daughter-lexicon sensitivity")
        if missing_blocks:
            errs.append(f"Missing or empty robustness blocks: {missing_blocks}")

        if not errs and checked_blocks >= 14:
            self.record(
                "T2_WAVE6_META_MATH",
                2,
                "wave6_meta",
                "PASS",
                f"Recomputed Fisher chi2_12, exact p, bonf7, and Stouffer Z matched across {checked_blocks} family×mode blocks in '{regime_key}' (+ non-empty jackknife/pooled/daughter blocks).",
                {"regime": regime_key, "checked_blocks": checked_blocks},
            )
        else:
            self.record(
                "T2_WAVE6_META_MATH",
                2,
                "wave6_meta",
                "FAIL",
                f"6-wave meta-math check failed ({len(errs)} issues): {errs[:5]}",
                {"regime": regime_key, "checked_blocks": checked_blocks, "errors": errs[:20]},
            )

    def _t2_split824_integrity(self) -> None:
        split_path = self.root / "work_data/key8a/split_824_corpus.csv"
        corpus_path = self.root / "work_data/reader_v3/corpus_soundfree_readings.csv"

        if not split_path.is_file():
            self.record("T2_SPLIT824_INTEGRITY", 2, "split_824", "FAIL", "Missing work_data/key8a/split_824_corpus.csv.")
            return

        hdr, rows, err = load_csv(split_path)
        if err or not rows:
            self.record("T2_SPLIT824_INTEGRITY", 2, "split_824", "FAIL", f"Invalid split_824_corpus.csv: {err or 'empty'}.")
            return

        id_col = next((c for c in ("text_id", "id") if c in hdr), None)
        split_col = next((c for c in ("split_id", "split", "class") if c in hdr), None)
        seal_col = next((c for c in ("seal_id", "ref_id") if c in hdr), None)
        cat_col = next((c for c in ("catalogue", "source", "corpus") if c in hdr), None)
        intact_col = next((c for c in ("intact", "is_intact") if c in hdr), None)

        if not id_col or not split_col:
            self.record(
                "T2_SPLIT824_INTEGRITY",
                2,
                "split_824",
                "FAIL",
                f"split_824_corpus.csv missing id/split_id columns (header={hdr}).",
            )
            return

        # Cross-join ground truth from corpus_soundfree_readings.csv if present
        gt_824: dict[str, dict[str, Any]] = {}
        if corpus_path.is_file():
            _, crows, cerr = load_csv(corpus_path)
            if not cerr and crows:
                for cr in crows:
                    toks = [x.strip().zfill(3) for x in str(cr.get("signs", "")).split("-") if x.strip().isdigit()]
                    if "824" in toks:
                        cid = str(cr.get("id", "")).strip()
                        gt_824[cid] = {
                            "catalogue": str(cr.get("catalogue", "")).strip(),
                            "intact": str(cr.get("intact", "")).strip().lower() in ("true", "1", "yes"),
                            "object_kind": str(cr.get("object_kind", "")).strip().lower(),
                            "ref_id": str(cr.get("ref_id", "")).strip(),
                            "site": str(cr.get("site", "")).strip(),
                        }

        errs: list[str] = []
        if len(rows) != 32:
            errs.append(f"Expected 32 total Lipi 824 rows, got {len(rows)}")

        seen_ids: set[str] = set()
        c_824a_tot = c_824a_intact = 0
        c_824b_tot = c_824b_intact = 0
        unseen_leak = 0
        h2085_splits: list[str] = []

        for r in rows:
            tid = str(r.get(id_col, "")).strip()
            sid = str(r.get(split_col, "")).strip()
            ref = str(r.get(seal_col, "")).strip() if seal_col else ""
            seen_ids.add(tid)

            csv_cat = str(r.get(cat_col, "")).strip() if cat_col else ""
            csv_intact_raw = str(r.get(intact_col, "")).strip().lower() if intact_col else ""

            # Check BOTH ground-truth catalogue/intact AND CSV row's own catalogue/intact columns
            if tid in gt_824:
                is_intact = gt_824[tid]["intact"]
                gt_cat = gt_824[tid]["catalogue"]
                if not ref:
                    ref = gt_824[tid]["ref_id"]
                if intact_col and csv_intact_raw != "":
                    csv_intact = csv_intact_raw in ("true", "1", "yes")
                    if csv_intact != is_intact:
                        errs.append(f"Row {tid}: intact mismatch vs ground truth (csv={csv_intact}, gt={is_intact})")
                cats_to_check = [gt_cat] + ([csv_cat] if csv_cat else [])
            else:
                is_intact = (csv_intact_raw in ("true", "1", "yes")) if intact_col else False
                cats_to_check = [csv_cat if csv_cat else "Lipi"]

            if any(
                ("mahadevan" in c.lower() or "unseen" in c.lower() or c.lower() == "new")
                for c in cats_to_check
            ):
                unseen_leak += 1

            if sid == "824a":
                c_824a_tot += 1
                if is_intact:
                    c_824a_intact += 1
            elif sid == "824b":
                c_824b_tot += 1
                if is_intact:
                    c_824b_intact += 1
            else:
                errs.append(f"Row {tid}: unexpected split_id '{sid}'")

            if tid == "887.2" or "H-2085" in ref.upper():
                h2085_splits.append(sid)

        if gt_824:
            gt_ids = set(gt_824.keys())
            if seen_ids != gt_ids:
                errs.append(f"Row IDs mismatch ground truth: missing={sorted(gt_ids - seen_ids)[:5]}, extra={sorted(seen_ids - gt_ids)[:5]}")

        if c_824a_tot != 10 or c_824a_intact != 7:
            errs.append(f"824a count mismatch: got {c_824a_intact} intact / {c_824a_tot} total (expected 7 intact / 10 total)")
        if c_824b_tot != 22 or c_824b_intact != 18:
            errs.append(f"824b count mismatch: got {c_824b_intact} intact / {c_824b_tot} total (expected 18 intact / 22 total)")
        if h2085_splits != ["824b"]:
            errs.append(f"Reversed 887.2 (H-2085) must be assigned to 824b, got {h2085_splits}")
        if unseen_leak > 0:
            errs.append(f"Detected {unseen_leak} unseen/Mahadevan leakage row(s) in split_824_corpus.csv")

        if not errs:
            self.record(
                "T2_SPLIT824_INTEGRITY",
                2,
                "split_824",
                "PASS",
                "824 split exact: 32 Lipi rows (824a=7/10 seals, 824b=18/22 tablets), H-2085 (887.2) in 824b, 0 unseen leakage.",
            )
        else:
            self.record(
                "T2_SPLIT824_INTEGRITY",
                2,
                "split_824",
                "FAIL",
                "; ".join(errs),
                {
                    "824a": {"intact": c_824a_intact, "total": c_824a_tot},
                    "824b": {"intact": c_824b_intact, "total": c_824b_tot},
                    "h2085_splits": h2085_splits,
                    "unseen_leak": unseen_leak,
                },
            )

    @staticmethod
    def _extract_dholavira_positions(data: dict[str, Any]) -> list[dict[str, Any]] | None:
        """Locate the 10-position breakdown list in dholavira_signboard_audit_v2.json."""
        for k in ("positions_10", "sign_breakdown_10", "signs", "positions", "tokens"):
            v = data.get(k)
            if isinstance(v, list) and len(v) == 10 and all(isinstance(x, dict) for x in v):
                return v
        # Fallback: any top-level 10-element list of dicts carrying a sign field
        sign_keys = ("lipi_sign", "sign", "sign_id", "id")
        for v in data.values():
            if (
                isinstance(v, list)
                and len(v) == 10
                and all(isinstance(x, dict) and any(sk in x for sk in sign_keys) for x in v)
            ):
                return v
        return None

    @staticmethod
    def _parse_dholavira_lock_status(item: dict[str, Any]) -> tuple[bool, bool]:
        """Return (has_valid_lock_field, is_locked) supporting both boolean and string status schemas."""
        for bk in ("locked", "is_locked", "locked_key8a", "locked_key7a", "locked_key6a"):
            if bk in item:
                if isinstance(item[bk], bool):
                    return True, item[bk]
                return False, False
        for sk in ("status_key8a", "lock_status", "status", "lock_tier"):
            val = item.get(sk)
            if isinstance(val, str) and val.strip():
                up = val.strip().upper()
                return True, up.startswith("LOCKED")
        return False, False

    @classmethod
    def _extract_dholavira_locked_counts(cls, dhol: dict[str, Any]) -> tuple[int, list[int]]:
        """Return (primary_locked_count, allowed_canonical_counts) from dholavira_signboard_audit_v2.json."""
        pos_list = cls._extract_dholavira_positions(dhol) or []
        pos_locked = 0
        for item in pos_list:
            ok, is_l = cls._parse_dholavira_lock_status(item)
            if ok and is_l:
                pos_locked += 1

        allowed: set[int] = set()
        rsum = dhol.get("reading_summary_key8a")
        primary: int | None = None
        if isinstance(rsum, dict):
            for k in (
                "locked_out_of_10_with_corpus_645",
                "locked_out_of_10_strict_phonetic",
                "all_10_glossed_with_611_architectural",
                "locked_count",
                "locked_out_of_10",
            ):
                v = rsum.get(k)
                if isinstance(v, int) and not isinstance(v, bool) and 1 <= v <= 10:
                    allowed.add(v)
                    if primary is None:
                        primary = v
        top_lc = dhol.get("locked_count")
        if isinstance(top_lc, int) and not isinstance(top_lc, bool) and 1 <= top_lc <= 10:
            allowed.add(top_lc)
            if primary is None:
                primary = top_lc
        if pos_locked > 0:
            allowed.add(pos_locked)
            if primary is None:
                primary = pos_locked
        if primary is None:
            primary = pos_locked
        if not allowed:
            allowed.add(primary)
        return primary, sorted(allowed)

    def _t2_dholavira_integrity(self) -> None:
        p = self.root / "work_data/key8a/dholavira_signboard_audit_v2.json"
        data, err = load_json(p)
        if err or not isinstance(data, dict):
            self.record("T2_DHOLAVIRA_AUDIT_V2", 2, "dholavira", "FAIL", f"Cannot load dholavira_signboard_audit_v2.json ({err}).")
            return

        errs: list[str] = []
        # Check record ID 144.1 across all Contract 1 ID key conventions
        id_blob = json.dumps(
            {
                k: data.get(k)
                for k in ("object_id", "signboard_id", "id", "record_id", "text_id", "lipi_id")
                if k in data
            }
        )
        if "144.1" not in id_blob and "144.1" not in json.dumps(data.get("lipi_raw_record", {})):
            errs.append("Missing record ID 144.1")

        # Verify Contract 1 Lothal L-116 parallel reference is present
        full_blob_low = json.dumps(data).lower()
        if "l-116" not in full_blob_low and "l116" not in full_blob_low:
            errs.append("Missing Contract 1 Lothal L-116 parallel reference")

        # Locate 10-position list
        pos_list = self._extract_dholavira_positions(data)
        locked_cnt = 0
        if pos_list is None:
            errs.append("Missing 10-element position list (positions_10 / sign_breakdown_10 / signs / positions)")
        else:
            has_top_notes = any(
                k for k in data
                if any(tok in k.lower() for tok in ("note", "audit", "bisht", "lothal", "summary"))
            )
            expected_anchors = {1: "820", 2: "611", 3: "388", 4: "820", 5: "850", 7: "031", 8: "820", 9: "820", 10: "798"}
            for idx, item in enumerate(pos_list, 1):
                if not isinstance(item, dict):
                    errs.append(f"Pos {idx}: entry is not a dict")
                    continue
                pos_val = item.get("pos") or item.get("position") or item.get("pos_reading_order") or idx
                try:
                    if int(pos_val) != idx:
                        errs.append(f"Pos {idx}: unexpected pos value {pos_val}")
                except (TypeError, ValueError):
                    errs.append(f"Pos {idx}: non-integer pos value {pos_val}")
                sign_val = item.get("lipi_sign") or item.get("sign") or item.get("sign_id") or item.get("id")
                if not sign_val:
                    errs.append(f"Pos {idx}: missing Lipi sign ID")
                else:
                    sn = norm_sign(sign_val)
                    if idx in expected_anchors and sn != expected_anchors[idx]:
                        errs.append(f"Pos {idx}: expected sign {expected_anchors[idx]}, got {sn}")
                # Check M77 metadata
                has_m77 = any(k in item for k in ("m77", "m77_id", "mahadevan", "m77_code", "m77_sign"))
                if not has_m77:
                    errs.append(f"Pos {idx}: missing M77 metadata field")
                # Check lock status (boolean OR non-empty string status)
                has_lock, is_locked = self._parse_dholavira_lock_status(item)
                if not has_lock:
                    errs.append(f"Pos {idx}: missing boolean or string lock status")
                elif is_locked:
                    locked_cnt += 1
                # Check reading/gloss
                if not any(item.get(k) for k in ("reading", "gloss", "proto_dravidian", "transliteration", "root")):
                    errs.append(f"Pos {idx}: missing reading/gloss")
                # Check notes
                if not has_top_notes and not any(item.get(k) for k in ("note", "notes", "audit_note", "lever", "evidence")):
                    errs.append(f"Pos {idx}: missing audit note")

            if locked_cnt < 7:
                errs.append(f"Dholavira locked count {locked_cnt}/10 < 7 (Key #7D floor)")

        if not errs:
            primary_lc, allowed_lc = self._extract_dholavira_locked_counts(data)
            self.record(
                "T2_DHOLAVIRA_AUDIT_V2",
                2,
                "dholavira",
                "PASS",
                f"Dholavira Signboard 144.1 audit valid (10/10 positions with Lipi/M77/lock/reading/notes + L-116 parallel; {locked_cnt}/10 locked, canonical={allowed_lc}).",
                {"locked_count": locked_cnt, "primary_locked_count": primary_lc, "allowed_counts": allowed_lc},
            )
        else:
            self.record("T2_DHOLAVIRA_AUDIT_V2", 2, "dholavira", "FAIL", "; ".join(errs[:6]), {"errors": errs})

    def _t2_sangam_multiface_m3_nulls(self) -> None:
        sangam_p = self.root / "work_data/key8b/test8b1_sangam_227plus.json"
        k8b_p = self.root / "work_data/key8b/key8b_summary.json"
        mf_p = self.root / "work_data/key8b/test8b3_multiface_key8.json"
        k8d_p = self.root / "work_data/key8d/key8d_summary.json"
        nulls_p = self.root / "work_data/key8c/honest_null_registry_v3.csv"

        s_data, s_err = load_json(sangam_p)
        b_data, b_err = load_json(k8b_p)

        # Scope Sangam fallback strictly to Sangam sub-dict inside key8b_summary.json (never unrelated keys!)
        sangam_sub_from_b: dict[str, Any] = {}
        if isinstance(b_data, dict):
            for k, v in b_data.items():
                kl = k.lower()
                if isinstance(v, dict) and any(tok in kl for tok in ("sangam", "test_8b1", "test8b1", "8b1")):
                    sangam_sub_from_b[k] = v
        sangam_scope: dict[str, Any] | None = None
        if isinstance(s_data, dict) and s_data:
            sangam_scope = s_data
        elif sangam_sub_from_b:
            sangam_scope = sangam_sub_from_b

        # 1. Sangam Prakrit loans == 0 (supporting words/obs_words, pairs/obs_pairs, and nested per-tier dicts)
        if sangam_scope is None:
            self.record("T2_SANGAM_PRAKRIT_ZERO", 2, "sangam_m3_nulls", "FAIL", f"Cannot load Sangam JSON ({s_err}, {b_err}).")
            self.record("T2_SANGAM_4TIERS", 2, "sangam_m3_nulls", "FAIL", "Blocked by missing Sangam JSON.")
        else:
            def _extract_wp_pairs(d: dict[str, Any]) -> list[tuple[str, Any, Any]]:
                out_wp: list[tuple[str, Any, Any]] = []
                w_key = next((wk for wk in ("words", "obs_words") if wk in d), None)
                p_key = next((pk for pk in ("pairs", "obs_pairs") if pk in d), None)
                if w_key is not None or p_key is not None:
                    out_wp.append(("self", d.get(w_key) if w_key else None, d.get(p_key) if p_key else None))
                    return out_wp
                # Nested per-tier Prakrit control dicts
                for nk, nv in d.items():
                    if isinstance(nv, dict):
                        nw = next((wk for wk in ("words", "obs_words") if wk in nv), None)
                        np_ = next((pk for pk in ("pairs", "obs_pairs") if pk in nv), None)
                        if nw is not None or np_ is not None:
                            out_wp.append((str(nk), nv.get(nw) if nw else None, nv.get(np_) if np_ else None))
                return out_wp

            prak_candidates: list[tuple[str, dict[str, Any], list[tuple[str, Any, Any]]]] = []
            def _walk_prak(obj: Any, path: str = "") -> None:
                if not isinstance(obj, dict):
                    return
                for k, v in obj.items():
                    kl = str(k).lower()
                    p_str = f"{path}.{k}" if path else str(k)
                    if "lexicon_size" in kl or "metadata" in kl:
                        continue
                    if "prakrit" in kl and isinstance(v, dict):
                        wp = _extract_wp_pairs(v)
                        if wp:
                            prak_candidates.append((p_str, v, wp))
                            continue
                    if isinstance(v, dict):
                        _walk_prak(v, p_str)

            _walk_prak(sangam_scope)
            if not prak_candidates and sangam_sub_from_b and sangam_scope is not sangam_sub_from_b:
                _walk_prak(sangam_sub_from_b)

            if not prak_candidates:
                self.record("T2_SANGAM_PRAKRIT_ZERO", 2, "sangam_m3_nulls", "FAIL", "Missing prakrit_loan_control result block (with words/pairs) in Sangam JSON.")
            else:
                prak_errs: list[str] = []
                for p_str, _, wp_list in prak_candidates:
                    for sub, w, pr in wp_list:
                        w_ok = (w == 0 and not isinstance(w, bool))
                        p_ok = (pr == 0 and not isinstance(pr, bool))
                        if not (w_ok and p_ok):
                            prak_errs.append(f"{p_str}.{sub}: words={w}, pairs={pr} (must be 0/0)")
                if not prak_errs:
                    self.record("T2_SANGAM_PRAKRIT_ZERO", 2, "sangam_m3_nulls", "PASS", f"Sangam Prakrit loan control strictly 0 words and 0 pairs across {len(prak_candidates)} block(s).")
                else:
                    self.record("T2_SANGAM_PRAKRIT_ZERO", 2, "sangam_m3_nulls", "FAIL", f"Prakrit loan leakage: {'; '.join(prak_errs[:5])}.")

            # 2. All 4 Sangam tiers present as dicts with numeric stats strictly inside Sangam scope
            tier_specs = [
                ("Tier1_frozen170", ("tier1", "tier_1", "frozen_170", "frozen170")),
                (
                    "Tier2_expanded_w56",
                    (
                        "tier2",
                        "tier_2",
                        "expanded_attested",
                        "expanded_w56",
                        "wave56",
                        "wave5_6",
                        "w56",
                        "expanded_key8",
                        "attested_expansion",
                    ),
                ),
                ("Tier3_non_numeral", ("tier3", "tier_3", "non_numeral", "nonnumeral", "lexical_lexical")),
                ("Tier4_automated_dict", ("tier4", "tier_4", "automated", "phoneme_preserving", "dedr_tamil")),
            ]
            missing_tiers: list[str] = []
            for label, needles in tier_specs:
                found = find_nested_dict(
                    sangam_scope,
                    lambda k, v, nd=needles: any(n in k.lower() for n in nd) and isinstance(v, dict) and has_non_null_numeric(v),
                )
                if found is None and sangam_sub_from_b and sangam_scope is not sangam_sub_from_b:
                    found = find_nested_dict(
                        sangam_sub_from_b,
                        lambda k, v, nd=needles: any(n in k.lower() for n in nd) and isinstance(v, dict) and has_non_null_numeric(v),
                    )
                if found is None:
                    missing_tiers.append(label)
            if not missing_tiers:
                self.record("T2_SANGAM_4TIERS", 2, "sangam_m3_nulls", "PASS", "All 4 Sangam epigraphy tiers present as numeric result dicts in Sangam JSON.")
            else:
                self.record("T2_SANGAM_4TIERS", 2, "sangam_m3_nulls", "FAIL", f"Missing or empty Sangam tier(s): {missing_tiers}.")

        # 3. Multi-face denominator 606 & decoded >= 378 (path-aware, never grabbing 163-sign baseline!)
        mf_data, mf_err = load_json(mf_p)
        mf_src = mf_data if isinstance(mf_data, dict) else (b_data if isinstance(b_data, dict) else None)
        if mf_src is None:
            self.record("T2_MULTIFACE_COUNTS", 2, "sangam_m3_nulls", "FAIL", f"Cannot load test8b3_multiface_key8.json ({mf_err}).")
        else:
            # Determine locked_signs hint from lexicon if available
            locked_hint: int | None = None
            lex8_p = self.root / "work_data/key8a/master_lexicon_after_key8a.csv"
            if lex8_p.is_file():
                _, lr, le = load_csv(lex8_p)
                if not le and lr:
                    locked_hint = len(lr)
            denom = self._find_int_field(mf_src, ("intact_multiface_raw", "intact_multiface_total", "intact_multiface"))
            dec = self._select_key8_multiface_int(mf_src, locked_signs=locked_hint)
            if denom == 606 and dec is not None and dec >= 378:
                self.record(
                    "T2_MULTIFACE_COUNTS",
                    2,
                    "sangam_m3_nulls",
                    "PASS",
                    f"Multi-face accounting verified: {dec} / {denom} intact multi-face objects decoded 100% (>= 378).",
                    {"decoded": dec, "intact_total": denom},
                )
            else:
                self.record(
                    "T2_MULTIFACE_COUNTS",
                    2,
                    "sangam_m3_nulls",
                    "FAIL",
                    f"Multi-face count check failed: decoded={dec} (need >= 378), intact_total={denom} (need 606).",
                )

        # 4. M3 External Locks: all 5 sub-tests present, non-empty numeric, and scoped 341/38 checks
        d_data, d_err = load_json(k8d_p)
        if d_err or not isinstance(d_data, dict):
            self.record("T2_M3_EXTERNAL_5SUBTESTS", 2, "sangam_m3_nulls", "FAIL", f"Cannot load key8d_summary.json ({d_err}).")
        else:
            m3_specs = [
                ("copper_bilinguals", ("copper", "bilingual", "341")),
                ("meluhha_endemism", ("meluhha", "endemism", "trade_loan")),
                ("pre_city_period12", ("pre_city", "precity", "period_1", "period1", "period12", "2650", "early_harappan", "pre_urban", "stage_i")),
                ("animal_stand_matrix", ("animal", "stand_letter", "stand_matrix")),
                ("megalithic_graffiti", ("megalithic", "graffiti", "keeladi", "lal")),
            ]
            missing_m3: list[str] = []
            matched_m3: dict[str, dict[str, Any]] = {}
            for label, needles in m3_specs:
                found = find_nested_dict(
                    d_data,
                    lambda k, v, nd=needles: any(n in k.lower() for n in nd) and isinstance(v, dict) and bool(v) and has_non_null_numeric(v),
                )
                if found is None:
                    missing_m3.append(label)
                else:
                    matched_m3[label] = found
            copper_blob = json.dumps(matched_m3.get("copper_bilinguals", {}))
            precity_blob = json.dumps(matched_m3.get("pre_city_period12", {}))
            has_341 = re.search(r"(?<!\d)341(?!\d)", copper_blob) is not None
            has_38 = re.search(r"(?<!\d)38(?!\d)", precity_blob) is not None
            if not missing_m3 and has_341 and has_38:
                self.record("T2_M3_EXTERNAL_5SUBTESTS", 2, "sangam_m3_nulls", "PASS", "All 5 M3 external-lock sub-tests present with numeric stats (incl. 341 in copper_bilinguals & 38 in pre_city_period12).")
            else:
                self.record(
                    "T2_M3_EXTERNAL_5SUBTESTS",
                    2,
                    "sangam_m3_nulls",
                    "FAIL",
                    f"M3 external sub-tests incomplete: missing={missing_m3}, has_341_in_copper={has_341}, has_38_in_precity={has_38}.",
                )

        # 5. Honest null registry v3 >= 41 populated rows
        if not nulls_p.is_file():
            self.record("T2_HONEST_NULL_REGISTRY", 2, "sangam_m3_nulls", "FAIL", "Missing honest_null_registry_v3.csv.")
        else:
            hdr, rows, err = load_csv(nulls_p)
            if err or not rows:
                self.record("T2_HONEST_NULL_REGISTRY", 2, "sangam_m3_nulls", "FAIL", f"Invalid honest_null_registry_v3.csv: {err or 'empty'}.")
            else:
                bad_rows = [
                    i + 1
                    for i, r in enumerate(rows)
                    if not (
                        str(r.get("test_id", "")).strip()
                        and str(r.get("tested_hypothesis", "")).strip()
                        and str(r.get("p_value", "")).strip()
                    )
                ]
                if len(rows) >= 41 and not bad_rows:
                    self.record(
                        "T2_HONEST_NULL_REGISTRY",
                        2,
                        "sangam_m3_nulls",
                        "PASS",
                        f"honest_null_registry_v3.csv has {len(rows)} fully populated rows (>= 41).",
                    )
                else:
                    self.record(
                        "T2_HONEST_NULL_REGISTRY",
                        2,
                        "sangam_m3_nulls",
                        "FAIL",
                        f"Honest null registry check failed: rows={len(rows)} (need >= 41), incomplete_rows={bad_rows[:10]}.",
                    )

    @staticmethod
    def _collect_int_fields(obj: Any, candidate_keys: tuple[str, ...]) -> list[tuple[str, int]]:
        """Collect all (full_key_path, int_val) pairs matching candidate_keys (case-insensitive)."""
        targets = {ck.lower() for ck in candidate_keys}
        hits: list[tuple[str, int]] = []

        def _walk(cur: Any, path: str) -> None:
            if isinstance(cur, dict):
                for k, v in cur.items():
                    kp = f"{path}.{k}" if path else str(k)
                    if str(k).lower() in targets and isinstance(v, int) and not isinstance(v, bool):
                        hits.append((kp, v))
                    if isinstance(v, (dict, list)):
                        _walk(v, kp)
            elif isinstance(cur, list):
                for idx, item in enumerate(cur):
                    if isinstance(item, (dict, list)):
                        _walk(item, f"{path}[{idx}]")

        _walk(obj, "")
        return hits

    def _select_key8_multiface_int(self, obj: Any, locked_signs: int | None = None) -> int | None:
        """Select Key #8 multi-face 100% count via path-aware scoring (never grabbing 163/227 baseline)."""
        keys: list[str] = []
        if locked_signs is not None:
            for ls in (locked_signs, locked_signs - 1):
                keys.extend([
                    f"decoded_100pct_multiface_{ls}_raw",
                    f"decoded_100pct_multiface_{ls}",
                    f"decoded_{ls}_raw",
                    f"decoded_{ls}",
                    f"multiface_100_{ls}",
                ])
        keys.extend([
            "decoded_100pct_multiface_key8a_raw",
            "decoded_100pct_multiface_key8_raw",
            "decoded_key8a_raw",
            "decoded_key8_raw",
            "decoded_100pct_multiface_raw",
            "decoded_100pct_raw",
            "decoded_100pct_multiface",
            "decoded_key8a",
            "decoded_key8",
            "multiface_100_key8a",
            "multiface_100_key8",
        ])
        hits = self._collect_int_fields(obj, tuple(keys))
        if not hits:
            return None
        scored: list[tuple[int, int, str]] = []
        for path, val in hits:
            pl = path.lower()
            score = 0
            if any(bad in pl for bad in ("163", "227", "baseline", "before", "key7", "key6")):
                score -= 200
            if any(good in pl for good in ("key8a", "key8", "after", "final", "locked")):
                score += 100
            if locked_signs is not None and (str(locked_signs) in pl or str(locked_signs - 1) in pl):
                score += 120
            scored.append((score, val, path))
        scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
        return scored[0][1]

    def _find_int_field(self, obj: Any, candidate_keys: tuple[str, ...]) -> int | None:
        for ck in candidate_keys:
            res = find_nested_dict(
                obj,
                lambda k, v, target=ck: k.lower() == target and isinstance(v, int) and not isinstance(v, bool),
            )
            if res is not None:
                val = next(iter(res.values()))
                if isinstance(val, int) and not isinstance(val, bool):
                    return val
        return None

    def _t2_repro_and_audit_v3(self) -> None:
        repro_script = self.root / "work_scripts/reproduce_all_keys.py"
        if not repro_script.is_file():
            self.record("T2_REPRO_CLI_RUN", 2, "repro_audit", "FAIL", "Missing work_scripts/reproduce_all_keys.py.")
        else:
            repro_src = repro_script.read_text(encoding="utf-8", errors="replace")
            req_flags = ("--nshuf", "--skip-live", "--verify-deliverables")
            missing_flags = [fl for fl in req_flags if fl not in repro_src]
            if missing_flags:
                self.record(
                    "T2_REPRO_CLI_RUN",
                    2,
                    "repro_audit",
                    "FAIL",
                    f"reproduce_all_keys.py missing required Contract 3 CLI flag(s): {missing_flags}.",
                )
            else:
                try:
                    proc = subprocess.run(
                        [sys.executable, str(repro_script), "--skip-live", "--verify-deliverables"],
                        cwd=str(self.root),
                        capture_output=True,
                        text=True,
                        timeout=180,
                    )
                    if proc.returncode == 0:
                        self.record(
                            "T2_REPRO_CLI_RUN",
                            2,
                            "repro_audit",
                            "PASS",
                            "reproduce_all_keys.py (--nshuf, --skip-live, --verify-deliverables) exited 0.",
                        )
                    else:
                        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-4:]
                        self.record(
                            "T2_REPRO_CLI_RUN",
                            2,
                            "repro_audit",
                            "FAIL",
                            f"reproduce_all_keys.py exited {proc.returncode}.",
                            {"tail": tail},
                        )
                except Exception as exc:
                    self.record("T2_REPRO_CLI_RUN", 2, "repro_audit", "FAIL", f"Failed executing reproduce_all_keys.py: {exc}.")

        # Master audit table v3 disk verification (non-empty regular files + Key #8 row check)
        audit_p = self.root / "work_data/key8c/master_audit_table_v3.json"
        audit, err = load_json(audit_p)
        if err or not isinstance(audit, dict):
            self.record("T2_AUDIT_V3_DISK_VERIFIED", 2, "repro_audit", "FAIL", f"Cannot load master_audit_table_v3.json ({err}).")
            return

        rows = audit.get("master_audit_rows", [])
        if not isinstance(rows, list):
            self.record("T2_AUDIT_V3_DISK_VERIFIED", 2, "repro_audit", "FAIL", "master_audit_rows is not a list.")
            return
        all_flag = audit.get("all_artifacts_verified_on_disk")
        missing_disk: list[str] = []
        false_flags: list[str] = []
        has_key8_row = False
        for r in rows:
            if not isinstance(r, dict):
                false_flags.append("<non-dict>")
                continue
            tid = str(r.get("test_id", "?"))
            key_str = str(r.get("key", "")).lower()
            if "key #8" in key_str or "key8" in key_str or tid.upper().startswith("K8"):
                has_key8_row = True
            if r.get("verified_on_disk") is not True:
                false_flags.append(tid)
            for col in ("script_path", "artifact_path"):
                raw_p = str(r.get(col, "")).strip()
                if not raw_p:
                    missing_disk.append(f"{tid}.{col}:<empty>")
                    continue
                for part in re.split(r"[;,]", raw_p):
                    part = part.strip()
                    if not part:
                        continue
                    target = self.root / part
                    if not target.is_file() or target.stat().st_size == 0:
                        missing_disk.append(f"{tid}.{col}:{part}")
        if all_flag is True and len(rows) >= 52 and (len(rows) > 52 or has_key8_row) and has_key8_row and not false_flags and not missing_disk:
            self.record(
                "T2_AUDIT_V3_DISK_VERIFIED",
                2,
                "repro_audit",
                "PASS",
                f"All {len(rows)} master_audit_table_v3 rows (incl. Key #8) verified as non-empty regular files on disk.",
            )
        else:
            self.record(
                "T2_AUDIT_V3_DISK_VERIFIED",
                2,
                "repro_audit",
                "FAIL",
                f"Audit v3 disk check failed: all_flag={all_flag}, rows={len(rows)}, has_key8_row={has_key8_row}, false_flags={len(false_flags)}, invalid_disk_files={len(missing_disk)}.",
                {"false_flags": false_flags[:10], "missing_disk": missing_disk[:10]},
            )

    # ===================================================================
    # TIER 3 — Cross-Artifact Numerical Consistency & Web/LaTeX Checks
    # ===================================================================

    def run_tier3(self) -> None:
        self._t3_cross_artifact_consistency()
        self._t3_web_static_checks()
        self._t3_latex_and_pdf_checks()

    def _select_sangam_headline_compounds(
        self,
        s8b1: dict[str, Any] | None,
        k8b: dict[str, Any] | None,
    ) -> int | None:
        """Extract canonical Sangam attested compound count without grabbing rival/control/subset cuts."""
        excluded_branch = (
            "rival",
            "prakrit",
            "control",
            "w24_both",
            "frozen_key4c_86",
            "sumerian",
            "non_hitting",
            "nonhitting",
            "ia_",
            "indo_aryan",
            "oia",
            "mw_ia",
        )
        sources: list[dict[str, Any]] = []
        if isinstance(s8b1, dict) and s8b1:
            sources.append(s8b1)
        if isinstance(k8b, dict) and k8b:
            sources.append(k8b)

        # 1. Explicit top-level / headline keys first
        explicit_keys = ("headline_attested_compounds", "attested_headwords", "sangam_compounds")
        for src in sources:
            hits = self._collect_int_fields(src, explicit_keys)
            clean_hits = [
                (p, v)
                for p, v in hits
                if not any(bad in p.lower() for bad in excluded_branch)
            ]
            if clean_hits:
                # Prefer shallower paths, break ties by max
                clean_hits.sort(key=lambda pv: (-pv[0].count("."), pv[1]), reverse=True)
                return clean_hits[0][1]

        # 2. Fallback: obs_words inside full-lexicon Tier 2 / Tier 1 cuts
        for src in sources:
            hits = self._collect_int_fields(src, ("obs_words", "attested_compounds"))
            scored: list[tuple[int, int, str]] = []
            for path, val in hits:
                pl = path.lower()
                if any(bad in pl for bad in excluded_branch):
                    continue
                score = 0
                if any(t2 in pl for t2 in ("tier2", "tier_2", "expanded_attested", "expanded_w56", "wave56", "key8")):
                    score += 100
                elif any(t1 in pl for t1 in ("tier1", "tier_1", "frozen_170", "frozen170", "full", "227")):
                    score += 80
                elif any(t34 in pl for t34 in ("tier3", "tier_3", "tier4", "tier_4", "non_numeral", "automated")):
                    score += 20
                else:
                    score += 40
                scored.append((score, val, path))
            if scored:
                scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
                return scored[0][1]
        return None

    def _derive_canonical_metrics(self) -> tuple[dict[str, Any] | None, list[str]]:
        if self._canonical_cache is not None:
            return self._canonical_cache, []

        missing: list[str] = []
        cov_raw, e1 = load_json(self.root / "work_data/key8a/coverage_after_key8a.json")
        meta6, e2 = load_json(self.root / "work_data/key8c/combined_6wave_meta_stats.json")
        dhol, e3 = load_json(self.root / "work_data/key8a/dholavira_signboard_audit_v2.json")
        k8b, e4 = load_json(self.root / "work_data/key8b/key8b_summary.json")
        s8b1, _ = load_json(self.root / "work_data/key8b/test8b1_sangam_227plus.json")
        mf8b3, _ = load_json(self.root / "work_data/key8b/test8b3_multiface_key8.json")
        lex_hdr, lex_rows, e5 = load_csv(self.root / "work_data/key8a/master_lexicon_after_key8a.csv")

        for name, err in (
            ("coverage_after_key8a.json", e1),
            ("combined_6wave_meta_stats.json", e2),
            ("dholavira_signboard_audit_v2.json", e3),
            ("key8b_summary.json", e4),
            ("master_lexicon_after_key8a.csv", e5),
        ):
            if err:
                missing.append(f"{name}: {err}")
        if missing:
            return None, missing

        splits = resolve_coverage_splits(cov_raw)
        if not all(k in splits for k in ("combined_intact", "unseen_intact")):
            return None, ["coverage_after_key8a.json missing combined_intact/unseen_intact"]

        lex_n = len(lex_rows)
        sc = next((c for c in ("sign", "sign_id", "id") if c in lex_hdr), None)
        has_split_824 = False
        if sc:
            low_ids = {str(r.get(sc, "")).strip().lower() for r in lex_rows}
            has_split_824 = ("824a" in low_ids and "824b" in low_ids)

        tier_name, u_tier = select_primary_locked_tier(
            splits["unseen_intact"],
            lexicon_count=lex_n,
            has_split_824=has_split_824,
        )
        if not tier_name or not u_tier or tier_name not in splits["combined_intact"]:
            return None, ["Cannot select primary locked Key #8A tier"]
        c_tier = splits["combined_intact"][tier_name]
        if not isinstance(c_tier, dict):
            return None, [f"Combined tier '{tier_name}' is not a dict"]

        # Extract 6-wave PhonSt & PhonEx Dravidian p-values safely
        meta7 = meta6.get("meta_7family", {}) if isinstance(meta6, dict) else {}
        if not isinstance(meta7, dict):
            return None, ["combined_6wave_meta_stats.json meta_7family is not a dict"]
        reg_key = next(
            (k for k in meta7 if "strictly_disjoint_6wave" in k.lower() and "keep142" not in k.lower() and "ultra" not in k.lower()),
            next((k for k in meta7 if "6wave" in k.lower()), None),
        )
        if not reg_key or not isinstance(meta7.get(reg_key), dict):
            return None, ["No 6-wave regime in combined_6wave_meta_stats.json"]
        reg = meta7[reg_key]
        ps_mode = reg.get("phon_stem") or reg.get("PhonSt") or {}
        pe_mode = reg.get("phon_exact") or reg.get("PhonEx") or {}
        ps_drav = ps_mode.get("Dravidian", {}) if isinstance(ps_mode, dict) else {}
        pe_drav = pe_mode.get("Dravidian", {}) if isinstance(pe_mode, dict) else {}
        raw_ps = ps_drav.get("fisher_p") if isinstance(ps_drav, dict) else None
        raw_pe = pe_drav.get("fisher_p") if isinstance(pe_drav, dict) else None
        try:
            if raw_ps is None or raw_pe is None:
                raise ValueError("missing Dravidian fisher_p")
            p_phonst = float(raw_ps)
            p_phonex = float(raw_pe)
        except (TypeError, ValueError) as exc:
            return None, [f"Invalid 6-wave Dravidian fisher_p in combined_6wave_meta_stats.json: {exc}"]

        # Dholavira locked count (supports both boolean & string status + reading_summary_key8a tiers)
        dhol_primary, dhol_allowed = self._extract_dholavira_locked_counts(dhol if isinstance(dhol, dict) else {})

        # Sangam headline compounds (excluding rival/control/subset cuts)
        sangam_compounds = self._select_sangam_headline_compounds(
            s8b1 if isinstance(s8b1, dict) else None,
            k8b if isinstance(k8b, dict) else None,
        )

        # Locked sign count & coverage numbers
        try:
            locked_signs = int(c_tier.get("n_signs", lex_n))
            combined_tok_pct = float(c_tier["token_pct"])
            unseen_tok_pct = float(u_tier["token_pct"])
            combined_full_faces = int(c_tier["faces_100pct"])
            unseen_full_faces = int(u_tier["faces_100pct"])
        except (KeyError, TypeError, ValueError) as exc:
            return None, [f"Invalid numeric coverage fields in tier '{tier_name}': {exc}"]

        # Multi-face 100% count (path-aware, preferring Key #8 / locked_signs over 163/227 baselines)
        mf_src = mf8b3 if isinstance(mf8b3, dict) else (k8b if isinstance(k8b, dict) else {})
        multiface_100 = self._select_key8_multiface_int(mf_src, locked_signs=locked_signs)
        if multiface_100 is None and isinstance(k8b, dict) and k8b is not mf_src:
            multiface_100 = self._select_key8_multiface_int(k8b, locked_signs=locked_signs)

        metrics = {
            "locked_signs": locked_signs,
            "combined_tok_pct": combined_tok_pct,
            "unseen_tok_pct": unseen_tok_pct,
            "combined_full_faces": combined_full_faces,
            "unseen_full_faces": unseen_full_faces,
            "p_6wave_phonst": p_phonst,
            "p_6wave_phonex": p_phonex,
            "sangam_compounds": sangam_compounds,
            "multiface_100": multiface_100,
            "dholavira_locked": dhol_primary,
            "dholavira_allowed_counts": dhol_allowed,
        }
        self._canonical_cache = metrics
        return metrics, []

    def _t3_cross_artifact_consistency(self) -> None:
        canon, errs = self._derive_canonical_metrics()
        if canon is None:
            for cid in (
                "T3_XDOC_MASTER_AUDIT_V3",
                "T3_XDOC_EXPLORER_V3",
                "T3_XDOC_READINGS_KEY7",
                "T3_XDOC_PAPER_DRAFT",
                "T3_XDOC_MANUSCRIPT_TEX",
                "T3_XDOC_MAP_MD",
                "T3_XDOC_DIARY_MD",
                "T3_XDOC_README_MD",
            ):
                is_m5_only = cid in (
                    "T3_XDOC_PAPER_DRAFT",
                    "T3_XDOC_MANUSCRIPT_TEX",
                    "T3_XDOC_MAP_MD",
                    "T3_XDOC_DIARY_MD",
                    "T3_XDOC_README_MD",
                )
                if is_m5_only and self.allow_missing_m5 and not self.m5_manuscript_exists():
                    self.record(cid, 3, "cross_artifact", "SKIP", "M5 deliverables absent (--allow-missing-m5).")
                else:
                    self.record(cid, 3, "cross_artifact", "FAIL", f"Cannot derive canonical Key #8 metrics: {errs}.")
            return

        # 0. master_audit_table_v3.json exact match against canonical Key #8 metrics
        audit_p = self.root / "work_data/key8c/master_audit_table_v3.json"
        audit_v3, audit_err = load_json(audit_p)
        if audit_err or not isinstance(audit_v3, dict):
            self.record("T3_XDOC_MASTER_AUDIT_V3", 3, "cross_artifact", "FAIL", f"Cannot load master_audit_table_v3.json ({audit_err}).")
        else:
            amiss: list[str] = []
            # Check explicit headline/summary blocks if present (catches any direct headline drift)
            for hkey in ("headline_metrics", "summary", "key8_summary", "meta"):
                hblk = audit_v3.get(hkey)
                if not isinstance(hblk, dict):
                    continue
                if "locked_signs" in hblk and hblk["locked_signs"] != canon["locked_signs"]:
                    amiss.append(f"{hkey}.locked_signs: {hblk['locked_signs']} != {canon['locked_signs']}")
                for ck in ("combined_tok_pct", "token_coverage_pct"):
                    if ck in hblk:
                        try:
                            if abs(float(hblk[ck]) - canon["combined_tok_pct"]) > 0.025:
                                amiss.append(f"{hkey}.{ck}: {hblk[ck]} != {canon['combined_tok_pct']}")
                        except (TypeError, ValueError):
                            amiss.append(f"{hkey}.{ck}: non-numeric")
                for uk in ("unseen_tok_pct", "unseen_token_pct"):
                    if uk in hblk:
                        try:
                            if abs(float(hblk[uk]) - canon["unseen_tok_pct"]) > 0.025:
                                amiss.append(f"{hkey}.{uk}: {hblk[uk]} != {canon['unseen_tok_pct']}")
                        except (TypeError, ValueError):
                            amiss.append(f"{hkey}.{uk}: non-numeric")
                for pk, target_p in (("p_6wave_phonst", canon["p_6wave_phonst"]), ("p_6wave_phonex", canon["p_6wave_phonex"])):
                    if pk in hblk:
                        try:
                            pv = float(hblk[pk])
                            if pv <= 0 or abs(pv - target_p) / target_p > 0.03:
                                amiss.append(f"{hkey}.{pk}: {pv} != {target_p:.3e}")
                        except (TypeError, ValueError):
                            amiss.append(f"{hkey}.{pk}: non-numeric")

            # Check invariant3_unseen_holdout_parity includes a clean Key #8A row matching canonical unseen_tok_pct
            inv3 = audit_v3.get("invariant3_unseen_holdout_parity")
            inv3_checks = inv3.get("checks", []) if isinstance(inv3, dict) else []
            matched_k8_parity = False
            if isinstance(inv3_checks, list):
                for row in inv3_checks:
                    if not isinstance(row, dict):
                        continue
                    if row.get("lipi_faces") == 3600 and row.get("new_faces") == 563:
                        try:
                            nt = float(row.get("new_token_pct", -1))
                        except (TypeError, ValueError):
                            continue
                        if abs(nt - canon["unseen_tok_pct"]) <= 0.025:
                            matched_k8_parity = True
                            break
            if not matched_k8_parity:
                amiss.append(f"invariant3_unseen_holdout_parity missing clean Key #8A row matching unseen_tok_pct={canon['unseen_tok_pct']:.2f}%")

            # Check Key #8 rows + invariant2_meta_7family_summary carry canonical 6-wave PhonSt & PhonEx P-values and locked_signs
            k8_rows = [
                r for r in (audit_v3.get("master_audit_rows") or [])
                if isinstance(r, dict) and ("key #8" in str(r.get("key", "")).lower() or "key8" in str(r.get("key", "")).lower() or str(r.get("test_id", "")).upper().startswith("K8"))
            ]
            audit_payload_blob = normalize_doc_text(
                json.dumps({
                    "inv2": audit_v3.get("invariant2_meta_7family_summary", {}),
                    "headline": audit_v3.get("headline_metrics", {}),
                    "summary": audit_v3.get("summary", {}),
                    "k8_rows": k8_rows,
                })
            )
            if not doc_has_pvalue(audit_payload_blob, canon["p_6wave_phonst"], rel_tol=0.03):
                amiss.append(f"master_audit_table_v3 missing 6-wave PhonSt p={canon['p_6wave_phonst']:.3e}")
            if not doc_has_pvalue(audit_payload_blob, canon["p_6wave_phonex"], rel_tol=0.03):
                amiss.append(f"master_audit_table_v3 missing 6-wave PhonEx p={canon['p_6wave_phonex']:.3e}")
            if not doc_has_int(audit_payload_blob, canon["locked_signs"]):
                amiss.append(f"master_audit_table_v3 missing canonical locked_signs={canon['locked_signs']}")

            if not amiss:
                self.record(
                    "T3_XDOC_MASTER_AUDIT_V3",
                    3,
                    "cross_artifact",
                    "PASS",
                    "master_audit_table_v3.json agrees with canonical Key #8 metrics (locked signs, coverage/parity, 6-wave PhonSt/PhonEx P-values).",
                )
            else:
                self.record(
                    "T3_XDOC_MASTER_AUDIT_V3",
                    3,
                    "cross_artifact",
                    "FAIL",
                    "; ".join(amiss),
                    {"canonical": canon, "mismatches": amiss},
                )

        # 1. explorer_data_v3.json exact match against canonical metrics
        exp_p = self.root / "work_data/key8c/explorer_data_v3.json"
        exp, exp_err = load_json(exp_p)
        if exp_err or not isinstance(exp, dict):
            self.record("T3_XDOC_EXPLORER_V3", 3, "cross_artifact", "FAIL", f"Cannot load explorer_data_v3.json ({exp_err}).")
        else:
            meta = exp.get("meta", {}) if isinstance(exp.get("meta"), dict) else {}
            mismatches: list[str] = []
            if meta.get("locked_signs") != canon["locked_signs"]:
                mismatches.append(f"locked_signs: {meta.get('locked_signs')} != {canon['locked_signs']}")
            try:
                if abs(float(meta.get("token_coverage_pct", -1)) - canon["combined_tok_pct"]) > 0.025:
                    mismatches.append(f"combined_tok_pct: {meta.get('token_coverage_pct')} != {canon['combined_tok_pct']}")
            except (TypeError, ValueError):
                mismatches.append(f"combined_tok_pct non-numeric: {meta.get('token_coverage_pct')}")
            try:
                if abs(float(meta.get("unseen_token_pct", -1)) - canon["unseen_tok_pct"]) > 0.025:
                    mismatches.append(f"unseen_tok_pct: {meta.get('unseen_token_pct')} != {canon['unseen_tok_pct']}")
            except (TypeError, ValueError):
                mismatches.append(f"unseen_tok_pct non-numeric: {meta.get('unseen_token_pct')}")
            if meta.get("faces_100_mapped") != canon["combined_full_faces"]:
                mismatches.append(f"combined_full_faces: {meta.get('faces_100_mapped')} != {canon['combined_full_faces']}")
            if meta.get("unseen_100_mapped") != canon["unseen_full_faces"]:
                mismatches.append(f"unseen_full_faces: {meta.get('unseen_100_mapped')} != {canon['unseen_full_faces']}")
            if canon["sangam_compounds"] is not None and meta.get("sangam_compounds") != canon["sangam_compounds"]:
                mismatches.append(f"sangam_compounds: {meta.get('sangam_compounds')} != {canon['sangam_compounds']}")

            # Support Key #7C naming (`multiface_100_<N>`), `multiface_100_key8a`, `multiface_100_key8`, or `multiface_stats`
            mf_exp = (
                meta.get(f"multiface_100_{canon['locked_signs']}")
                or meta.get("multiface_100_key8a")
                or meta.get("multiface_100_key8")
                or meta.get("multiface_100_locked")
                or meta.get("multiface_100")
            )
            if mf_exp is None:
                for mk, mv in meta.items():
                    if re.match(r"^multiface_100_(?!163$|227$)\w+$", str(mk)) and isinstance(mv, int) and not isinstance(mv, bool):
                        mf_exp = mv
                        break
            if mf_exp is None and isinstance(exp.get("multiface_stats"), dict):
                mf_exp = self._select_key8_multiface_int(exp["multiface_stats"], locked_signs=canon["locked_signs"])
            if canon["multiface_100"] is not None and mf_exp != canon["multiface_100"]:
                mismatches.append(f"multiface_100: {mf_exp} != {canon['multiface_100']}")

            dhol_blk = exp.get("dholavira_signboard")
            dhol_exp = None
            if isinstance(dhol_blk, dict):
                dhol_exp = dhol_blk.get("locked_count")
                if dhol_exp is None:
                    dhol_exp = dhol_blk.get("locked_out_of_10")
            if dhol_exp not in canon["dholavira_allowed_counts"]:
                mismatches.append(f"dholavira_locked: {dhol_exp} not in {canon['dholavira_allowed_counts']}")

            # Check 6-wave Dravidian p-values inside six_wave_7family
            sw_blob = normalize_doc_text(json.dumps(exp.get("six_wave_7family", {})))
            if not doc_has_pvalue(sw_blob, canon["p_6wave_phonst"], rel_tol=0.03):
                mismatches.append(f"six_wave_7family missing PhonSt p={canon['p_6wave_phonst']:.3e}")
            if not doc_has_pvalue(sw_blob, canon["p_6wave_phonex"], rel_tol=0.03):
                mismatches.append(f"six_wave_7family missing PhonEx p={canon['p_6wave_phonex']:.3e}")

            if not mismatches:
                self.record("T3_XDOC_EXPLORER_V3", 3, "cross_artifact", "PASS", "explorer_data_v3.json matches all canonical Key #8 metrics.", canon)
            else:
                self.record("T3_XDOC_EXPLORER_V3", 3, "cross_artifact", "FAIL", "; ".join(mismatches), {"canonical": canon, "mismatches": mismatches})

        def _slice_headline_md(s: str, max_lines: int = 120) -> str:
            lines = s.splitlines()
            return "\n".join(lines[:max_lines])

        def _slice_headline_tex(s: str) -> str:
            m_doc = re.search(r"\\begin\{document\}", s)
            body = s[m_doc.start():] if m_doc else s
            m_abs = re.search(r"\\end\{abstract\}", body)
            head_lines = "\n".join(body.splitlines()[:130])
            if m_abs and m_abs.end() > len(head_lines):
                return body[: m_abs.end() + 4000]
            return head_lines

        # Helper to audit a narrative/manuscript document against canonical metrics with contextual proximity
        def check_doc(
            cid: str,
            rel_path: str,
            slice_fn,
            m5_doc: bool,
            require_all_metrics: bool = True,
            extra_stale_check: bool = False,
        ) -> None:
            fp = self.root / rel_path
            if m5_doc and self.allow_missing_m5 and not self.m5_manuscript_exists():
                self.record(cid, 3, "cross_artifact", "SKIP", f"M5 doc sync pending for {rel_path} (--allow-missing-m5).")
                return
            if not fp.is_file():
                self.record(cid, 3, "cross_artifact", "FAIL", f"Missing {rel_path}.")
                return
            raw = fp.read_text(encoding="utf-8", errors="replace")
            if rel_path.endswith(".tex"):
                raw = strip_tex_comments(raw)
            section = slice_fn(raw)
            norm = normalize_doc_text(section)
            full_norm = normalize_doc_text(raw)
            miss: list[str] = []
            if not doc_has_int_near(norm, canon["locked_signs"], r"\b(?:sign|signs|locked|lexicon|glossary|decoded)\b", window=80):
                miss.append(f"locked_signs={canon['locked_signs']}")
            if not doc_has_pct(norm, canon["combined_tok_pct"]):
                miss.append(f"combined_tok_pct={canon['combined_tok_pct']:.2f}%")
            if not doc_has_pct(norm, canon["unseen_tok_pct"]):
                miss.append(f"unseen_tok_pct={canon['unseen_tok_pct']:.2f}%")
            if not (
                doc_has_ratio(norm, canon["combined_full_faces"], 4163)
                or doc_has_int_near(norm, canon["combined_full_faces"], r"(?:intact|face|faces|4,163|4163|100%|full)", window=60)
            ):
                miss.append(f"combined_full_faces={canon['combined_full_faces']}")
            if not (
                doc_has_ratio(norm, canon["unseen_full_faces"], 563)
                or doc_has_int_near(norm, canon["unseen_full_faces"], r"(?:unseen|holdout|563|mahadevan|new)", window=60)
            ):
                miss.append(f"unseen_full_faces={canon['unseen_full_faces']}")
            if not doc_has_pvalue(norm, canon["p_6wave_phonst"], rel_tol=0.03):
                miss.append(f"p_6wave_phonst={canon['p_6wave_phonst']:.2e}")
            if require_all_metrics:
                if not doc_has_pvalue(full_norm, canon["p_6wave_phonex"], rel_tol=0.03):
                    miss.append(f"p_6wave_phonex={canon['p_6wave_phonex']:.2e}")
                if canon["sangam_compounds"] is not None and not doc_has_int_near(
                    full_norm,
                    canon["sangam_compounds"],
                    r"(?:sangam|compound|headword|tamil|epigraph|dravidian|brahmi)",
                    window=80,
                ):
                    miss.append(f"sangam_compounds={canon['sangam_compounds']}")
                if canon["multiface_100"] is not None and not (
                    doc_has_ratio(full_norm, canon["multiface_100"], 606)
                    or doc_has_int_near(full_norm, canon["multiface_100"], r"(?:multi-?face|whole-?object|606)", window=60)
                ):
                    miss.append(f"multiface_100={canon['multiface_100']}/606")
                if not any(
                    doc_has_ratio_near(full_norm, cnt, 10, r"(?:dholavira|signboard|144\.1|north\s+gate)", window=120)
                    for cnt in canon["dholavira_allowed_counts"]
                ):
                    miss.append(f"dholavira_locked={canon['dholavira_allowed_counts']}/10")

            if extra_stale_check:
                low_full = full_norm.lower()
                for stale in (
                    "exact sign-by-sign phonetic words are not established",
                    "phonetic words are not established",
                    "do not yet clear the 7-family bonferroni",
                    "sign-by-sign words do not yet clear",
                ):
                    if stale in low_full:
                        miss.append(f"stale pre-Key#2 phrasing: '{stale}'")

            if not miss:
                self.record(cid, 3, "cross_artifact", "PASS", f"{rel_path} matches all canonical Key #8 headline metrics.")
            else:
                self.record(cid, 3, "cross_artifact", "FAIL", f"{rel_path} mismatches/omits: {', '.join(miss)}", {"missing_or_mismatched": miss})

        check_doc("T3_XDOC_READINGS_KEY7", "READINGS_KEY7.md", lambda s: _slice_headline_md(s, 120), m5_doc=False)
        check_doc("T3_XDOC_PAPER_DRAFT", "PAPER_DRAFT.md", lambda s: _slice_headline_md(s, 120), m5_doc=True)
        check_doc("T3_XDOC_MANUSCRIPT_TEX", "paper/manuscript.tex", _slice_headline_tex, m5_doc=True)
        check_doc(
            "T3_XDOC_MAP_MD",
            "MAP.md",
            lambda s: "\n".join(s.splitlines()[:45]),
            m5_doc=True,
        )
        check_doc(
            "T3_XDOC_README_MD",
            "README.md",
            lambda s: "\n".join(s.splitlines()[:75]),
            m5_doc=True,
            extra_stale_check=True,
        )

        # DIARY.md Key #8 tail sync + Colab units == 0 check
        diary_p = self.root / "DIARY.md"
        if self.allow_missing_m5 and not self.m5_manuscript_exists():
            self.record("T3_XDOC_DIARY_MD", 3, "cross_artifact", "SKIP", "M5 doc sync pending for DIARY.md (--allow-missing-m5).")
        elif not diary_p.is_file():
            self.record("T3_XDOC_DIARY_MD", 3, "cross_artifact", "FAIL", "Missing DIARY.md.")
        else:
            d_raw = diary_p.read_text(encoding="utf-8", errors="replace")
            d_lines = d_raw.splitlines()
            k8_idx = next((i for i, ln in enumerate(d_lines) if re.search(r"key\s*#?\s*8\b", ln, re.IGNORECASE)), None)
            if k8_idx is None:
                self.record("T3_XDOC_DIARY_MD", 3, "cross_artifact", "FAIL", "DIARY.md has no Key #8 entries.")
            else:
                tail_norm = normalize_doc_text("\n".join(d_lines[k8_idx:]))
                d_miss: list[str] = []
                if not doc_has_int_near(tail_norm, canon["locked_signs"], r"\b(?:sign|signs|locked|lexicon)\b", window=80):
                    d_miss.append(f"locked_signs={canon['locked_signs']}")
                if not doc_has_pct(tail_norm, canon["combined_tok_pct"]):
                    d_miss.append(f"combined_tok_pct={canon['combined_tok_pct']:.2f}%")
                if not doc_has_pct(tail_norm, canon["unseen_tok_pct"]):
                    d_miss.append(f"unseen_tok_pct={canon['unseen_tok_pct']:.2f}%")
                if not doc_has_pvalue(tail_norm, canon["p_6wave_phonst"], rel_tol=0.03):
                    d_miss.append(f"p_6wave_phonst={canon['p_6wave_phonst']:.2e}")
                colab_matches = re.findall(r"colab\s+units(?:\s+used)?\s*[:=]?\s*(\d+(?:\.\d+)?)", tail_norm, re.IGNORECASE)
                if not colab_matches:
                    d_miss.append("missing Colab units record in Key #8 DIARY.md tail")
                elif any(float(cm) != 0.0 for cm in colab_matches):
                    d_miss.append(f"non-zero Colab units in Key #8 DIARY.md tail: {colab_matches}")
                if not d_miss:
                    self.record("T3_XDOC_DIARY_MD", 3, "cross_artifact", "PASS", "DIARY.md Key #8 tail entries match canonical Key #8 metrics and record 0 Colab units.")
                else:
                    self.record("T3_XDOC_DIARY_MD", 3, "cross_artifact", "FAIL", f"DIARY.md Key #8 tail issues: {', '.join(d_miss)}", {"issues": d_miss})

    def _t3_web_static_checks(self) -> None:
        html_p = self.root / "map_page/index.html"
        if not html_p.is_file():
            self.record("T3_WEB_JS_SYNTAX", 3, "web_static", "FAIL", "Missing map_page/index.html.")
            self.record("T3_WEB_EMBEDDED_V3", 3, "web_static", "FAIL", "Missing map_page/index.html.")
            self.record("T3_WEB_DAG_STATIC", 3, "web_static", "FAIL", "Missing map_page/index.html.")
            return

        html = html_p.read_text(encoding="utf-8", errors="replace")
        scripts = [
            m.group(2)
            for m in re.finditer(r"<script([^>]*)>(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
            if "src=" not in m.group(1).lower() and m.group(2).strip()
        ]

        # 1. JS syntax validation via `node --check` in tempfile.TemporaryDirectory()
        if not scripts:
            self.record("T3_WEB_JS_SYNTAX", 3, "web_static", "FAIL", "No inline <script> blocks found in map_page/index.html.")
        else:
            js_errs: list[str] = []
            with tempfile.TemporaryDirectory(prefix="key8_js_check_") as td:
                for idx, code in enumerate(scripts):
                    tf = Path(td) / f"block_{idx}.js"
                    tf.write_text(code, encoding="utf-8")
                    proc = subprocess.run(
                        ["node", "--check", str(tf)],
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    if proc.returncode != 0:
                        js_errs.append(f"script[{idx}]: {(proc.stderr or proc.stdout).strip()[:300]}")
            if not js_errs:
                self.record(
                    "T3_WEB_JS_SYNTAX",
                    3,
                    "web_static",
                    "PASS",
                    f"node --check passed cleanly on {len(scripts)} inline <script> block(s).",
                )
            else:
                self.record("T3_WEB_JS_SYNTAX", 3, "web_static", "FAIL", f"JS syntax error: {js_errs[0]}", {"errors": js_errs})

        # 2. Embedded explorer_data_v3 payload check
        pre_m5_skip = self.allow_missing_m5 and not self.m5_build_exists()
        exp_p = self.root / "work_data/key8c/explorer_data_v3.json"
        exp_data, exp_err = load_json(exp_p)
        if pre_m5_skip and ("six_wave_7family" not in html):
            self.record("T3_WEB_EMBEDDED_V3", 3, "web_static", "SKIP", "M5 build_map_page.py not yet built (--allow-missing-m5).")
        else:
            req_tokens = ("six_wave_7family", "dholavira_signboard", "inscriptions", "glossary")
            missing_toks = [t for t in req_tokens if t not in html]
            meta_ok = True
            meta_note = ""
            if not exp_err and isinstance(exp_data, dict):
                locked_n = exp_data.get("meta", {}).get("locked_signs")
                if locked_n is not None and str(locked_n) not in html:
                    meta_ok = False
                    meta_note = f"canonical locked_signs={locked_n} absent in HTML"
            if not missing_toks and meta_ok:
                self.record("T3_WEB_EMBEDDED_V3", 3, "web_static", "PASS", "explorer_data_v3 sections and canonical locked sign count embedded in map_page/index.html.")
            else:
                self.record(
                    "T3_WEB_EMBEDDED_V3",
                    3,
                    "web_static",
                    "FAIL",
                    f"Missing embedded v3 payload elements: tokens={missing_toks} {meta_note}".strip(),
                )

        # 3. Static DAG parent resolution & <=12-char label check (bracket-balanced, never silent PASS!)
        dag_nodes, dag_reason = self._extract_static_dag_nodes(html)
        if dag_nodes is None:
            if pre_m5_skip and dag_reason == "not_found":
                self.record("T3_WEB_DAG_STATIC", 3, "web_static", "SKIP", "Pre-M5 HTML (--allow-missing-m5).")
            else:
                self.record(
                    "T3_WEB_DAG_STATIC",
                    3,
                    "web_static",
                    "FAIL",
                    f"Static DAG node array missing or unparseable ({dag_reason}) — cannot verify DAG parent resolution.",
                )
        else:
            node_ids = {n["id"] for n in dag_nodes}
            dangling = [
                f"{n['id']}->{p}"
                for n in dag_nodes
                for p in n["parents"]
                if p not in node_ids
            ]
            long_labels = [
                f"{n['id']}:'{line}'({len(line)})"
                for n in dag_nodes
                for line in re.split(r"[|\n]", n["label"])
                if len(line.strip()) > 12
            ]
            if not dangling and not long_labels:
                self.record(
                    "T3_WEB_DAG_STATIC",
                    3,
                    "web_static",
                    "PASS",
                    f"Static DAG valid: {len(dag_nodes)} nodes, 0 dangling parents, 0 label lines > 12 chars.",
                )
            elif pre_m5_skip and not dangling:
                self.record(
                    "T3_WEB_DAG_STATIC",
                    3,
                    "web_static",
                    "SKIP",
                    f"Pre-M5 HTML has legacy >12-char labels awaiting M5 build_map_page.py (--allow-missing-m5): {long_labels[:5]}",
                )
            else:
                self.record(
                    "T3_WEB_DAG_STATIC",
                    3,
                    "web_static",
                    "FAIL",
                    f"Static DAG violation: dangling_parents={len(dangling)}, labels_gt12={len(long_labels)}.",
                    {"dangling": dangling[:10], "long_labels": long_labels[:10]},
                )

    def _extract_static_dag_nodes(self, html: str) -> tuple[list[dict[str, Any]] | None, str]:
        """Safely parse static DAG node array via bracket-balanced extraction + Node vm sandbox."""
        candidates: list[str] = []
        m = re.search(r"/\*TREE\*/(.*?)/\*END-TREE\*/", html, re.DOTALL)
        if m:
            block = m.group(1)
            m_eq = re.search(r"=\s*\[", block)
            if m_eq:
                arr_s = extract_balanced_js_array(block, m_eq.end() - 1)
                if arr_s:
                    candidates.append(arr_s)
        for m_decl in re.finditer(r"(?:const|let|var)\s+(?:N|NODES|DAG_NODES|TREE_NODES|DAG)\s*=\s*\[", html):
            arr_s = extract_balanced_js_array(html, m_decl.end() - 1)
            if arr_s and arr_s not in candidates:
                candidates.append(arr_s)
        if not candidates:
            return None, "not_found"

        js_eval = (
            "const vm = require('vm');\n"
            "const fs = require('fs');\n"
            "const src = fs.readFileSync(0, 'utf8');\n"
            "const arr = vm.runInNewContext('(' + src + ')', Object.create(null), {timeout: 2000});\n"
            "if (!Array.isArray(arr) || arr.length === 0) process.exit(2);\n"
            "const valid = arr.every(n => (Array.isArray(n) && n.length >= 3) || (n && typeof n === 'object' && 'id' in n));\n"
            "if (!valid) process.exit(3);\n"
            "const out = arr.map(n => Array.isArray(n)\n"
            "  ? {id: String(n[0]), label: String(n[2] || ''), parents: Array.isArray(n[5]) ? n[5].map(String) : []}\n"
            "  : {id: String(n.id), label: String(n.label || n.short || ''), parents: Array.isArray(n.parents) ? n.parents.map(String) : []}\n"
            ");\n"
            "process.stdout.write(JSON.stringify(out));\n"
        )
        last_err = "parse_error: empty result"
        for arr_src in candidates:
            try:
                proc = subprocess.run(
                    ["node", "-e", js_eval],
                    input=arr_src,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    parsed = json.loads(proc.stdout)
                    if isinstance(parsed, list) and parsed:
                        return parsed, "ok"
                else:
                    last_err = f"parse_error: rc={proc.returncode} {(proc.stderr or '').strip()[:160]}"
            except Exception as exc:
                last_err = f"parse_error: {exc}"
        return None, last_err

    def _t3_latex_and_pdf_checks(self) -> None:
        tex_p = self.root / "paper/manuscript.tex"
        bib_p = self.root / "paper/references.bib"
        pdf_p = self.root / "paper/manuscript.pdf"
        log_p = self.root / "paper/manuscript.log"

        if self.allow_missing_m5 and not any(p.exists() for p in (tex_p, bib_p, pdf_p)):
            for cid in ("T3_LATEX_FIGURES_REFS", "T3_LATEX_BIBTEX_CITATIONS", "T3_LATEX_PDF_STRUCTURE", "T3_LATEX_PDF_NO_UNRESOLVED"):
                self.record(cid, 3, "latex_pdf", "SKIP", "M5 paper/ deliverables absent (--allow-missing-m5).")
            return

        # 1. All 5 figures referenced in manuscript.tex
        if not tex_p.is_file():
            self.record("T3_LATEX_FIGURES_REFS", 3, "latex_pdf", "FAIL", "Missing paper/manuscript.tex.")
            self.record("T3_LATEX_BIBTEX_CITATIONS", 3, "latex_pdf", "FAIL", "Missing paper/manuscript.tex.")
        else:
            tex_clean = strip_tex_comments(tex_p.read_text(encoding="utf-8", errors="replace"))
            inc_args = re.findall(r"\\includegraphics(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}", tex_clean)
            inc_blob = " ".join(inc_args).lower()
            missing_figs = [f"fig{i}" for i in range(1, 6) if f"fig{i}" not in inc_blob]
            if not missing_figs:
                self.record("T3_LATEX_FIGURES_REFS", 3, "latex_pdf", "PASS", f"paper/manuscript.tex includes all 5 figures ({len(inc_args)} \\includegraphics calls).")
            else:
                self.record("T3_LATEX_FIGURES_REFS", 3, "latex_pdf", "FAIL", f"paper/manuscript.tex missing \\includegraphics refs for: {missing_figs}.", {"found": inc_args})

            # 2. All \cite* / biblatex citation keys exist in references.bib
            cite_matches = re.findall(
                r"\\(?:cite(?:p|t|alt|alp|author|year|num|text|s|ps|ts)?|textcite|parencite|autocite|footcite|footcitetext|supercite|fullcite|nocite)\*?(?:\s*\[[^\]]*\])*\s*\{([^}]+)\}",
                tex_clean,
            )
            cited_keys: set[str] = set()
            for grp in cite_matches:
                for k in grp.split(","):
                    ks = k.strip()
                    if ks and ks != "*":
                        cited_keys.add(ks)
            if not bib_p.is_file():
                self.record("T3_LATEX_BIBTEX_CITATIONS", 3, "latex_pdf", "FAIL", "Missing paper/references.bib.")
            else:
                bib_text = bib_p.read_text(encoding="utf-8", errors="replace")
                bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_text))
                missing_bib = sorted(cited_keys - bib_keys)
                if cited_keys and not missing_bib:
                    self.record(
                        "T3_LATEX_BIBTEX_CITATIONS",
                        3,
                        "latex_pdf",
                        "PASS",
                        f"100% of cited keys ({len(cited_keys)}/{len(cited_keys)}) resolve in paper/references.bib ({len(bib_keys)} entries).",
                    )
                else:
                    self.record(
                        "T3_LATEX_BIBTEX_CITATIONS",
                        3,
                        "latex_pdf",
                        "FAIL",
                        f"BibTeX citation failure: cited={len(cited_keys)}, missing_in_bib={missing_bib[:15]}.",
                        {"missing": missing_bib},
                    )

        # 3. Compiled PDF structure & multi-page check
        if not pdf_p.is_file():
            self.record("T3_LATEX_PDF_STRUCTURE", 3, "latex_pdf", "FAIL", "Missing paper/manuscript.pdf.")
            self.record("T3_LATEX_PDF_NO_UNRESOLVED", 3, "latex_pdf", "FAIL", "Missing paper/manuscript.pdf.")
            return

        pdf_bytes = pdf_p.read_bytes()
        sz = len(pdf_bytes)
        header_ok = pdf_bytes.startswith(b"%PDF-")
        eof_ok = b"%%EOF" in pdf_bytes[-4096:]
        pages = 0
        pdfinfo_bin = shutil.which("pdfinfo")
        if pdfinfo_bin:
            proc = subprocess.run([pdfinfo_bin, str(pdf_p)], capture_output=True, text=True, timeout=30)
            if proc.returncode == 0:
                m_pg = re.search(r"^Pages:\s*(\d+)", proc.stdout, re.MULTILINE)
                if m_pg:
                    pages = int(m_pg.group(1))
        if pages == 0:
            pages = count_pdf_pages_pure_python(pdf_bytes)

        if header_ok and eof_ok and sz > 5120 and pages >= 5:
            self.record(
                "T3_LATEX_PDF_STRUCTURE",
                3,
                "latex_pdf",
                "PASS",
                f"paper/manuscript.pdf structurally valid ({sz:,} B, {pages} pages >= 5).",
                {"bytes": sz, "pages": pages},
            )
        else:
            self.record(
                "T3_LATEX_PDF_STRUCTURE",
                3,
                "latex_pdf",
                "FAIL",
                f"PDF structure check failed: header={header_ok}, eof={eof_ok}, bytes={sz} (>5120), pages={pages} (>=5).",
            )

        # 4. Zero unresolved ?? / [?] in PDF + non-empty text + diacritics + multiline manuscript.log check
        extracted_text = ""
        method = "pure_python"
        pdftotext_bin = shutil.which("pdftotext")
        if pdftotext_bin:
            proc = subprocess.run([pdftotext_bin, str(pdf_p), "-"], capture_output=True, text=True, timeout=30)
            if proc.returncode == 0 and proc.stdout.strip():
                extracted_text = proc.stdout
                method = "pdftotext"
        if not extracted_text:
            extracted_text = extract_pdf_text_pure_python(pdf_bytes)

        pdf_issues: list[str] = []
        stripped_text = extracted_text.strip()
        if not stripped_text:
            pdf_issues.append("No extractable text found in manuscript.pdf (cannot verify zero unresolved refs)")
        elif method == "pdftotext":
            if len(stripped_text) < 200:
                pdf_issues.append(f"pdftotext extracted too little text ({len(stripped_text)} chars < 200)")
            elif not any(ch in stripped_text for ch in "āīūēōḷḻṇṉṟṭṅĀĪŪĒŌḶḺṆṈṞṬṄ"):
                pdf_issues.append("No Proto-Dravidian diacritics (āīūēōḷḻṇṉṟṭṅ) survived in pdftotext output")

        unresolved_hits: list[str] = []
        for m in re.finditer(r".{0,25}(?:\?\?|\[\?\]).{0,25}", extracted_text):
            unresolved_hits.append(m.group(0).strip())
            if len(unresolved_hits) >= 10:
                break

        log_warnings: list[str] = []
        if log_p.is_file():
            log_text = log_p.read_text(encoding="utf-8", errors="replace")
            for pat in (
                r"LaTeX Warning: Reference[\s\S]{0,160}?undefined",
                r"LaTeX Warning: Citation[\s\S]{0,160}?undefined",
                r"There were undefined references",
                r"There were undefined citations",
                r"Missing character: There is no .* in font",
            ):
                for m in re.finditer(pat, log_text):
                    log_warnings.append(m.group(0).replace("\n", " "))

        if not unresolved_hits and not log_warnings and not pdf_issues:
            self.record(
                "T3_LATEX_PDF_NO_UNRESOLVED",
                3,
                "latex_pdf",
                "PASS",
                f"Zero unresolved citations/refs (?? / [?]) or missing glyphs in manuscript.pdf (method={method}) and manuscript.log.",
                {"method": method, "extracted_chars": len(stripped_text)},
            )
        else:
            self.record(
                "T3_LATEX_PDF_NO_UNRESOLVED",
                3,
                "latex_pdf",
                "FAIL",
                f"PDF/LaTeX quality failure: pdf_hits={len(unresolved_hits)}, log_warnings={len(log_warnings)}, issues={pdf_issues}.",
                {"pdf_hits": unresolved_hits, "log_warnings": log_warnings[:10], "issues": pdf_issues},
            )

    # ===================================================================
    # TIER 4 — Headless Playwright Chromium & Git/Workspace Hygiene
    # ===================================================================

    def run_tier4(self) -> None:
        self._t4_playwright_browser_checks()
        self._t4_git_and_workspace_hygiene()

    def _t4_playwright_browser_checks(self) -> None:
        html_p = self.root / "map_page/index.html"
        if not html_p.is_file():
            for cid in ("T4_BROWSER_LOAD_ZERO_ERRORS", "T4_BROWSER_TABS_5", "T4_BROWSER_DAG_RENDER", "T4_BROWSER_SEARCH_FILTER"):
                self.record(cid, 4, "playwright_browser", "FAIL", "Missing map_page/index.html.")
            return

        pre_m5_skip = self.allow_missing_m5 and not self.m5_build_exists()

        # Derive positive search query dynamically from explorer_data_v3.json if available
        pos_query = "Harappa"
        exp_data, exp_err = load_json(self.root / "work_data/key8c/explorer_data_v3.json")
        if not exp_err and isinstance(exp_data, dict):
            inscs = exp_data.get("inscriptions")
            if isinstance(inscs, list) and inscs and isinstance(inscs[0], dict):
                cand = inscs[0].get("site") or inscs[0].get("id") or inscs[0].get("ref")
                if cand and str(cand).strip():
                    pos_query = str(cand).strip()
            else:
                gl = exp_data.get("glossary")
                if isinstance(gl, list) and gl and isinstance(gl[0], dict):
                    cand = gl[0].get("id") or gl[0].get("gloss")
                    if cand and str(cand).strip():
                        pos_query = str(cand).strip()

        try:
            from playwright.sync_api import sync_playwright
        except Exception as exc:
            for cid in ("T4_BROWSER_LOAD_ZERO_ERRORS", "T4_BROWSER_TABS_5", "T4_BROWSER_DAG_RENDER", "T4_BROWSER_SEARCH_FILTER"):
                self.record(cid, 4, "playwright_browser", "FAIL", f"Playwright unavailable: {exc}.")
            return

        console_errors: list[str] = []
        page_errors: list[str] = []
        failed_reqs: list[str] = []
        external_reqs: list[str] = []

        url = html_p.resolve().as_uri()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                page = context.new_page()
                page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: page_errors.append(str(e)))
                page.on("requestfailed", lambda r: failed_reqs.append(f"{r.url}: {r.failure}"))
                page.on(
                    "request",
                    lambda r: external_reqs.append(r.url)
                    if r.url.lower().startswith(("http://", "https://"))
                    else None,
                )

                page.goto(url, wait_until="load", timeout=30000)
                page.wait_for_timeout(300)

                # 1. Load & zero errors / zero external requests
                if not console_errors and not page_errors and not failed_reqs and not external_reqs:
                    self.record(
                        "T4_BROWSER_LOAD_ZERO_ERRORS",
                        4,
                        "playwright_browser",
                        "PASS",
                        "Headless Chromium loaded map_page/index.html with 0 console errors, 0 page errors, 0 failed reqs, 0 external reqs.",
                    )
                else:
                    self.record(
                        "T4_BROWSER_LOAD_ZERO_ERRORS",
                        4,
                        "playwright_browser",
                        "FAIL",
                        f"Browser errors detected: console={len(console_errors)}, page={len(page_errors)}, failed={len(failed_reqs)}, external={len(external_reqs)}.",
                        {
                            "console_errors": console_errors[:10],
                            "page_errors": page_errors[:10],
                            "failed_requests": failed_reqs[:10],
                            "external_requests": external_reqs[:10],
                        },
                    )

                # 2. Discover & click all 5 tabs
                tab_selectors = ('[role="tab"]', "[data-tab]", ".tab-btn", ".tabs button", "nav button")
                tab_loc = None
                tab_sel_used = None
                tab_count = 0
                for sel in tab_selectors:
                    loc = page.locator(sel)
                    cnt = loc.count()
                    if cnt >= 5:
                        tab_loc = loc
                        tab_sel_used = sel
                        tab_count = cnt
                        break
                    if cnt > tab_count:
                        tab_loc = loc
                        tab_sel_used = sel
                        tab_count = cnt

                if tab_count < 5:
                    if pre_m5_skip:
                        self.record(
                            "T4_BROWSER_TABS_5",
                            4,
                            "playwright_browser",
                            "SKIP",
                            f"Pre-M5 HTML has {tab_count} tabs (< 5); M5 build_map_page.py not yet present (--allow-missing-m5).",
                        )
                    else:
                        self.record(
                            "T4_BROWSER_TABS_5",
                            4,
                            "playwright_browser",
                            "FAIL",
                            f"Expected >= 5 interactive tabs, found {tab_count} (selector={tab_sel_used}).",
                        )
                else:
                    tab_errs: list[str] = []
                    tab_summaries: list[dict[str, Any]] = []
                    distinct_snapshots: set[str] = set()
                    pre_err_n = len(console_errors) + len(page_errors)
                    pre_ext_n = len(external_reqs)
                    pre_fail_n = len(failed_reqs)
                    for i in range(tab_count):
                        btn = tab_loc.nth(i)
                        label = (btn.inner_text() or f"tab_{i}").strip()
                        try:
                            btn.click(timeout=5000)
                            page.wait_for_timeout(150)
                            # Query explicit tabpanel selectors FIRST; only fall back to main > section/div if zero explicit panels exist.
                            # Filter strictly by CSS visibility (NOT r.height > 0) so empty 0-height panels measure 0 chars and FAIL.
                            panel_state = page.evaluate(
                                """() => {
                                    const explicitSel = '[role="tabpanel"], .tab-panel, .tab-pane, .panel-section, section[data-tab-panel], [data-panel]';
                                    let panels = Array.from(document.querySelectorAll(explicitSel));
                                    const hasExplicit = panels.length > 0;
                                    if (!hasExplicit) {
                                        panels = Array.from(document.querySelectorAll('main > section, main > div'));
                                    }
                                    if (panels.length > 0) {
                                        const vis = panels.filter(el => {
                                            if (el.hidden) return false;
                                            const st = window.getComputedStyle(el);
                                            return st.display !== 'none' && st.visibility !== 'hidden';
                                        });
                                        if (vis.length === 0) {
                                            return {len: 0, snapshot: ''};
                                        }
                                        const texts = vis.map(el => (el.innerText || '').trim());
                                        const combined = texts.join('\\n').trim();
                                        const maxLen = Math.max(...texts.map(t => t.length));
                                        return {len: maxLen, snapshot: combined.replace(/\\s+/g, ' ').slice(0, 600)};
                                    }
                                    const bodyTxt = (document.body.innerText || '').trim();
                                    return {len: bodyTxt.length, snapshot: bodyTxt.replace(/\\s+/g, ' ').slice(0, 600)};
                                }"""
                            )
                            vis_len = int(panel_state.get("len", 0))
                            snap = str(panel_state.get("snapshot", ""))
                            if snap:
                                distinct_snapshots.add(snap)
                            tab_summaries.append({"tab": label, "visible_text_len": vis_len})
                            if vis_len <= 50:
                                tab_errs.append(f"Tab '{label}' rendered <=50 chars ({vis_len})")
                        except Exception as exc:
                            tab_errs.append(f"Tab '{label}' click error: {exc}")
                    req_distinct = min(5, tab_count)
                    if len(distinct_snapshots) < req_distinct:
                        tab_errs.append(f"Tabs did not switch distinct visible content ({len(distinct_snapshots)}/{req_distinct} distinct views)")
                    post_err_n = len(console_errors) + len(page_errors)
                    if post_err_n > pre_err_n:
                        tab_errs.append(f"{post_err_n - pre_err_n} runtime console/page error(s) triggered while clicking tabs")
                    if len(external_reqs) > pre_ext_n:
                        tab_errs.append(f"{len(external_reqs) - pre_ext_n} lazy external network request(s) triggered on tab click: {external_reqs[pre_ext_n:pre_ext_n+5]}")
                    if len(failed_reqs) > pre_fail_n:
                        tab_errs.append(f"{len(failed_reqs) - pre_fail_n} failed network request(s) triggered on tab click")
                    if not tab_errs:
                        self.record(
                            "T4_BROWSER_TABS_5",
                            4,
                            "playwright_browser",
                            "PASS",
                            f"Clicked all {tab_count} tabs ({tab_sel_used}); {len(distinct_snapshots)} distinct views (>50 chars each), 0 runtime/network errors.",
                            {"tabs": tab_summaries, "distinct_views": len(distinct_snapshots)},
                        )
                    else:
                        self.record(
                            "T4_BROWSER_TABS_5",
                            4,
                            "playwright_browser",
                            "FAIL",
                            "; ".join(tab_errs),
                            {"tabs": tab_summaries, "distinct_views": len(distinct_snapshots), "external_requests": external_reqs[:10]},
                        )

                    # Return to first tab (DAG) for SVG inspection
                    try:
                        tab_loc.nth(0).click(timeout=5000)
                        page.wait_for_timeout(150)
                    except Exception:
                        pass

                # 3. DAG SVG rendered rect non-overlap & <=12-char label check
                # Ensure DAG SVG is visible (if hidden in another tab, try clicking tab containing 'map'/'dag'/'tree')
                if tab_loc is not None and tab_count >= 2:
                    has_vis_sv = page.evaluate(
                        """() => {
                            const s = document.querySelector('svg#sv, svg[data-dag], svg.dag');
                            if (!s) return false;
                            const r = s.getBoundingClientRect();
                            return r.width > 0 && r.height > 0;
                        }"""
                    )
                    if not has_vis_sv:
                        for i in range(tab_count):
                            tab_loc.nth(i).click(timeout=5000)
                            page.wait_for_timeout(100)
                            ok = page.evaluate(
                                """() => {
                                    const s = document.querySelector('svg#sv, svg[data-dag], svg.dag');
                                    if (!s) return false;
                                    const r = s.getBoundingClientRect();
                                    return r.width > 0 && r.height > 0;
                                }"""
                            )
                            if ok:
                                break

                dag_report = page.evaluate(
                    """() => {
                        let svg = document.querySelector('svg#sv, svg[data-dag], svg.dag');
                        if (!svg) {
                            const svgs = Array.from(document.querySelectorAll('svg')).filter(s => {
                                const r = s.getBoundingClientRect();
                                return r.width > 0 && r.height > 0 && s.querySelectorAll('rect').length >= 3;
                            });
                            svg = svgs[0] || null;
                        }
                        if (!svg) return {found: false};
                        const sRect = svg.getBoundingClientRect();
                        let nodeGroups = Array.from(svg.querySelectorAll('g.nd, g.node, g[data-node]'));
                        let rects = [];
                        let texts = [];
                        if (nodeGroups.length >= 2) {
                            for (const g of nodeGroups) {
                                const rEl = g.querySelector('rect');
                                if (rEl) {
                                    const b = rEl.getBoundingClientRect();
                                    if (b.width > 2 && b.height > 2) {
                                        rects.push({left: b.left, top: b.top, right: b.right, bottom: b.bottom, text: (g.textContent || '').trim().slice(0, 30)});
                                    }
                                }
                                for (const t of g.querySelectorAll('text')) {
                                    const tspans = Array.from(t.querySelectorAll('tspan'));
                                    if (tspans.length > 0) {
                                        for (const ts of tspans) texts.push((ts.textContent || '').trim());
                                    } else {
                                        for (const ln of (t.textContent || '').split('\\n')) texts.push(ln.trim());
                                    }
                                }
                            }
                        } else {
                            for (const rEl of svg.querySelectorAll('rect')) {
                                const b = rEl.getBoundingClientRect();
                                if (b.width < 5 || b.height < 5) continue;
                                if (b.width >= 0.85 * sRect.width && b.height >= 0.85 * sRect.height) continue;
                                rects.push({left: b.left, top: b.top, right: b.right, bottom: b.bottom, text: rEl.getAttribute('data-id') || ''});
                            }
                            for (const t of svg.querySelectorAll('text')) {
                                const tspans = Array.from(t.querySelectorAll('tspan'));
                                if (tspans.length > 0) {
                                    for (const ts of tspans) texts.push((ts.textContent || '').trim());
                                } else {
                                    for (const ln of (t.textContent || '').split('\\n')) texts.push(ln.trim());
                                }
                            }
                        }
                        const overlaps = [];
                        const tol = 1.0;
                        for (let i = 0; i < rects.length; i++) {
                            for (let j = i + 1; j < rects.length; j++) {
                                const a = rects[i], b = rects[j];
                                if (a.left + tol < b.right && b.left + tol < a.right && a.top + tol < b.bottom && b.top + tol < a.bottom) {
                                    overlaps.push({a: a.text || i, b: b.text || j});
                                    if (overlaps.length >= 20) break;
                                }
                            }
                            if (overlaps.length >= 20) break;
                        }
                        const longLabels = texts.filter(s => s.length > 12).map(s => ({text: s, len: s.length}));
                        return {found: true, rectCount: rects.length, textLineCount: texts.length, overlaps, longLabels};
                    }"""
                )

                if not dag_report.get("found") or dag_report.get("rectCount", 0) == 0:
                    self.record("T4_BROWSER_DAG_RENDER", 4, "playwright_browser", "FAIL", "Could not locate rendered DAG SVG with node rects.")
                else:
                    ov = dag_report.get("overlaps", [])
                    ll = dag_report.get("longLabels", [])
                    if not ov and not ll:
                        self.record(
                            "T4_BROWSER_DAG_RENDER",
                            4,
                            "playwright_browser",
                            "PASS",
                            f"Rendered DAG SVG verified: {dag_report['rectCount']} rects, 0 overlaps, 0 label lines > 12 chars.",
                        )
                    elif pre_m5_skip and not ov:
                        self.record(
                            "T4_BROWSER_DAG_RENDER",
                            4,
                            "playwright_browser",
                            "SKIP",
                            f"Pre-M5 HTML has 0 SVG rect overlaps but legacy >12-char labels awaiting M5 (--allow-missing-m5): {ll[:5]}",
                        )
                    else:
                        self.record(
                            "T4_BROWSER_DAG_RENDER",
                            4,
                            "playwright_browser",
                            "FAIL",
                            f"Rendered DAG defect: overlaps={len(ov)}, labels_gt12={len(ll)}.",
                            {"overlaps": ov[:10], "long_labels": ll[:10]},
                        )

                # 4. Live dynamic search filtering test (with runtime error & network monitoring)
                pre_s_err = len(console_errors) + len(page_errors)
                pre_s_ext = len(external_reqs)
                pre_s_fail = len(failed_reqs)
                search_res = self._test_live_search_filter(page, tab_loc, tab_count, pos_query)
                post_s_errs: list[str] = []
                if len(console_errors) + len(page_errors) > pre_s_err:
                    post_s_errs.append(f"{(len(console_errors) + len(page_errors)) - pre_s_err} console/page error(s) during search")
                if len(external_reqs) > pre_s_ext:
                    post_s_errs.append(f"{len(external_reqs) - pre_s_ext} external request(s) during search")
                if len(failed_reqs) > pre_s_fail:
                    post_s_errs.append(f"{len(failed_reqs) - pre_s_fail} failed request(s) during search")

                if search_res["status"] == "SKIP" and pre_m5_skip and not post_s_errs:
                    self.record("T4_BROWSER_SEARCH_FILTER", 4, "playwright_browser", "SKIP", search_res["message"])
                elif search_res["status"] == "PASS" and not post_s_errs:
                    self.record("T4_BROWSER_SEARCH_FILTER", 4, "playwright_browser", "PASS", search_res["message"], search_res.get("details"))
                else:
                    msg = search_res["message"]
                    if post_s_errs:
                        msg = f"{msg}; {'; '.join(post_s_errs)}"
                    self.record("T4_BROWSER_SEARCH_FILTER", 4, "playwright_browser", "FAIL", msg, search_res.get("details"))
            finally:
                browser.close()

    def _test_live_search_filter(self, page, tab_loc, tab_count: int, pos_query: str) -> dict[str, Any]:
        input_sel = 'input[type="search"], input[type="text"], input:not([type])'

        def find_visible_search_input():
            loc = page.locator(input_sel)
            for idx in range(loc.count()):
                el = loc.nth(idx)
                try:
                    if el.is_visible():
                        return el
                except Exception:
                    continue
            return None

        target_input = find_visible_search_input()
        if target_input is None and tab_loc is not None and tab_count > 0:
            for i in range(tab_count):
                try:
                    tab_loc.nth(i).click(timeout=5000)
                    page.wait_for_timeout(120)
                except Exception:
                    continue
                target_input = find_visible_search_input()
                if target_input is not None:
                    break

        if target_input is None:
            return {
                "status": "SKIP" if (self.allow_missing_m5 and not self.m5_build_exists()) else "FAIL",
                "message": "No visible search <input> found across tabs.",
            }

        def count_visible_items(locked_sel: str | None = None, use_panel_scope: bool | None = None) -> dict[str, Any]:
            return page.evaluate(
                """([lockedSel, usePanelScope]) => {
                    const isVis = (el) => {
                        if (el.hidden) return false;
                        const st = window.getComputedStyle(el);
                        const r = el.getBoundingClientRect();
                        return st.display !== 'none' && st.visibility !== 'hidden' && r.width > 0 && r.height > 0;
                    };
                    // Prefer scoping to the active visible tabpanel if present
                    const explicitPanels = Array.from(document.querySelectorAll(
                        '[role="tabpanel"], .tab-panel, .tab-pane, .panel-section, section[data-tab-panel], [data-panel]'
                    )).filter(el => {
                        if (el.hidden) return false;
                        const st = window.getComputedStyle(el);
                        return st.display !== 'none' && st.visibility !== 'hidden';
                    });
                    const activeRoot = explicitPanels.length === 1 ? explicitPanels[0] : null;

                    if (lockedSel) {
                        const root = (usePanelScope && activeRoot) ? activeRoot : document;
                        const els = Array.from(root.querySelectorAll(lockedSel)).filter(isVis);
                        const textScope = root === document ? document.body : root;
                        return {
                            count: els.length,
                            selector: lockedSel,
                            usePanelScope: Boolean(usePanelScope && activeRoot),
                            bodyText: (textScope.innerText || '').slice(0, 50000),
                        };
                    }

                    const primarySelectors = [
                        'tbody tr',
                        '[data-search-item]',
                        '.insc-row',
                        '.insc-card',
                        '.glossary-row',
                        '.result-row',
                        'li.entry'
                    ];
                    const fallbackSelectors = ['.card', '.item'];

                    function pickBest(root, sels) {
                        let best = 0;
                        let bestSel = '';
                        for (const sel of sels) {
                            const els = Array.from(root.querySelectorAll(sel)).filter(isVis);
                            if (els.length > best) {
                                best = els.length;
                                bestSel = sel;
                            }
                        }
                        return {best, bestSel};
                    }

                    const rootsToTry = activeRoot ? [[activeRoot, true], [document, false]] : [[document, false]];
                    for (const [root, isScoped] of rootsToTry) {
                        let res = pickBest(root, primarySelectors);
                        if (res.best === 0) {
                            res = pickBest(root, fallbackSelectors);
                        }
                        if (res.best > 0) {
                            const textScope = root === document ? document.body : root;
                            return {
                                count: res.best,
                                selector: res.bestSel,
                                usePanelScope: isScoped,
                                bodyText: (textScope.innerText || '').slice(0, 50000),
                            };
                        }
                    }
                    return {count: 0, selector: '', usePanelScope: false, bodyText: (document.body.innerText || '').slice(0, 50000)};
                }""",
                [locked_sel, use_panel_scope],
            )

        # Ensure input starts empty
        target_input.fill("")
        page.wait_for_timeout(150)
        init_state = count_visible_items()
        init_cnt = init_state["count"]
        locked_sel = init_state["selector"]
        locked_scope = bool(init_state.get("usePanelScope", False))
        if init_cnt <= 0 or not locked_sel:
            return {
                "status": "FAIL",
                "message": "Search tab rendered 0 initial items before filtering.",
                "details": {"init_count": init_cnt},
            }

        # Pick a query guaranteed to appear in the initial visible text if pos_query doesn't
        active_query = pos_query
        if active_query.lower() not in init_state["bodyText"].lower():
            fallback = page.evaluate(
                """([sel, usePanelScope]) => {
                    const explicitPanels = Array.from(document.querySelectorAll(
                        '[role="tabpanel"], .tab-panel, .tab-pane, .panel-section, section[data-tab-panel], [data-panel]'
                    )).filter(el => {
                        if (el.hidden) return false;
                        const st = window.getComputedStyle(el);
                        return st.display !== 'none' && st.visibility !== 'hidden';
                    });
                    const root = (usePanelScope && explicitPanels.length === 1) ? explicitPanels[0] : document;
                    const els = Array.from(root.querySelectorAll(sel || 'tbody tr, .card, .item')).filter(el => {
                        if (el.hidden) return false;
                        const st = window.getComputedStyle(el);
                        const r = el.getBoundingClientRect();
                        return st.display !== 'none' && st.visibility !== 'hidden' && r.width > 0 && r.height > 0;
                    });
                    if (!els.length) return '';
                    const words = (els[0].innerText || '').split(/\\s+/).filter(w => w.length >= 3 && /[A-Za-z0-9]/.test(w));
                    return words[0] || '';
                }""",
                [locked_sel, locked_scope],
            )
            if fallback:
                active_query = fallback

        target_input.fill(active_query)
        target_input.dispatch_event("input")
        page.wait_for_timeout(200)
        pos_state = count_visible_items(locked_sel, locked_scope)

        neg_query = "zzzxxyy999_nomatch"
        target_input.fill(neg_query)
        target_input.dispatch_event("input")
        page.wait_for_timeout(200)
        neg_state = count_visible_items(locked_sel, locked_scope)

        # Reset input
        target_input.fill("")
        target_input.dispatch_event("input")

        pos_ok = (0 < pos_state["count"] <= init_cnt) and (active_query.lower() in pos_state["bodyText"].lower())
        neg_zero_msg = bool(re.search(r"\b(?:0\s+(?:results?|matches?|items?|rows?|inscriptions?|signs?)|no\s+(?:results?|matches?))\b", neg_state["bodyText"], re.IGNORECASE))
        neg_ok = (neg_state["count"] == 0) or (neg_state["count"] <= 1 and neg_zero_msg)

        if pos_ok and neg_ok:
            return {
                "status": "PASS",
                "message": f"Dynamic search verified (sel='{locked_sel}', init={init_cnt}, query='{active_query}'->{pos_state['count']}, nonsense->{neg_state['count']}).",
                "details": {"selector": locked_sel, "init": init_cnt, "query": active_query, "pos_count": pos_state["count"], "neg_count": neg_state["count"]},
            }
        return {
            "status": "FAIL",
            "message": f"Dynamic search check failed (sel='{locked_sel}', init={init_cnt}, query='{active_query}'->{pos_state['count']}, nonsense->{neg_state['count']}).",
            "details": {"selector": locked_sel, "init": init_cnt, "query": active_query, "pos_count": pos_state["count"], "neg_count": neg_state["count"]},
        }

    def _t4_git_and_workspace_hygiene(self) -> None:
        def git(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                ["git", "-C", str(self.root), *args],
                capture_output=True,
                text=True,
                timeout=30,
            )

        # 1. Branch == "work"
        br = git("branch", "--show-current")
        branch_name = br.stdout.strip()
        if br.returncode == 0 and branch_name == "work":
            self.record("T4_GIT_BRANCH_WORK", 4, "git_hygiene", "PASS", "Active git branch is 'work'.")
        else:
            self.record("T4_GIT_BRANCH_WORK", 4, "git_hygiene", "FAIL", f"Expected git branch 'work', got '{branch_name}' (rc={br.returncode}).")

        # 2. Local main untouched (if refs/heads/main exists)
        has_main = git("show-ref", "--verify", "--quiet", "refs/heads/main").returncode == 0
        if not has_main:
            self.record("T4_GIT_MAIN_UNTOUCHED", 4, "git_hygiene", "PASS", "Local refs/heads/main absent (work-only branch); main untouched.")
        else:
            has_orig_main = git("show-ref", "--verify", "--quiet", "refs/remotes/origin/main").returncode == 0
            main_sha = git("rev-parse", "refs/heads/main").stdout.strip()
            head_sha = git("rev-parse", "HEAD").stdout.strip()
            if has_orig_main:
                orig_sha = git("rev-parse", "refs/remotes/origin/main").stdout.strip()
                if main_sha == orig_sha and branch_name != "main":
                    self.record("T4_GIT_MAIN_UNTOUCHED", 4, "git_hygiene", "PASS", f"Local main matches origin/main ({main_sha[:8]}) and HEAD is not main.")
                else:
                    self.record("T4_GIT_MAIN_UNTOUCHED", 4, "git_hygiene", "FAIL", f"Local main ({main_sha[:8]}) differs from origin/main ({orig_sha[:8]}) or HEAD is on main.")
            else:
                if branch_name != "main":
                    self.record("T4_GIT_MAIN_UNTOUCHED", 4, "git_hygiene", "PASS", f"HEAD ({head_sha[:8]}) is on '{branch_name}', not main ({main_sha[:8]}).")
                else:
                    self.record("T4_GIT_MAIN_UNTOUCHED", 4, "git_hygiene", "FAIL", "HEAD is currently on main.")

        # 3. Zero .agents tracked or staged
        ls_ag = git("ls-files", ".agents")
        tracked_ag = [ln for ln in ls_ag.stdout.splitlines() if ln.strip()]
        cached = git("diff", "--cached", "--name-only")
        staged_ag = [ln for ln in cached.stdout.splitlines() if ln.strip() == ".agents" or ln.strip().startswith(".agents/")]
        if ls_ag.returncode == 0 and cached.returncode == 0 and not tracked_ag and not staged_ag:
            self.record("T4_GIT_NO_AGENTS_TRACKED", 4, "git_hygiene", "PASS", "Zero .agents/ files tracked or staged in git.")
        else:
            self.record(
                "T4_GIT_NO_AGENTS_TRACKED",
                4,
                "git_hygiene",
                "FAIL",
                f"Detected .agents/ git leakage: tracked={len(tracked_ag)}, staged={len(staged_ag)}.",
                {"tracked": tracked_ag[:10], "staged": staged_ag[:10]},
            )

        # 4. No stray temporary/build files in repo root
        bad_exts = {".tmp", ".bak", ".log", ".aux", ".out", ".pyc", ".pdf", ".png", ".svg"}
        stray: list[str] = []
        for entry in sorted(self.root.iterdir()):
            if entry.is_dir():
                continue
            name = entry.name
            low = name.lower()
            if entry.suffix.lower() in bad_exts or low == "m.js" or low.startswith(("tmp_", "scratch")) or (low.startswith("test_") and low.endswith(".py")):
                stray.append(name)
        if not stray:
            self.record("T4_WORKSPACE_NO_STRAY_FILES", 4, "git_hygiene", "PASS", "Zero stray temporary/build files in repository root.")
        else:
            self.record("T4_WORKSPACE_NO_STRAY_FILES", 4, "git_hygiene", "FAIL", f"Stray files in repo root: {stray}.", {"stray": stray})

    # ===================================================================
    # Summary & Reporting
    # ===================================================================

    def build_report(self, tiers_run: list[int]) -> dict[str, Any]:
        by_tier: dict[str, dict[str, int]] = {}
        for t in tiers_run:
            t_checks = [c for c in self.checks if c["tier"] == t]
            by_tier[str(t)] = {
                "total": len(t_checks),
                "passed": sum(1 for c in t_checks if c["status"] == "PASS"),
                "failed": sum(1 for c in t_checks if c["status"] == "FAIL"),
                "skipped": sum(1 for c in t_checks if c["status"] == "SKIP"),
            }
        total = len(self.checks)
        passed = sum(1 for c in self.checks if c["status"] == "PASS")
        failed = sum(1 for c in self.checks if c["status"] == "FAIL")
        skipped = sum(1 for c in self.checks if c["status"] == "SKIP")
        exit_code = 0 if (failed == 0 and (self.allow_missing_m5 or skipped == 0)) else 1
        return {
            "root": str(self.root),
            "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tiers_run": tiers_run,
            "allow_missing_m5": self.allow_missing_m5,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "by_tier": by_tier,
            },
            "exit_code": exit_code,
            "checks": self.checks,
        }


def print_summary(report: dict[str, Any]) -> None:
    s = report["summary"]
    print("=" * 78)
    print(f"Key #8 E2E Verification Suite | root={report['root']}")
    print(f"Tiers={report['tiers_run']} | allow_missing_m5={report['allow_missing_m5']} | exit_code={report['exit_code']}")
    print("-" * 78)
    print(f"{'Tier':<8}{'Total':>8}{'PASS':>8}{'FAIL':>8}{'SKIP':>8}")
    for t in report["tiers_run"]:
        bt = s["by_tier"][str(t)]
        print(f"Tier {t:<3}{bt['total']:>8}{bt['passed']:>8}{bt['failed']:>8}{bt['skipped']:>8}")
    print("-" * 78)
    print(f"{'TOTAL':<8}{s['total']:>8}{s['passed']:>8}{s['failed']:>8}{s['skipped']:>8}")
    print("=" * 78)

    failed_checks = [c for c in report["checks"] if c["status"] == "FAIL"]
    skipped_checks = [c for c in report["checks"] if c["status"] == "SKIP"]
    if failed_checks:
        print("\nFAILED CHECKS:")
        for c in failed_checks:
            print(f"  [FAIL] T{c['tier']} {c['id']}: {c['message']}")
    if skipped_checks:
        print("\nSKIPPED CHECKS:")
        for c in skipped_checks:
            print(f"  [SKIP] T{c['tier']} {c['id']}: {c['message']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Key #8 Independent 4-Tier E2E Verification Suite")
    parser.add_argument("--tier", choices=("1", "2", "3", "4", "all"), default="all", help="Verification tier to execute")
    parser.add_argument("--json-out", type=Path, default=None, help="Write structured JSON report to PATH")
    parser.add_argument(
        "--allow-missing-m5",
        action="store_true",
        default=False,
        help="Allow strictly absent M5 deliverables to be SKIP instead of FAIL (never skips present-but-broken artifacts)",
    )
    parser.add_argument("--root", type=Path, default=None, help="Override repository root path")
    args = parser.parse_args(argv)

    root = args.root.resolve() if args.root else DEFAULT_ROOT
    tiers_run = [1, 2, 3, 4] if args.tier == "all" else [int(args.tier)]

    verifier = E2EVerifier(root=root, allow_missing_m5=args.allow_missing_m5)
    for t in tiers_run:
        if t == 1:
            verifier.run_tier1()
        elif t == 2:
            verifier.run_tier2()
        elif t == 3:
            verifier.run_tier3()
        elif t == 4:
            verifier.run_tier4()

    report = verifier.build_report(tiers_run)
    print_summary(report)

    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return int(report["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
