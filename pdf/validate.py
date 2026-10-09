#!/usr/bin/env python3
"""
validate.py --- Lint every pdf/content/*.json against the content contract.

Purpose : Catch schema drift, over-long kernels, oversized ASCII diagrams and
          wrong `key` strings before they reach pdflatex, and report coverage
          against the canonical manifest.
Inputs  : pdf/content/*.json + pdf/manifest.json
Outputs : a per-file issue report on stdout; exit code 1 if anything is broken.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQ = ["key", "one_liner", "core_objective", "bounds", "approaches", "diagram",
       "cpp_vs_py", "cpp_alts", "py_alts", "trap", "invariant", "questions"]
AREQ = ["name", "aha", "py", "cpp", "time", "space", "why"]
MAX_KERNEL_LINES = 13
MAX_KERNEL_COLS = 80
MAX_DIAG_ROWS = 26
MAX_DIAG_COLS = 68
BAD_CHARS = set("│─┌┐└┘├┤┬┴┼━┃┏┓┗┛")


def check(path: Path, known: set[str], issues: list[str]) -> set[str]:
    """Purpose: validate one content file. Inputs: path + known keys. Output: set of covered keys."""
    tag = path.name
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:                      # noqa: BLE001
        issues.append(f"{tag}: invalid JSON -> {exc}")
        return set()

    probs = data["problems"] if isinstance(data, dict) else data
    covered: set[str] = set()

    for p in probs:
        key = p.get("key", "<no key>")
        covered.add(key)
        if key not in known:
            issues.append(f"{tag}: unknown key {key!r}")

        for field in REQ:
            if field not in p or p[field] in ("", [], {}):
                issues.append(f"{tag}:{key}: empty/missing {field!r}")
        if p.get("category_note") is None and field_ok(p, "approaches"):
            pass

        apps = p.get("approaches") or []
        if not 1 <= len(apps) <= 3:
            issues.append(f"{tag}:{key}: {len(apps)} approaches (want 1-3)")
        for a in apps:
            for field in AREQ:
                if field not in a or a[field] in ("", [], {}):
                    issues.append(f"{tag}:{key}: approach missing {field!r}")
            for lang in ("py", "cpp"):
                code = a.get(lang, "")
                rows = code.strip().splitlines()
                if not 1 <= len(rows) <= MAX_KERNEL_LINES:
                    issues.append(f"{tag}:{key}: {lang} kernel has {len(rows)} lines")
                wide = max((len(r) for r in rows), default=0)
                if wide > MAX_KERNEL_COLS:
                    issues.append(f"{tag}:{key}: {lang} kernel line {wide} cols > {MAX_KERNEL_COLS}")
                for banned in ("import ", "#include", "class Solution", "int main", "__main__"):
                    if banned in code:
                        issues.append(f"{tag}:{key}: {lang} kernel has boilerplate {banned!r}")

        diag = (p.get("diagram") or "").splitlines()
        if len(diag) > MAX_DIAG_ROWS:
            issues.append(f"{tag}:{key}: diagram {len(diag)} rows > {MAX_DIAG_ROWS}")
        wide = max((len(r) for r in diag), default=0)
        if wide > MAX_DIAG_COLS:
            issues.append(f"{tag}:{key}: diagram {wide} cols > {MAX_DIAG_COLS}")
        for row in diag:
            bad = BAD_CHARS.intersection(row)
            if bad:
                issues.append(f"{tag}:{key}: diagram has unicode box chars {sorted(bad)}")
                break

        if len(p.get("questions") or []) != 3:
            issues.append(f"{tag}:{key}: {len(p.get('questions') or [])} questions (want 3)")
        for q in p.get("questions") or []:
            if "q" not in q or "a" not in q or not q["q"].strip() or not q["a"].strip():
                issues.append(f"{tag}:{key}: question missing q/a")
        if len(p.get("cpp_alts") or []) < 2 or len(p.get("py_alts") or []) < 2:
            issues.append(f"{tag}:{key}: want >=2 cpp_alts and >=2 py_alts")
    return covered


def field_ok(p: dict, name: str) -> bool:
    """Purpose: tiny guard so the unused-branch above stays readable."""
    return name in p


def main() -> int:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    known = {m["key"] for m in manifest}

    issues: list[str] = []
    covered: set[str] = set()
    files = sorted(f for f in (HERE / "content").glob("*.json") if not f.name.startswith(("SMOKE", "TEST")))
    for f in files:
        got = check(f, known, issues)
        dupes = covered & got
        if dupes:
            issues.append(f"{f.name}: duplicate keys {sorted(dupes)}")
        covered |= got

    missing = sorted(known - covered)
    print(f"content files : {len(files)}")
    print(f"covered       : {len(covered)}/{len(known)}")
    print(f"missing ({len(missing)}):")
    for m in missing:
        print("   -", m)
    print(f"issues        : {len(issues)}")
    for i in issues[:120]:
        print("   !", i)
    return 1 if (issues or missing) else 0


if __name__ == "__main__":
    sys.exit(main())