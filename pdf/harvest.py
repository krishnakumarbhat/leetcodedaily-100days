#!/usr/bin/env python3
"""
harvest.py --- Mine the existing neetcode150/ solution headers + code.

Purpose : The solution files already carry a hand-written PROBLEM, INTUITION,
          per-APPROACH commentary with stated complexities, DEEP DIVE notes and
          REAL LIFE notes. This script harvests those (per language, aligned by
          approach class name) together with a de-boilerplated code kernel, so
          the PDF payload only has to be authored where it adds new value:
          bounds, diagrams, traps, invariants and the intuition questions.

Inputs  : neetcode150/**/*.py and *.cpp
Outputs : pdf/harvest.json -- one record per problem, keyed like manifest.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEETCODE = ROOT / "neetcode150"
OUT = Path(__file__).resolve().parent / "harvest.json"

TRIVIAL_PY = {
    "pass", "return None", "return []", "return {}", "return False", "return True",
    "return 0", "return -1", "return \"\"", "raise NotImplementedError",
    "from __future__ import annotations",
}
TRIVIAL_CPP = {"return {};", "return -1;", "return 0;"}

# class names are wildly inconsistent across the repo: Solution_OnePassHashmap,
# SolutionOne, Solution_1, even a bare `class Solution:` -- accept them all.
RE_PY_CLASS = re.compile(r"^class\s+Solution_?(\w*)\s*[({:]")

SEC_RE = re.compile(
    r"^(PROBLEM|INTUITION|APPROACH\s+\d+.*?|DEEP DIVE.*?|DATA STRUCTURE.*?|"
    r"LANGUAGE.*?|MEMORY.*?|PERFORMANCE.*?|REAL LIFE|EXAMPLE.*?|EDGE CASES.*?|"
    r"COMPLEXITY.*?|KEY INSIGHT.*?|WHY IT WORKS.*?)$"
)


# --------------------------------------------------------------------------
# header docstring -> {section name: body}
# --------------------------------------------------------------------------
def split_sections(doc: str) -> dict[str, list[str]]:
    """Purpose: slice a header docstring into its ALL-CAPS sections."""
    out: dict[str, list[str]] = {}
    cur: str | None = None
    for raw in doc.splitlines():
        line = re.sub(r"^\s*\*\s?", "", raw.rstrip())
        s = line.strip()
        if s and line == s:
            m = SEC_RE.match(s)
            if m:
                cur = m.group(1).strip()
                out.setdefault(cur, [])
                continue
        if cur:
            out[cur].append(line)
    return {k: [ln.rstrip() for ln in v] for k, v in out.items()}


def join(lines: list[str]) -> str:
    """Purpose: re-wrap an indented header block into flowing prose paragraphs."""
    paras, cur = [], []
    for ln in lines:
        if not ln.strip():
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(ln.strip())
    if cur:
        paras.append(" ".join(cur))
    return "\n\n".join(p for p in paras if p)


RE_APPROACH_HEAD = re.compile(r"^APPROACH\s+(\d+)\s*[—\-–:]*\s*(.+?)\s*$")
RE_TIME = re.compile(r"Time\s+Complexity\s*:\s*(.+?)\s{2,}(?:Space|MEMORY)\s+Complexity\s*:\s*(.+?)\s*$",
                     re.I | re.M)
RE_TIME2 = re.compile(r"Time\s+Complexity\s*:\s*(.+?)\s*$", re.I | re.M)
RE_SPACE2 = re.compile(r"(?:Space|MEMORY)\s+Complexity\s*:\s*(.+?)\s*$", re.I | re.M)


def parse_approaches(doc: str) -> list[dict]:
    """Purpose: pull each APPROACH block: name, prose, stated time and space."""
    lines = doc.splitlines()
    marks = [(i, m.group(1), m.group(2)) for i, ln in enumerate(lines)
             if (m := RE_APPROACH_HEAD.match(ln.strip()))]
    out = []
    for idx, (ln, num, name) in enumerate(marks):
        stop = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        block = "\n".join(lines[ln + 1:stop])
        t, sp = None, None
        if m := RE_TIME.search(block):
            t, sp = m.group(1).strip(), m.group(2).strip()
        else:
            if m := RE_TIME2.search(block):
                t = m.group(1).strip()
            if m := RE_SPACE2.search(block):
                sp = m.group(1).strip()
        prose = re.split(r"\n\s*(?:Time|Space|MEMORY)\s+Complexity\s*:", block)[0]
        out.append({"name": name.strip(), "prose": join(prose.splitlines()), "time": t, "space": sp})
    return out


# --------------------------------------------------------------------------
# code kernels
# --------------------------------------------------------------------------
def _strip_py_noise(body: list[str]) -> list[str]:
    """Purpose: drop docstrings, comments and empty lines from a Python body."""
    out, in_doc, quote = [], False, ""
    for ln in body:
        s = ln.strip()
        if in_doc:
            if quote in s:
                in_doc = False
            continue
        if s.startswith(('"""', "'''")):
            quote = s[:3]
            if len(s) <= 3 or quote not in s[3:]:
                in_doc = True
            continue
        if s.startswith("#") or not s:
            continue
        out.append(ln.rstrip())
    return out


def _collapse(lines: list[str]) -> list[str]:
    """Purpose: fold single-statement guarded returns onto one line, drop `pass`."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        cur = lines[i]
        if cur.strip() in TRIVIAL_PY:
            i += 1
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        indent = len(cur) - len(cur.lstrip())
        if (cur.rstrip().endswith(":") and nxt.strip()
                and nxt.strip() != "else:" and len(nxt) - len(nxt.lstrip()) == indent + 4
                and " " not in nxt.strip()[:0]):
            merged = cur.rstrip() + " " + nxt.strip()
            if len(merged) <= 68 and not merged.strip().startswith(("for ", "while ", "if ", "def ")):
                out.append(merged)
                i += 2
                continue
        if cur.strip() == "else:" and out and not out[-1].rstrip().endswith((":", ")", "]")):
            merged = out[-1].rstrip() + " else: " + nxt.strip() if nxt.strip() else cur
            if len(merged) <= 68:
                out[-1] = merged
                i += 2
                continue
        out.append(cur)
        i += 1
    return out


def python_kernels(src: str) -> dict[str, list[str]]:
    """Purpose: map Solution_<Name> -> de-boilerplated kernel lines from a .py file."""
    lines = src.splitlines()
    out: dict[str, list[str]] = {}
    i = 0
    while i < len(lines):
        m = RE_PY_CLASS.match(lines[i])
        if not m:
            i += 1
            continue
        name = m.group(1)
        j, body, in_def = i + 1, [], False
        while j < len(lines):
            ln = lines[j]
            if ln and not ln.startswith((" ", "\t")):
                break
            if re.match(r"^\s+def \w+\(", ln):
                in_def = True
            if in_def:
                if ln.strip().startswith('"""') or ln.strip().startswith("'''"):
                    in_def = "doc"
                elif in_def == "doc":
                    if '"""' in ln or "'''" in ln:
                        in_def = True
                else:
                    body.append(ln)
            j += 1
        body = _strip_py_noise(body)
        body = [b for b in body if b.strip() != "self"]
        body = [b for b in body if not re.match(r"^\s*def \w+\(", b)]
        out[name] = _collapse(body)[:10]
        i = j
    return out


RE_CPP_CLASS = re.compile(r"^class\s+(\w+)")
# A declaration line: optional modifiers, a (possibly templated / qualified / pointer)
# return type, a name, and an argument list.  `;`-terminated lines are rejected so
# ordinary call statements can never match.
RE_CPP_SIG = re.compile(r"^\s{0,8}(?:static\s+|inline\s+|virtual\s+|const\s+|unsigned\s+)*"
                        r"(?:[A-Za-z_]\w*::)*[A-Za-z_][\w:<>,\s*&]*?\b\w+\s*\([^;]*$")
RE_HELPER = {"walk", "helper", "_", "main", "bench"}


def _fn_body(lines: list[str], sig: int) -> list[str] | None:
    """Purpose: body lines of the function whose signature starts at `sig`.

    Tolerates the brace sitting on its own line, which this repo does often.
    """
    k = sig
    while k < len(lines) and "{" not in lines[k]:
        k += 1
    if k >= len(lines):
        return None
    if "{" in lines[k] and lines[k].strip() != "{":   # brace shares the signature line
        k += 1
    depth = 0
    out = []
    while k < len(lines):
        depth += lines[k].count("{") - lines[k].count("}")
        if depth > 0:
            out.append(lines[k])
        elif out:
            break
        k += 1
    return out


def _clean_body(body: list[str]) -> list[str]:
    """Purpose: strip comments/blank lines/trivial returns, then fold short blocks."""
    body = [b for b in body
            if b.strip() and not b.strip().startswith(("//", "/*", "*"))
            and b.strip() not in TRIVIAL_CPP]
    return _collapse_cpp(body)[:10]


def cpp_kernels(src: str) -> dict[str, list[str]]:
    """Purpose: map Solution_<Name> -> de-boilerplated kernel lines from a .cpp file.

    Handles three shapes found in the repo: `class Solution_X { ... }` with the
    brace on the same line, the same with the brace on the next line, and files
    that use free functions plus `main()` instead of a class at all.
    """
    lines = src.splitlines()
    out: dict[str, list[str]] = {}
    scoped: list[tuple[str, list[str]]] = []

    i = 0
    while i < len(lines):
        m = RE_CPP_CLASS.match(lines[i])
        if not m:
            i += 1
            continue
        name = m.group(1)
        j = i
        while j < len(lines) and "{" not in lines[j]:
            j += 1
        if j >= len(lines):
            i += 1
            continue
        depth, end = 0, j
        while end < len(lines):
            depth += lines[end].count("{") - lines[end].count("}")
            end += 1
            if depth <= 0:
                break
        for k in range(j + 1, max(j + 1, end - 1)):
            sig_name = re.search(r"\b(\w+)\s*\(", lines[k].rstrip())
            if RE_CPP_SIG.match(lines[k]) and ";" not in lines[k] and lines[k].rstrip().endswith((")", "{")):
                body = _fn_body(lines, k)
                if body and (not sig_name or sig_name.group(1) not in RE_HELPER):
                    scoped.append((name, _clean_body(body)))
        i = max(end, i + 1)

    if scoped:
        for name, kernel in scoped:                     # keep the longest per class
            if len(kernel) > len(out.get(name, [])):
                out[name] = kernel
        return out

    for k, line in enumerate(lines):                     # free-function fallback
        if re.match(r"^\w[\w:<>,&\s*]*\b\w+\s*\(", line) and ";" not in line:
            body = _fn_body(lines, k)
            if body:
                nm = re.search(r"\b(\w+)\s*\(", line)
                if nm and nm.group(1) != "main":
                    out.setdefault(nm.group(1), _clean_body(body))
    return out


def _collapse_cpp(lines: list[str]) -> list[str]:
    """Purpose: fold short guarded one-liners in C++ bodies."""
    out: list[str] = []
    for ln in lines:
        s = ln.strip()
        if out and out[-1].rstrip().endswith("{") and len(ln) <= 62 and s and not s.startswith("#"):
            out[-1] = out[-1].rstrip() + " " + s
        else:
            out.append(ln.rstrip())
    return out


STOP = {"per", "and", "the", "of", "a", "an", "to", "in", "on", "with", "no", "for",
        "is", "are", "best", "simplest", "optimal", "memory", "contrast", "kernel",
        "brute", "force", "v2", "same", "idea", "style", "without", "only", "at",
        "one", "two", "up", "out", "case", "via", "using", "by", "from"}


def norm(name: str) -> str:
    """Purpose: loose key so `OnePassHashmap` and `One-pass hash map (BEST)` line up."""
    name = re.sub(r"[(\[][^)\]]*[)\]]", "", name)      # drop (BEST) / [contrast]
    name = re.sub(r"\s*[—\u2013\-:]\s.*$", "", name)            # drop " -- variant"
    return re.sub(r"[^a-z0-9]", "", name.lower())


def tokens(name: str) -> set[str]:
    """Purpose: content words of an approach name, for fuzzy class matching."""
    return {w for w in re.findall(r"[A-Za-z]{2,}", name.lower()) if w not in STOP}


def score(app: str, cls: str) -> int:
    """Purpose: similarity of an approach header name to a Solution_<Name> class."""
    a, c = norm(app), norm(cls)
    if a and a == c:
        return 100
    if c and (c in a or a in c):
        return 60
    ta, tc = tokens(app), tokens(cls)
    if not ta or not tc:
        return 0
    return int(40 * len(ta & tc) / len(ta | tc))


def assign(apps: list[dict], tables: list[dict]) -> None:
    """Purpose: bind each approach to a class per language.

    Name similarity first; anything left over falls back to ORDINAL position,
    because the class declarations always appear in the same order as the
    APPROACH headers in both the .py and the .cpp.
    """
    for order, table in enumerate(tables):
        names = list(table)
        used: set[str] = set()
        for a in apps:
            best, best_score = "", 0
            for cls in names:
                if cls in used or not cls:
                    continue
                sc = score(a["name"], cls)
                if sc > best_score:
                    best, best_score = cls, sc
            if best_score >= 30:
                used.add(best)
                a.setdefault("_cls", {})[order] = best
        for i, a in enumerate(apps):
            if order in a.get("_cls", {}):
                continue
            for cls in names:                       # ordinal fallback
                if cls and cls not in used:
                    used.add(cls)
                    a.setdefault("_cls", {})[order] = cls
                    break


def main() -> None:
    recs = []
    for py in sorted(NEETCODE.glob("*/*.py")):
        if "__pycache__" in str(py):
            continue
        rel = f"{py.parent.name}/{py.stem}"
        src = py.read_text(encoding="utf-8", errors="replace")
        doc = src.split('"""')[1] if src.count('"""') >= 2 else ""
        secs = split_sections(doc)
        cps = py.with_suffix(".cpp")
        cpp_src = cps.read_text(encoding="utf-8", errors="replace") if cps.exists() else ""
        cpp_doc = cpp_src.split("/*")[1] if cpp_src.count("/*") >= 2 else ""
        cpp_secs = split_sections(cpp_doc)

        pyk = python_kernels(src)
        cppk = cpp_kernels(cpp_src)

        apps = parse_approaches(doc)
        if not apps:                              # no APPROACH headers: read the classes
            apps = [{"name": k.replace("_", " "), "prose": "", "time": None, "space": None}
                    for k in list(pyk) or list(cppk)]
        assign(apps, [pyk, cppk])
        for a in apps:
            cls = a.get("_cls", {})
            a["py"] = list(pyk.get(cls.get(0, ""), []))
            a["cpp"] = list(cppk.get(cls.get(1, ""), []))
            a.pop("_cls", None)

        recs.append({
            "key": rel,
            "problem": join(secs.get("PROBLEM", [])),
            "intuition": join(secs.get("INTUITION", [])),
            "real_life": join(secs.get("REAL LIFE", [])),
            "deep_dive": "\n\n".join(
                b for b in (
                    "\n\n".join(join(secs[k]) for k in secs
                                 if k.startswith(("DEEP DIVE", "DATA STRUCTURE", "LANGUAGE",
                                                  "MEMORY", "PERFORMANCE", "WHY IT WORKS",
                                                  "KEY INSIGHT"))),
                    "\n\n".join(join(cpp_secs[k]) for k in cpp_secs
                                 if k.startswith(("DEEP DIVE", "DATA STRUCTURE", "LANGUAGE",
                                                  "MEMORY", "PERFORMANCE", "WHY IT WORKS",
                                                  "KEY INSIGHT"))),
                ) if b.strip()),
            "approaches": [{k: v for k, v in a.items() if k != "_cls"} for a in apps],
        })

    OUT.write_text(json.dumps(recs, indent=1), encoding="utf-8")
    ok = sum(1 for r in recs if r["approaches"] and all(a["py"] for a in r["approaches"]))
    print(f"harvested {len(recs)} files | problems with full py kernels: {ok}")
    for r in recs[:3]:
        print(f"  {r['key']}: {len(r['approaches'])} approaches, "
              f"deep_dive {len(r['deep_dive'])} chars")


if __name__ == "__main__":
    main()