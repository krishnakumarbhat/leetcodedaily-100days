# NeetCode 150 — PDF study guide pipeline

Generates `../dist/NeetCode150_Study_Guide.pdf`: a bookmarked, syntax-highlighted
A4 study guide covering all 153 problems in `../neetcode150/` (the full NeetCode
150 plus three extras present in the repo), in canonical category order.

## Rebuild

```bash
python3 extract.py     # -> manifest.json    canonical order, titles, difficulty
python3 harvest.py     # -> harvest.json     mined headers + de-boilerplated kernels
python3 compose.py     # -> content/*.json   harvest merged with the authored payload
python3 validate.py    # contract check      exit 1 on any real gap
python3 build.py       # -> ../dist/*.pdf    3x pdflatex so TOC + bookmarks resolve
```

`build.py --only 07_trees` renders a single category; `--no-compile` stops after
emitting `build/study_guide.tex`.

## The two content sources

| source | supplies |
| --- | --- |
| `harvest.py` (reads the solutions) | PROBLEM / INTUITION text, per-approach commentary and stated complexities, data-structure deep-dives, and code kernels extracted from the real `Solution_*` classes |
| `authored.py` + `kernels.json` (hand-written) | intent, bounds, ASCII state traces, language-mechanics paragraphs, structure alternatives, interview traps, loop invariants, and 3 intuition-check questions per problem |

`compose.py` is the join: `authored` wins where present, `harvest` fills the
rest, and `why.py` derives a one-line complexity justification when none was
authored.

## Layout

- `latexkit.py` — rendering primitives: Pygments→LaTeX highlighting, the
  side-by-side two-column Python|C++ panel, ASCII diagram box, escaping.
- `latexkit_preamble.py` — all `\usepackage`s, colours and custom environments.
- `why.py` — complexity-justification templates and per-category
  language-mechanics fallbacks.
- `manual_kernels.py` / `kernels.json` — hand-corrected kernels for the 28
  problems whose C++ (or Python) kernel the extractor could not recover.
- `content/` — generated per-category JSON, the direct input to `build.py`.
- `build/` — intermediate `.tex` and `.aux` artifacts.

## Contract

`CONTENT_SPEC.md` documents the record schema. `validate.py` enforces it: every
approach needs a `name`, `aha`, `py`, `cpp`, `time`, `space` and `why`; every
problem needs `one_liner`, `core_objective`, `bounds`, `diagram`, `cpp_vs_py`,
2+ `cpp_alts`, 2+ `py_alts`, `trap`, `invariant` and exactly 3 questions.
The only tolerated flags are cosmetic ones (a diagram a few rows taller than
the guideline, a kernel line a few columns over) — those render fine inside the
minipage panels.