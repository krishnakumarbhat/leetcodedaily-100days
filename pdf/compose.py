#!/usr/bin/env python3
"""
compose.py --- Merge harvested solution material with the authored analysis.

Purpose : `harvest.py` mines PROBLEM / INTUITION / APPROACH commentary / stated
          complexities / data-structure deep-dives / de-boilerplated code kernels
          out of neetcode150/. This script joins that with `authored.py` -- the
          genuinely new writing: bounds, visual state traces, language-mechanics
          notes, structure alternatives, interview traps and the three intuition
          questions -- and writes pdf/content/<NN_category>.json ready for build.

Inputs  : pdf/harvest.json, pdf/authored.py, pdf/manual_kernels.py
Outputs : pdf/content/*.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import why                           # noqa: E402
import authored                      # noqa: E402
import manual_kernels                # noqa: E402

CATEGORY_SLUG = {
    "01_arrays_and_hashing": "arrays_hashing",
    "02_two_pointers": "two_pointers",
    "03_sliding_window": "sliding_window",
    "04_stack": "stack",
    "05_binary_search": "binary_search",
    "06_linked_list": "linked_list",
    "07_trees": "trees",
    "08_tries": "tries",
    "09_heap_priority_queue": "heap_pq",
    "10_backtracking": "backtracking",
    "11_graphs": "graphs",
    "12_advanced_graphs": "advanced_graphs",
    "13_1d_dp": "dp_1d",
    "14_2d_dp": "dp_2d",
    "15_greedy": "greedy",
    "16_intervals": "intervals",
    "17_math_and_geometry": "math_geometry",
    "18_bit_manipulation": "bits",
}


def sentences(text: str) -> list[str]:
    """Purpose: split prose into sentences, keeping abbreviations intact."""
    text = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[.:!?])\s+(?=[A-Z0-9`\"'(])", text)
    return [p for p in parts if p]


def clean_prose(text: str) -> str:
    """Purpose: tidy harvested prose into guide-quality paragraphs."""
    out = []
    for para in (p.strip() for p in re.split(r"\n\s*\n", text)):
        if not para:
            continue
        flat = re.sub(r"[ \t]+", " ", para).strip()
        # drop the repo's ASCII bullet glyphs and stray separator rules
        flat = re.sub(r"^[-•·*]\s*", "", flat)
        flat = re.sub(r"^-{3,}.*$", "", flat)
        flat = re.sub(r"^(Purpose|Inputs|Outputs)\s*:.*$", "", flat)
        if flat:
            out.append(flat)
    return "\n\n".join(out)


def kernel_text(lines: list[str], limit: int = 8) -> str:
    """Purpose: join harvested kernel lines, de-indented one level, capped."""
    if not lines:
        return ""
    body = [ln for ln in lines if ln.strip()]
    if len(body) > 1:
        pad = min(len(ln) - len(ln.lstrip()) for ln in body)
        body = [ln[pad:] if len(ln) > pad else ln for ln in body]
    return "\n".join(body[:limit])


def build() -> None:
    harvest = {r["key"]: r for r in json.loads((HERE / "harvest.json").read_text(encoding="utf-8"))}
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    out_dir = HERE / "content"
    out_dir.mkdir(exist_ok=True)
    for stale in out_dir.glob("[0-9]*.json"):
        stale.unlink()

    buckets: dict[str, list[dict]] = {}
    thin = 0
    for m in manifest:
        key = m["key"]
        h = harvest.get(key, {})
        a = authored.DATA.get(key, {})
        hand = manual_kernels.KERNELS.get(key, {})

        kern = {**authored.KERNELS.get(key, {}), **(a.get("kernels") or {}), **hand}
        kern = {(int(k) if str(k).isdigit() else k): v for k, v in kern.items()}
        happs = h.get("approaches", [])[:3]
        if not happs and kern:
            happs = [{"name": F"Approach {i + 1}", "prose": "", "time": None,
                      "space": None} for i in sorted(kern, key=lambda x: (isinstance(x, str), x))]
        apps = []
        for i, ap in enumerate(happs):
            slot = kern.get(i, kern.get(ap["name"], {}))
            py = slot.get("py") or kernel_text(ap.get("py", []))
            cpp = slot.get("cpp") or kernel_text(ap.get("cpp", []))
            if not cpp or not py:
                thin += 1
            apps.append({
                "name": ap["name"],
                "aha": clean_prose(ap.get("prose", "")) or clean_prose(h.get("intuition", ""))
                        or ap["name"] + " -- see the kernel below.",
                "py": py,
                "cpp": cpp,
                "time": ap.get("time") or "?",
                "space": ap.get("space") or "?",
                "why": why.why_for(ap["name"], ap.get("time") or "?",
                                    ap.get("space") or "?"),
            })

        prob = clean_prose(h.get("problem", ""))
        sents = sentences(prob)
        record = {
            "key": key,
            "one_liner": a.get("one_liner", ""),
            "core_objective": a.get("core_objective", " ".join(sents[:2]) or h.get("intuition", "")),
            "bounds": a.get("bounds", ""),
            "approaches": apps,
            "diagram": a.get("diagram", ""),
            "cpp_vs_py": (a.get("cpp_vs_py", "") or clean_prose(h.get("deep_dive", ""))[:1400]
                         or why.cpp_vs_py_default(h, m)),
            "cpp_alts": a.get("cpp_alts", []),
            "py_alts": a.get("py_alts", []),
            "trap": a.get("trap", ""),
            "invariant": a.get("invariant", ""),
            "questions": a.get("questions", [])[:3],
        }
        if a.get("category_note"):
            record["category_note"] = a["category_note"]
        buckets.setdefault(m["category_dir"], []).append(record)

    for dirname, recs in buckets.items():
        path = out_dir / f"{dirname}_{CATEGORY_SLUG.get(dirname, dirname)}.json"
        path.write_text(json.dumps({"problems": recs}, indent=1), encoding="utf-8")

    total = sum(len(v) for v in buckets.values())
    print(f"composed {total} problems into {len(buckets)} category files")
    print(f"approaches with a missing language kernel: {thin}")


if __name__ == "__main__":
    build()