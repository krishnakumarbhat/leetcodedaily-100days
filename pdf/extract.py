#!/usr/bin/env python3
"""
extract.py --- Build the canonical manifest of the NeetCode 150 set.

Purpose : Walk ../neetcode150/<category>/ and pull title / difficulty /
          category / approach names / stated complexity out of the headers
          of every solution file, so the PDF builder and every content
          sub-agent agree on ONE canonical ordering.
Inputs  : the neetcode150/ directory (Python sources are the source of
          truth; C++ is only checked for presence).
Outputs : pdf/manifest.json  (ordered list of problem records)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEETCODE = ROOT / "neetcode150"
OUT = Path(__file__).resolve().parent / "manifest.json"

# Canonical NeetCode category order (directory name -> human title).
CATEGORY_ORDER = [
    ("01_arrays_and_hashing", "Arrays & Hashing"),
    ("02_two_pointers", "Two Pointers"),
    ("03_sliding_window", "Sliding Window"),
    ("04_stack", "Stack"),
    ("05_binary_search", "Binary Search"),
    ("06_linked_list", "Linked List"),
    ("07_trees", "Trees"),
    ("08_tries", "Tries"),
    ("09_heap_priority_queue", "Heap / Priority Queue"),
    ("10_backtracking", "Backtracking"),
    ("11_graphs", "Graphs"),
    ("12_advanced_graphs", "Advanced Graphs"),
    ("13_1d_dp", "1-D Dynamic Programming"),
    ("14_2d_dp", "2-D Dynamic Programming"),
    ("15_greedy", "Greedy"),
    ("16_intervals", "Intervals"),
    ("17_math_and_geometry", "Math & Geometry"),
    ("18_bit_manipulation", "Bit Manipulation"),
]

# 1143 is a 1-D DP problem; a stray copy also sits in 14_2d_dp/.
MISFILED = {"14_2d_dp/1143_longest_common_subsequence"}

RE_TITLE = re.compile(r"LeetCode\s+(\d+)\s*:\s*(.+?)\s*\((Easy|Medium|Hard)\)", re.S)
RE_APPROACH = re.compile(r"^APPROACH\s+(\d+)\s*[—\-:]*\s*(.+?)\s*$", re.M)
RE_COMPLEXITY = re.compile(r"Time\s+Complexity\s*:\s*(.+?)\s{2,}Space\s+Complexity\s*:\s*(.+?)\s*$", re.M)


def parse_header(text: str) -> dict:
    """Purpose: pull number/title/difficulty + approach list out of a solution header."""
    m = RE_TITLE.search(text)
    num, title, diff = (m.group(1), m.group(2).strip(), m.group(3)) if m else ("", "", "")
    title = re.sub(r"\s+", " ", title)
    approaches = [re.sub(r"\s+", " ", a).strip(" —-:") for _, a in RE_APPROACH.findall(text)]
    return {"number": num, "title": title, "difficulty": diff, "approaches": approaches}


def main() -> None:
    records: list[dict] = []
    for dirname, cat_title in CATEGORY_ORDER:
        folder = NEETCODE / dirname
        py_files = sorted(p for p in folder.glob("*.py") if "__pycache__" not in str(p))
        for py in py_files:
            rel = f"{dirname}/{py.stem}"
            if rel in MISFILED:
                continue
            head = parse_header(py.read_text(encoding="utf-8", errors="replace"))
            cpp = py.with_suffix(".cpp")
            records.append(
                {
                    "key": rel,
                    "category_dir": dirname,
                    "category": cat_title,
                    "number": head["number"] or py.stem[:4],
                    "slug": py.stem,
                    "title": head["title"] or py.stem[5:].replace("_", " ").title(),
                    "difficulty": head["difficulty"] or "?",
                    "approaches": head["approaches"],
                    "py": str(py.relative_to(ROOT)),
                    "cpp": str(cpp.relative_to(ROOT)) if cpp.exists() else "",
                }
            )

    OUT.write_text(json.dumps(records, indent=2), encoding="utf-8")
    by_cat: dict[str, int] = {}
    for r in records:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    print(f"total problems: {len(records)}")
    for dirname, cat_title in CATEGORY_ORDER:
        print(f"  {cat_title:<28} {by_cat.get(cat_title, 0)}")


if __name__ == "__main__":
    main()