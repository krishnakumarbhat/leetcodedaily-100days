#!/usr/bin/env python3
"""
latexkit.py --- Rendering primitives for the NeetCode 150 study-guide PDF.

Purpose : Convert content JSON (problem records) into a single pdflatex-ready
          .tex file: escaped prose, Pygments-highlighted Python/C++ kernels
          laid out SIDE-BY-SIDE in two-column tables, boxed ASCII diagrams,
          and the section/command scaffolding.
Inputs  : records  -- list of dicts (see content schema)
          metadata -- dict with title/subtitle/author/date
Outputs : a LaTeX source string (the build driver writes it to disk).
"""

from __future__ import annotations

import html
import re
from pygments import lex
from pygments.lexers import PythonLexer, CppLexer
from pygments.token import Token

# --------------------------------------------------------------------------
# Colour palettes (Pygments token -> xcolor name, values in the preamble).
# --------------------------------------------------------------------------
PALETTE = {
    "tok.kw":      ("pykw",  "7C3AED"),  # keyword
    "tok.name":    ("pynm",  "1F2937"),  # identifier / builtin-ish
    "tok.func":    ("pyfn",  "2563EB"),  # function name / class name
    "tok.str":     ("pystr", "0F766E"),  # string / char literal
    "tok.num":     ("pynum", "B45309"),  # numeric literal
    "tok.comment": ("pycm",  "6B7280"),  # comment
    "tok.op":      ("pyop",  "9CA3AF"),  # operators / punctuation
    "tok.dec":     ("pydec", "111827"),  # decimal token
}


def _tok_class(ttype) -> str | None:
    """Purpose: map a Pygments token type onto one of our xcolor macros."""
    if ttype in Token.Comment:
        return "pycm"
    if ttype in Token.Keyword:
        return "pykw"
    if ttype in Token.Literal.String:
        return "pystr"
    if ttype in Token.Literal.Number:
        return "pynum"
    if ttype in Token.Name.Function or ttype in Token.Name.Class:
        return "pyfn"
    if ttype in Token.Name:
        return "pynm"
    if ttype in Token.Literal:
        return "pystr"
    if ttype in Token.Punctuation or ttype in Token.Operator:
        return "pyop"
    return None


_LATEX_ESC = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
    "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}



# Unicode harvested from the repo headers -> pdflatex-safe equivalents.
UNI = {
    "\u2248": r"$\approx$", "\u2264": r"$\leq$", "\u2265": r"$\geq$",
    "\u2260": r"$\neq$", "\u00d7": r"$\times$", "\u00f7": r"$\div$",
    "\u221e": r"$\infty$", "\u2211": r"$\sum$", "\u220f": r"$\prod$",
    "\u221a": r"$\sqrt{\ }$", "\u2208": r"$\in$", "\u2209": r"$\notin$",
    "\u2286": r"$\subseteq$", "\u2205": r"$\emptyset$", "\u00b1": r"$\pm$",
    "\u2192": r"$\to$", "\u2190": r"$\leftarrow$", "\u2191": r"$\uparrow$",
    "\u2193": r"$\downarrow$", "\u21d2": r"$\Rightarrow$", "\u00b0": r"$^\circ$",
    "\u00b5": r"$\mu$", "\u03a9": r"$\Omega$", "\u03b1": r"$\alpha$",
    "\u03b2": r"$\beta$", "\u03bb": r"$\lambda$", "\u2018": "`", "\u2019": "'",
    "\u201c": "``", "\u201d": "''", "\u2013": "--", "\u2014": "---",
    "\u2026": r"\ldots{}", "\u2022": r"$\bullet$", "\u00b7": "-",
    "\u2261": r"$\equiv$", "\u00ac": r"$\neg$", "\u2223": r"$|$",
    "\u2261x": "", "\u0301": "", "\ufeff": "",
    "\u2080": "0", "\u2081": "1", "\u2082": "2", "\u2083": "3",
    "\u00b2": "^2", "\u00b3": "^3", "\u207f": "^n", "\u00bc": r"$\frac14$",
}


def uni(text: str) -> str:
    """Purpose: fold the harvested Unicode down to pdflatex-safe ASCII.

    Inputs : text -- raw text from the solution headers.
    Outputs: text with every non-ASCII char mapped or dropped.
    """
    out = []
    for ch in text:
        if ord(ch) < 128:
            out.append(ch)
            continue
        repl = UNI.get(ch)
        if repl is None:
            repl = "" if not ch.isalnum() else {"\u2019": "'"}.get(ch, "")
        out.append(repl)
    return "".join(out)


def esc(text: str) -> str:
    """Purpose: escape a plain-text string for pdflatex. Inputs: str. Output: str."""
    out = []
    for ch in uni(text):
        out.append(_LATEX_ESC.get(ch, ch))
    return "".join(out)


def esc_math(text: str) -> str:
    """Purpose: escape text that may carry $...$ inline math. Inputs: str. Output: str."""
    parts = text.split("$")
    out = []
    for i, part in enumerate(parts):
        out.append(esc(part) if i % 2 == 0 else part)
    return "".join(out)


def _mono_piece(s: str) -> str:
    """Purpose: LaTeX-escape a fragment destined for \\texttt{} inside a color macro."""
    s = uni(s)
    s = s.replace("\\", r"\textbackslash{}")
    for ch, rep in (("{", r"\{"), ("}", r"\}"), ("_", r"\_"), ("&", r"\&"),
                    ("%", r"\%"), ("#", r"\#"), ("$", r"\$"), ("~", r"\textasciitilde{}"),
                    ("^", r"\textasciicircum{}")):
        s = s.replace(ch, rep)
    return s


def _tokens(code: str, language: str) -> list[list[tuple[str | None, str]]]:
    """Purpose: lex a kernel into per-line runs of (colour-class, raw text)."""
    lexer = PythonLexer() if language == "python" else CppLexer()
    lines: list[list[tuple[str | None, str]]] = [[]]
    for ttype, value in lex(code, lexer):
        if not value:
            continue
        cls = _tok_class(ttype)
        pieces = value.split("\n")
        lines[-1].append((cls, pieces[0]))
        for mid in pieces[1:-1]:
            lines.append([(None, mid)])
        if len(pieces) > 1:
            lines.append([(cls, pieces[-1])])
    return lines


def _merge(runs: list[tuple[str | None, str]]) -> list[tuple[str | None, str]]:
    """Purpose: coalesce adjacent runs sharing a colour class (smaller .tex)."""
    out: list[tuple[str | None, str]] = []
    for cls, txt in runs:
        if not txt:
            continue
        if out and out[-1][0] == cls:
            out[-1] = (cls, out[-1][1] + txt)
        else:
            out.append((cls, txt))
    return out


def highlight(code: str, language: str) -> list[str]:
    """Purpose: syntax-highlight a kernel into one LaTeX string per source line.

    Inputs : code -- raw kernel source (no imports, no boilerplate)
             language -- "python" | "cpp"
    Outputs: list of LaTeX fragments, one per source line, escaped and wrapped
             in the \\py<cls>{...} colour macros.
    """
    rows = []
    for runs in _tokens(code, language):
        rows.append("".join(
            ("\\" + cls + "{" + _mono_piece(txt) + "}") if cls else _mono_piece(txt)
            for cls, txt in _merge(runs)
        ))
    return rows


def code_block(code: str, language: str, numbered: bool = True) -> str:
    """Purpose: emit a standalone highlighted listing block. Inputs: str. Outputs: LaTeX str."""
    body = []
    for i, row in enumerate(highlight(code.strip("\n"), language), start=1):
        num = "\\clnnum{" + str(i) + "}" if numbered else ""
        body.append(num + row + "\\\\*")
    return "\\begin{codebox}\n" + "\n".join(body) + "\n\\end{codebox}"


def _col(label: str, rows: list[str], start: int) -> list[str]:
    """Purpose: one side-by-side column: header chip + numbered source lines."""
    out = ["\\begin{sbscol}{" + label + "}"]
    for i, row in enumerate(rows, start=start):
        out.append("\\clnnum{" + str(i) + "}" + row + "\\par")
    out.append("\\end{sbscol}")
    return out


def side_by_side(py_code: str, cpp_code: str, label_left: str = "Python (intuition kernel)",
                 label_right: str = "C++ (intuition kernel)") -> str:
    """Purpose: two-column comparative block -- Python left, C++ right.

    Inputs : py_code / cpp_code -- highlighted kernel sources (3-8 lines each).
    Outputs: LaTeX fragment built from two minipages inside one panel, so the two
             implementations read as a notebook diff view and never stack.
    """
    py_rows = highlight(py_code.strip("\n"), "python")
    cpp_rows = highlight(cpp_code.strip("\n"), "cpp")
    body = ["\\begin{sbsbox}"]
    body += _col(label_left, py_rows, 1)
    body += _col(label_right, cpp_rows, 1)
    body.append("\\end{sbsbox}")
    return "\n".join(body)


# --------------------------------------------------------------------------
# ASCII diagram box (drawn as a shaded, framed verbatim block)
# --------------------------------------------------------------------------
def diagram(text: str) -> str:
    """Purpose: render an ASCII state-trace / graph diagram. Inputs: str. Outputs: LaTeX str."""
    lines = uni(text).strip("\n").split("\n")
    width = max((len(html.unescape(l)) for l in lines), default=1)
    rows = []
    for i, line in enumerate(lines):
        body = _mono_piece(html.unescape(line))
        rows.append(f"\\diagline{{{body}}}")
        if i < len(lines) - 1:
            rows.append("\\diagspace")
    return "\\begin{diagbox}\n" + "\n".join(rows) + "\n\\end{diagbox}"


def _clean(text: str) -> str:
    """Purpose: normalise whitespace/newlines coming from a sub-agent JSON blob."""
    text = text.replace("\r", "")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


RE_TICK = re.compile(r"`([^`]+)`")
RE_BIGOH = re.compile(r"\bO\(([^()\n]{1,24})\)")


def _esc_math_aware(text: str) -> str:
    """Purpose: escape prose for LaTeX while leaving $...$ math spans untouched."""
    parts = re.split(r"(\$[^$]*\$)", text)
    return "".join(p if p.startswith("$") else esc(p) for p in parts)


def inline(text: str) -> str:
    """Purpose: render one line of prose -- `x` becomes \\texttt{x}, O(...) becomes math.

    Inputs : text -- raw prose (may contain backticks and $...$ math).
    Outputs: escaped single-line LaTeX.
    """
    out = []
    for i, chunk in enumerate(RE_TICK.split(uni(_clean(text)))):
        flat = chunk.replace("\n", " ")
        if i % 2:
            out.append("\\texttt{" + esc(flat) + "}")
            continue
        parts = re.split(r"(\$[^$]*\$)", flat)
        for j, part in enumerate(parts):
            if j % 2:
                out.append(part)
            else:
                out.append(RE_BIGOH.sub(lambda m: "$O(" + m.group(1) + ")$", esc(part)))
    return "".join(out)


def para(text: str) -> str:
    """Purpose: escaped multi-line paragraph block. Inputs: str. Outputs: LaTeX str."""
    chunks = [_clean(p) for p in _clean(text).split("\n\n")]
    return "\n".join(inline(c) for c in chunks if c)


def bullets(items, style: str = "tight") -> str:
    """Purpose: render a list of strings as a LaTeX itemize. Inputs: list[str]. Output: str."""
    out = ["\\begin{itemize}"]
    for it in items:
        out.append("  \\item " + inline(str(it)))
    out.append("\\end{itemize}")
    return "\n".join(out)


def badge(difficulty: str) -> str:
    """Purpose: colour-coded difficulty chip. Inputs: str. Outputs: LaTeX str."""
    cls = {"Easy": "bdEasy", "Medium": "bdMed", "Hard": "bdHard"}.get(difficulty, "bdEasy")
    return f"\\difficultychip{{{cls}}}{{{difficulty}}}"


def approach_block(idx: int, ap: dict) -> str:
    """Purpose: render one full approach: name, aha, side-by-side kernel, complexity."""
    name = esc(_clean(ap.get("name", f"Approach {idx}")))
    parts = [f"\\paragraph{{\\textcolor{{keycolor}}{{{name}}}}}", para(ap.get("aha", ""))]
    if ap.get("py") or ap.get("cpp"):
        parts.append(side_by_side(ap.get("py", ""), ap.get("cpp", "")))
    time_c = esc(_clean(ap.get("time", "?")))
    space_c = esc(_clean(ap.get("space", "?")))
    why = para(ap.get("why", ""))
    cell_time = "\\complexitycell{\\textbf{Time}\\ " + time_c + "}"
    cell_space = "\\complexitycell{\\textbf{Space}\\ " + space_c + "}"
    parts.append("\\complexityrow{" + cell_time + "}{" + cell_space + "}")
    if why:
        parts.append(f"\\justwhy{{{why}}}")
    return "\n".join(parts)


def question_block(q: dict, i: int) -> str:
    """Purpose: render one intuition-check question with its answer key."""
    qtext = inline(q.get("q", ""))
    ans = para(q.get("a", ""))
    return "\\qitem{\\textbf{Q" + str(i) + ".} " + qtext + "}\n\\anskey{" + ans + "}"


def problem_block(rec: dict, idx: int) -> str:
    """Purpose: render the complete 6-section entry for one problem. Output: LaTeX str."""
    num = esc(str(rec.get("number", "")).zfill(4))
    title = esc(_clean(rec.get("title", "")))
    title_tt = title.replace(" ", r"\ ")
    parts: list[str] = []

    parts.append(
        "\\phantomsection\n"
        + "\\addcontentsline{toc}{subsection}{" + num + " " + title + "}\n"
        + "\\newsubsection{" + num + r"\ \texttt{" + title_tt + "}"
        + badge(rec.get("difficulty", "?")) + "}"
    )

    # 1. Essence
    parts.append("\\probsection{Essence \\& Bounds}")
    parts.append(para(rec.get("core_objective", "")))
    if rec.get("bounds"):
        parts.append(para(rec["bounds"]))

    # 2. Multi-solution intuition
    parts.append("\\probsection{Multi-Solution Intuition (Python vs C++)}")
    for i, ap in enumerate(rec.get("approaches", [])[:3], start=1):
        parts.append(approach_block(i, ap))

    # 3. Visual trace
    if rec.get("diagram"):
        parts.append("\\probsection{Visual State Trace}")
        parts.append(diagram(rec["diagram"]))

    # 4. Language mechanics
    parts.append("\\probsection{Language Mechanics: Python vs C++}")
    if rec.get("cpp_vs_py"):
        parts.append(para(rec["cpp_vs_py"]))

    # 5. Alternative data structures
    parts.append("\\probsection{Alternative Data Structures \\& Optimisations}")
    if rec.get("cpp_alts"):
        parts.append(bullets(rec["cpp_alts"]))
    if rec.get("py_alts"):
        parts.append(bullets(rec["py_alts"]))

    # 6. Traps
    parts.append("\\probsection{Interview Traps \\& Sanity Checks}")
    trap = rec.get("trap")
    if isinstance(trap, list):
        trap = bullets(trap)
    if trap:
        parts.append(para(trap) if isinstance(trap, str) else trap)
    invariant = rec.get("invariant")
    if isinstance(invariant, list):
        invariant = " ".join(invariant)
    if invariant:
        parts.append("\\invariantcheck{" + para(invariant) + "}")

    # Intuition check
    qs = rec.get("questions", [])[:3]
    if qs:
        parts.append("\\probsection{Intuition Check --- 3 Questions}")
        parts.append("\\begin{qbox}")
        for i, q in enumerate(qs, start=1):
            parts.append(question_block(q, i))
        parts.append("\\end{qbox}")

    return "\n".join(parts)


def category_intro(rec: dict) -> str:
    """Purpose: render a problem row inside a category quick-reference table."""
    num = str(rec.get("number", "")).zfill(4)
    diff = {"Easy": "bdEasy", "Medium": "bdMed", "Hard": "bdHard"}.get(rec.get("difficulty", ""), "bdEasy")
    return ("\\qrow{" + num + "}{" + esc(_clean(rec.get("title", ""))) + "}"
            + "{" + rec.get("difficulty", "") + "}{" + diff + "}"
            + "{" + inline(rec.get("one_liner", "")) + "}")


def build_tex(records: list[dict], metadata: dict) -> str:
    """Purpose: assemble the complete .tex document. Inputs: records + metadata. Output: str."""
    from latexkit_preamble import PREAMBLE, BEGIN_DOC, END_DOC, render

    body: list[str] = []
    by_cat: dict[str, list[dict]] = {}
    for r in records:
        by_cat.setdefault(r["category"], []).append(r)

    for ci, (cat, probs) in enumerate(by_cat.items(), start=1):
        body.append("\\phantomsection")
        body.append("\\addcontentsline{toc}{section}{" + str(ci) + ". " + esc(cat) + "}")
        body.append("\\newchapter{\\textcolor{keycolor}{" + str(ci) + ".}\\ "
                    + esc(cat) + "}")
        note = next((p["category_note"] for p in probs if p.get("category_note")), "")
        if note:
            body.append(para(note))
        body.append("\\begin{qtable}")
        body.append("\\qrowhead{\\char`#}{Problem}{Level}{One-line intent}")
        for p in probs:
            body.append(category_intro(p))
        body.append("\\end{qtable}")
        for p in probs:
            body.append(problem_block(p, 0))

    total = sum(len(p) for p in by_cat.values())
    body.append("\\phantomsection")
    body.append("\\addcontentsline{toc}{section}{Appendix: Coverage Checklist}")
    body.append("\\newchapter{\\textcolor{keycolor}{Appendix}\\ Coverage Checklist}")
    body.append(para("Every problem in the local NeetCode repository, in canonical category order. "
                     "Tick a row only when you can answer all three intuition questions without looking."))
    body.append("\\begin{qtable}")
    body.append("\\qrowhead{\\char`#}{Category}{Count}{Coverage}")
    n = 0
    for cat, probs in by_cat.items():
        n += len(probs)
        body.append("\\qrow{" + str(n).zfill(3) + "}{" + esc(cat) + "}{" + str(len(probs))
                + "}{inksoft}{}")
    body.append("\\end{qtable}")

    head = render(PREAMBLE, title=metadata.get("title", "NeetCode 150"),
                  subtitle=metadata.get("subtitle", ""), author=metadata.get("author", ""),
                  date=metadata.get("date", ""))
    toc = "\\tableofcontents\n\\newpage"
    return head + render(BEGIN_DOC, title=metadata.get("title", ""),
                         subtitle=metadata.get("subtitle", ""), author=metadata.get("author", ""),
                         date=metadata.get("date", "")) + toc + "\n".join(body) + "\n" + END_DOC