#!/usr/bin/env python3
"""
build.py --- Compile the NeetCode 150 study-guide PDF.

Purpose : Merge manifest.json (canonical order / titles / difficulty) with the
          per-category content JSON written by the content sub-agents, render a
          bookmarked pdflatex document, and compile it twice so the TOC and
          PDF bookmarks resolve.
Inputs  : pdf/manifest.json + pdf/content/*.json
Outputs : dist/NeetCode150_Study_Guide.pdf
Usage   : python3 build.py [--only 07_trees] [--no-compile]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from latexkit import build_tex  # noqa: E402

DIST = HERE.parent / "dist"
BUILD = HERE / "build"


def load_records(only: str | None) -> list[dict]:
    """Purpose: attach per-problem content JSON onto the canonical manifest."""
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    blob: dict[str, dict] = {}
    for f in sorted((HERE / "content").glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        items = data["problems"] if isinstance(data, dict) else data
        for it in items:
            blob[it["key"]] = it

    out: list[dict] = []
    missing: list[str] = []
    for m in manifest:
        if only and only not in m["category_dir"]:
            continue
        c = blob.get(m["key"])
        if not c:
            missing.append(m["key"])
            c = {
                "one_liner": "content pending",
                "core_objective": "(content not yet generated)",
                "approaches": [],
                "questions": [],
            }
        rec = {**m, **c}
        rec["approaches"] = [a for a in rec.get("approaches", []) if isinstance(a, dict)]
        out.append(rec)
    if missing:
        print(f"[warn] {len(missing)} problem(s) without content JSON:", file=sys.stderr)
        for k in missing[:200]:
            print(f"        {k}", file=sys.stderr)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="substring filter on the category directory, e.g. 07_trees")
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--out", default="NeetCode150_Study_Guide.pdf")
    args = ap.parse_args()

    records = load_records(args.only)
    covered = sum(1 for r in records if r.get("approaches"))
    print(f"rendering {len(records)} problems ({covered} with full content)")

    metadata = {
        "title": "NeetCode 150",
        "subtitle": "Algorithmic Intuition Study Guide --- Python \\textrightarrow{} C++",
        "author": "Generated from the local neetcode150/ solution set",
        "date": dt.date.today().isoformat(),
    }
    tex = build_tex(records, metadata)

    BUILD.mkdir(exist_ok=True)
    main_tex = BUILD / "study_guide.tex"
    main_tex.write_text(tex, encoding="utf-8")
    print(f"wrote {main_tex} ({len(tex)/1024:.0f} KiB of TeX)")

    if args.no_compile:
        return

    DIST.mkdir(exist_ok=True)
    passes = 3
    for i in range(1, passes + 1):
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-jobname", "study_guide", "-output-directory", str(BUILD), str(main_tex)],
            capture_output=True, text=True,
        )
        log = BUILD / "study_guide.log"
        tail = log.read_text(errors="replace")[-4000:] if log.exists() else proc.stdout[-4000:]
        ok = (BUILD / "study_guide.pdf").exists()
        print(f"  pdflatex pass {i}/{passes}: pdf={'yes' if ok else 'NO'} rc={proc.returncode}")
        if not ok:
            print(tail)
            sys.exit(1)

    produced = BUILD / "study_guide.pdf"
    target = DIST / args.out
    target.write_bytes(produced.read_bytes())
    size_mb = target.stat().st_size / 1_048_576
    print(f"\n>>> {target}  ({size_mb:.1f} MB)")

    pages = subprocess.run(["pdfinfo", str(target)], capture_output=True, text=True).stdout
    if pages:
        for line in pages.splitlines():
            if line.startswith(("Pages", "Title")):
                print("    " + line)


if __name__ == "__main__":
    main()