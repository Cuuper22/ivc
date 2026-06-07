#!/usr/bin/env python
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / ".codex" / "ivc_research_state.json"
IMAGE_PATH = ROOT / ".codex" / "assets" / "codex-loop-warning.png"
LOG_DIR = ROOT / ".codex" / "hooks" / "logs"
RUN_STATE_PATH = ROOT / ".codex" / "hooks" / "agent_script_runs.json"
MAX_BACKGROUND_SECONDS = 20 * 60
MAX_TMP_SCRIPT_AGE_SECONDS = 6 * 60 * 60


LANGUAGE_QUESTIONS = [
    "what is actually written",
    "which physical side and direction",
    "same sign/allograph/damage/transcription split/distinct sign",
    "what formula slot",
    "what external variable the slot predicts",
    "which hypothesis survives/dies/stays unresolved",
    "what source image or prior-work claim decides the next gate",
]


DISTRACTION_PATTERNS = [
    r"\bnpm\s+(run\s+)?(build|test|lint|dev)\b",
    r"\bpnpm\s+(build|test|lint|dev)\b",
    r"\byarn\s+(build|test|lint|dev)\b",
    r"\bpytest\b",
    r"\bgo\s+test\b",
    r"\bcargo\s+test\b",
    r"\bplaywright\b",
    r"\bnext\s+(build|dev)\b",
    r"\bvite\b",
]


ADMIN_ALLOW_PATTERNS = [
    r"\.codex",
    r"hooks?",
    r"ivc_hook",
    r"codex\s+(debug|features|app-server)",
    r"git\s+status",
    r"rg\b",
    r"Get-Content",
    r"Select-String",
]


SCRIPT_PATH_PATTERN = re.compile(
    r"(?P<path>(?:[A-Za-z]:[\\/]|\.?[\\/])?(?:tmp|data)[\\/][^\s'\"`]+?\.(?:py|mjs|js|ps1)|[A-Za-z]:[^\s'\"`]+?[\\/](?:tmp|data)[\\/][^\s'\"`]+?\.(?:py|mjs|js|ps1))",
    flags=re.IGNORECASE,
)

BACKGROUND_LAUNCH_PATTERN = re.compile(
    r"\b(Start-Process|Start-Job|nohup|&\s*$|--watch|--serve|npm\s+run\s+dev|vite\s+--host|next\s+dev)\b",
    flags=re.IGNORECASE,
)


def read_stdin_json():
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {"_raw_stdin": raw[:4000]}


def emit(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=True))


def hook_context(event_name, text):
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": event_name,
                "additionalContext": text,
            }
        }
    )


def empty():
    emit({})


def load_state():
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"state_error": str(exc)}


def load_run_state():
    if not RUN_STATE_PATH.exists():
        return {"runs": []}
    try:
        data = json.loads(RUN_STATE_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"runs": []}
        data.setdefault("runs", [])
        return data
    except Exception:
        return {"runs": []}


def save_run_state(state):
    RUN_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = RUN_STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=True, indent=2), encoding="utf-8")
    tmp.replace(RUN_STATE_PATH)


def resolve_project_path(raw_path):
    cleaned = str(raw_path).strip().strip("'\"`")
    if not cleaned:
        return None
    path = Path(cleaned)
    if not path.is_absolute():
        path = ROOT / path
    try:
        resolved = path.resolve()
        resolved.relative_to(ROOT)
        return resolved
    except Exception:
        return None


def project_script_paths(cmd):
    paths = []
    seen = set()
    for match in SCRIPT_PATH_PATTERN.finditer(cmd or ""):
        path = resolve_project_path(match.group("path"))
        if path and path.exists() and path not in seen:
            paths.append(path)
            seen.add(path)
    return paths


def path_age_seconds(path):
    try:
        return datetime.now().timestamp() - path.stat().st_mtime
    except Exception:
        return 0


def is_temp_agent_script(path):
    try:
        rel = path.relative_to(ROOT).as_posix().lower()
    except Exception:
        return False
    return rel.startswith("tmp/") and (Path(rel).name.startswith("run_") or "/run_" in rel)


def latest_research_state_mtime():
    candidates = [
        STATE_PATH,
        ROOT / "docs" / "active_decipherment_attempt.md",
        ROOT / "docs" / "evidence_ledger.md",
        ROOT / "docs" / "source_register.md",
        ROOT / "docs" / "experiment_backlog.md",
        ROOT / "data" / "claim_ledger" / "claims.json",
    ]
    mtimes = []
    for path in candidates:
        try:
            if path.exists():
                mtimes.append(path.stat().st_mtime)
        except Exception:
            pass
    return max(mtimes) if mtimes else 0


def stale_script_decision(cmd):
    if "ALLOW_STALE_AGENT_SCRIPT=1" in cmd or "--allow-stale-script" in cmd:
        return None
    stale_tmp = []
    state_newer = []
    state_mtime = latest_research_state_mtime()
    for path in project_script_paths(cmd):
        age = path_age_seconds(path)
        rel = path.relative_to(ROOT).as_posix()
        if is_temp_agent_script(path) and age > MAX_TMP_SCRIPT_AGE_SECONDS:
            stale_tmp.append((rel, int(age // 60)))
        elif "data/" in rel.lower() and "/tools/" in rel.lower() and state_mtime > path.stat().st_mtime:
            state_newer.append(rel)
    if stale_tmp:
        details = "; ".join(f"{rel} age={minutes}m" for rel, minutes in stale_tmp[:5])
        return (
            "Blocked by IVC hook: stale temp agent runner. "
            f"{details}. Refresh the runner for the current evidence gate or promote it to data/.../tools with provenance."
        )
    if state_newer:
        return None
    return None


def process_alive(pid):
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {int(pid)}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return str(pid) in result.stdout and "INFO:" not in result.stdout
    except Exception:
        return False


def kill_process_tree(pid):
    try:
        subprocess.run(
            ["taskkill", "/PID", str(int(pid)), "/T", "/F"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return True
    except Exception:
        return False


def reap_stale_project_runs():
    state = load_run_state()
    now = datetime.now().timestamp()
    kept = []
    killed = []
    changed = False
    for run in state.get("runs", []):
        pid = run.get("pid")
        started = float(run.get("started_ts") or 0)
        if not pid or not process_alive(pid):
            changed = True
            continue
        age = now - started
        if age > MAX_BACKGROUND_SECONDS:
            if kill_process_tree(pid):
                killed.append({"pid": pid, "cmd": run.get("cmd"), "age_seconds": int(age)})
                changed = True
            else:
                kept.append(run)
        else:
            kept.append(run)
    state["runs"] = kept
    if killed:
        state.setdefault("killed", []).extend(killed[-20:])
    if changed:
        save_run_state(state)
    return killed


def record_possible_background_run(cmd, payload):
    if not cmd or not BACKGROUND_LAUNCH_PATTERN.search(cmd):
        return
    if not project_script_paths(cmd) and str(ROOT).lower() not in cmd.lower():
        return
    state = load_run_state()
    state.setdefault("runs", []).append(
        {
            "started_ts": datetime.now().timestamp(),
            "event": payload.get("hook_event_name") or payload.get("event"),
            "turn_id": payload.get("turn_id"),
            "tool_name": payload.get("tool_name"),
            "pid": None,
            "cmd": cmd[:1000],
            "cwd": os.getcwd(),
            "note": "Background launch detected. PID unknown unless script writes one; stale sweep still warns on future hooks.",
        }
    )
    save_run_state(state)


def log_event(event, payload, note=None):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / "ivc_hooks.jsonl"
    row = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "event": event,
        "note": note,
        "cwd": os.getcwd(),
        "turn_id": payload.get("turn_id"),
        "tool_name": payload.get("tool_name"),
        "source": payload.get("source"),
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=True) + "\n")
    try:
        if log_path.stat().st_size > 1_000_000:
            lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
            log_path.write_text("\n".join(lines[-2000:]) + "\n", encoding="utf-8")
    except Exception:
        pass


def base_research_context(include_compact_image=False):
    state = load_state()
    accepted = state.get("accepted_claim_counts", {})
    frontiers = state.get("current_frontiers", [])

    frontier_lines = []
    for item in frontiers:
        frontier_lines.append(
            f"- {item.get('name')}: {item.get('question')} Next gate: {item.get('next_gate')}"
        )

    text = [
        "IVC RESEARCH MODE IS ACTIVE.",
        "This workspace is an academic decipherment attempt, not a software project.",
        "Code is allowed only as a research instrument: parsing, source retrieval, image/crop handling, tabulation, and evidence integrity.",
        "Do not drift into app-building, CI, unit-test theater, generic audits, or foundation-building unless it directly decides a live decipherment claim.",
        "",
        "Valid progress must answer at least one language/source question:",
    ]
    text.extend(f"- {q}" for q in LANGUAGE_QUESTIONS)
    text.extend(
        [
            "",
            "Accepted claim counts right now:",
            f"- translations: {accepted.get('translations', 0)}",
            f"- phonetic values: {accepted.get('phonetic_values', 0)}",
            f"- sign meanings: {accepted.get('sign_meanings', 0)}",
            f"- stable language identification: {accepted.get('stable_language_identification', 0)}",
            "",
            "Current live frontiers:",
        ]
    )
    text.extend(frontier_lines or ["- Missing frontier state. Rebuild from docs/evidence_ledger.md before research claims."])
    text.extend(
        [
            "",
            "Agent policy:",
            "- Keep one mechanic agent for scripts/data/crops/hash/path integrity.",
            "- Everyone else must be a researcher, linguist, epigrapher, source critic, or adversarial prior-work reviewer.",
            "- Mechanic output is only useful if it serves a sign/side/slot/source question.",
        ]
    )
    if include_compact_image:
        text.extend(
            [
                "",
                "POST-COMPACTION WARNING IMAGE:",
                f"- Stored at: {IMAGE_PATH}",
                "- Treat this as loaded context: do not behave like the image.",
                "- No Codex loop, no 'you said it not me' reframing, no hedge maxxing, no essay machine, no ritual key phrases, no cracked junior engineer busywork, no explaining away broken evidence.",
                "- If evidence breaks a claim, say the claim broke and move to the next gate.",
            ]
        )
    return "\n".join(text)


def event_session_start(payload):
    source = str(payload.get("source") or "").lower()
    trigger = str(payload.get("trigger") or "").lower()
    include_image = source == "compact" or trigger == "compact"
    killed = reap_stale_project_runs()
    log_event("SessionStart", payload, note=f"source={source};trigger={trigger}")
    text = base_research_context(include_compact_image=include_image)
    if killed:
        text += "\n\nPROJECT HOOK REAPED STALE BACKGROUND RUNS:\n"
        text += "\n".join(f"- pid {row.get('pid')} age={row.get('age_seconds')}s" for row in killed)
    hook_context("SessionStart", text)


def event_user_prompt_submit(payload):
    prompt = str(payload.get("prompt") or "")
    lowered = prompt.lower()
    ivc_related = any(
        token in lowered
        for token in [
            "ivc",
            "indus",
            "harappa",
            "mohenjo",
            "cisi",
            "decipher",
            "translation",
            "script",
            "sign",
            "grapheme",
            "034",
            "415",
            "m-",
            "h-",
        ]
    )
    hook_admin = "hook" in lowered or ".codex" in lowered
    if ivc_related and not hook_admin:
        text = (
            "Before answering, classify this IVC turn as one of: source evidence, graphemics, side mapping, allography, formula slot, semantic anchor, prior-work test, or research governance. "
            "Answer it as a language/source-critical research problem. The next action must move a live decipherment question toward accept, reject, or unresolved."
        )
    elif hook_admin:
        text = (
            "This is Codex hook/admin work for the IVC research discipline. Keep it short and concrete. Do not turn it into app architecture."
        )
    else:
        text = (
            "If this touches the IVC workspace, keep the research frame: inscription, source, sign, side, slot, evidence, decision gate."
        )
    log_event("UserPromptSubmit", payload, note="prompt_context_injected")
    hook_context("UserPromptSubmit", text)


def command_text(payload):
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("command", "cmd", "script", "query"):
            if key in tool_input:
                return str(tool_input[key])
        return json.dumps(tool_input, ensure_ascii=True)
    return str(tool_input)


def is_distraction_command(cmd):
    if any(re.search(p, cmd, flags=re.IGNORECASE) for p in ADMIN_ALLOW_PATTERNS):
        return False
    return any(re.search(p, cmd, flags=re.IGNORECASE) for p in DISTRACTION_PATTERNS)


def event_pre_tool_use(payload):
    cmd = command_text(payload)
    tool = str(payload.get("tool_name") or "")
    killed = reap_stale_project_runs()
    log_event("PreToolUse", payload, note=cmd[:240])
    stale_reason = stale_script_decision(cmd)
    if stale_reason:
        emit({"decision": "block", "reason": stale_reason})
        return
    if (
        cmd
        and BACKGROUND_LAUNCH_PATTERN.search(cmd)
        and project_script_paths(cmd)
        and "ALLOW_BACKGROUND_AGENT_RUN=1" not in cmd
        and "--allow-background-agent-run" not in cmd
    ):
        emit(
            {
                "decision": "block",
                "reason": (
                    "Blocked by IVC hook: project agent scripts must run foreground-bounded. "
                    "Do not leave Start-Process/watch/dev/background jobs alive in this research workspace."
                ),
            }
        )
        return
    if cmd and is_distraction_command(cmd):
        emit(
            {
                "decision": "block",
                "reason": (
                    "Blocked by IVC research hook: this looks like software-project work. "
                    "Run it only if you can name the inscription/sign/side/slot/source claim it decides."
                ),
            }
        )
        return
    text = (
        f"Pre-tool research constraint for {tool or 'tool'}: this action should produce source evidence, graphemic evidence, side/direction evidence, slot evidence, prior-work pressure, or mechanic support for one of those. "
        "After the tool returns, extract the evidence delta and next decision gate."
    )
    if killed:
        text += " Project hook also reaped stale project background runs before this tool."
    hook_context("PreToolUse", text)


def event_post_tool_use(payload):
    cmd = command_text(payload)
    record_possible_background_run(cmd, payload)
    killed = reap_stale_project_runs()
    log_event("PostToolUse", payload, note="capture_evidence_delta")
    text = (
        "Post-tool evidence capture: if the tool touched source pages, OCR, images, tables, papers, or ledgers, record the delta as: source/object, sign/side, finding, confidence, claim affected, and next gate. "
        "Do not drift into process narration."
    )
    if killed:
        text += " Project hook reaped stale background runs after this tool."
    hook_context("PostToolUse", text)


def event_pre_compact(payload):
    log_event("PreCompact", payload, note="state_check")
    if not STATE_PATH.exists():
        emit(
            {
                "decision": "block",
                "reason": "Before compaction, recreate .codex/ivc_research_state.json so the decipherment frontier survives context loss.",
            }
        )
        return
    empty()


def event_post_compact(payload):
    log_event("PostCompact", payload, note="compact_done_sessionstart_compact_will_inject_image_context")
    empty()


def event_permission_request(payload):
    log_event("PermissionRequest", payload, note="approval_policy_never_guard")
    text = (
        "Permission hook: approvals are not the work. If permission handling appears, keep focus on the research claim and avoid approval-theater detours."
    )
    hook_context("PermissionRequest", text)


def final_has_research_delta(message):
    if not message.strip():
        return False
    lowered = message.lower()
    admin_pass = any(token in lowered for token in ["hook", ".codex", "codex config", "hooks.json"])
    if admin_pass:
        return True
    evidence_terms = [
        "evidence",
        "source",
        "side",
        "sign",
        "slot",
        "allograph",
        "graphem",
        "cisi",
        "harappa",
        "mohenjo",
        "accepted",
        "rejected",
        "unresolved",
        "next gate",
        "hypothesis",
        "claim",
        "translation",
    ]
    has_evidence_term = any(term in lowered for term in evidence_terms)
    has_gate = any(term in lowered for term in ["next gate", "next decisive", "decision gate", "blocked by", "survives", "dies", "fails"])
    return has_evidence_term and has_gate


def last_assistant_message_from_transcript(path_value):
    if not path_value:
        return ""
    try:
        path = Path(str(path_value))
        if not path.exists():
            return ""
        last_text = ""
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                row = json.loads(line)
            except Exception:
                continue
            payload = row.get("payload") if isinstance(row, dict) else None
            if not isinstance(payload, dict):
                continue
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                parts = []
                for item in payload.get("content") or []:
                    if isinstance(item, dict):
                        value = item.get("text") or item.get("content")
                        if isinstance(value, str):
                            parts.append(value)
                if parts:
                    last_text = "\n".join(parts)
            elif payload.get("type") == "response_item":
                inner = payload.get("payload")
                if isinstance(inner, dict) and inner.get("type") == "message" and inner.get("role") == "assistant":
                    parts = []
                    for item in inner.get("content") or []:
                        if isinstance(item, dict):
                            value = item.get("text") or item.get("content")
                            if isinstance(value, str):
                                parts.append(value)
                    if parts:
                        last_text = "\n".join(parts)
        return last_text
    except Exception:
        return ""


def event_stop(payload):
    killed = reap_stale_project_runs()
    log_event("Stop", payload, note="final_gate")
    if payload.get("stop_hook_active"):
        empty()
        return
    message = str(payload.get("last_assistant_message") or "")
    if not message:
        message = last_assistant_message_from_transcript(payload.get("transcript_path"))
    if not message:
        empty()
        return
    if final_has_research_delta(message):
        empty()
        return
    emit(
        {
            "decision": "block",
            "reason": (
                "Continue. The final response is missing a concrete IVC research delta or next decision gate. "
                "State what claim changed, what evidence supports it, and the next source/sign/side/slot gate. "
                "If this was hook/admin work, state exactly what hook files changed and what behavior they enforce."
            ),
        }
    )


def main():
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    payload = read_stdin_json()
    try:
        if event == "SessionStart":
            event_session_start(payload)
        elif event == "UserPromptSubmit":
            event_user_prompt_submit(payload)
        elif event == "PreToolUse":
            event_pre_tool_use(payload)
        elif event == "PostToolUse":
            event_post_tool_use(payload)
        elif event == "PreCompact":
            event_pre_compact(payload)
        elif event == "PostCompact":
            event_post_compact(payload)
        elif event == "PermissionRequest":
            event_permission_request(payload)
        elif event == "Stop":
            event_stop(payload)
        else:
            empty()
    except Exception as exc:
        # Hooks should not brick the workspace because of a script bug.
        emit({"suppressOutput": True, "reason": f"IVC hook error: {exc}"})


if __name__ == "__main__":
    main()
