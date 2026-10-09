# Content contract for one NeetCode 150 category

You are writing the analytical payload for one category of a study-guide PDF.

## Inputs
Read **both** solutions for every problem you are assigned:
- `neetcode150/<key>.py`
- `neetcode150/<key>.cpp`

`<key>` is given below as `<dir>/<stem>` (no extension). Every header block in
those files already states the difficulty, the intuition, and the named approaches.
**Reuse their vocabulary; do not invent different approach names.**

## Output
Write ONE JSON file to `pdf/content/<OUTFILE>`:

```json
{"problems": [ <record>, <record>, ... ]}
```

### Record schema (exact keys, no extras, no omissions)

```json
{
  "key": "01_arrays_and_hashing/0001_two_sum",
  "one_liner": "<= 12 words, the problem's intent in one clause>",
  "category_note": "2-4 sentences on the mental model of this whole category. Put this ONLY on the FIRST problem record of the category; omit it elsewhere.",
  "core_objective": "Exactly 2 sentences distilling what must be computed.",
  "bounds": "Concrete value/length ranges plus the boundary traps: empty input, n=1, negatives, duplicates, cycles, overflow, off-by-one.",
  "approaches": [
    {
      "name":  "approach name, taken from the solution header (e.g. 'One-pass hash map')",
      "aha":   "1-2 sentences: the conceptual breakthrough in plain English.",
      "py":    "3-8 lines of Python -- the algorithmic kernel only",
      "cpp":   "3-8 lines of C++  -- the algorithmic kernel only",
      "time":  "O(n) or O(n log n) ...",
      "space": "O(n) or O(1) ...",
      "why":   "one short line justifying both bounds"
    }
  ],
  "diagram": "ASCII art, <= 18 lines, <= 64 chars per line",
  "cpp_vs_py": "1 paragraph, 3-5 sentences, hardware-level: cache locality, boxing, static vs dynamic dispatch, branch prediction, allocation.",
  "cpp_alts": ["2-4 bullets on std::map vs unordered_map vs gp_hash_table, custom hashers, string_view, deque, ... -- only what genuinely applies"],
  "py_alts": ["2-4 bullets on defaultdict, Counter, deque, heapq, bisect, itertools, dict.setdefault, ... -- only what genuinely applies"],
  "trap": "1-2 sentences on the #1 mistake candidates make here.",
  "invariant": "1 sentence: the loop/recursion invariant to check before submitting.",
  "questions": [
    {"q": "intuition question 1", "a": "answer, 1-3 sentences"},
    {"q": "intuition question 2", "a": "answer"},
    {"q": "intuition question 3", "a": "answer"}
  ]
}
```

## HARD RULES

**Kernels (`py` / `cpp`)**
1. 3-8 lines each. Match the two languages *row for row in intent*, not line count.
2. NO imports, NO `#include`, NO `class`/`def`/`Solution(...)`/`: public:` wrapper,
   NO `return []`, NO benchmark/`__main__`. Show the loop/state transition only.
3. Indent the kernel exactly as it sits inside the real function so the nesting reads.
4. Prefer real code lifted from the solution file, lightly trimmed. Keep every line
   at or under ~52 characters so both columns fit a two-column A4 page without wrapping.
5. Give between 2 and 3 approaches. Order them brute-force-ish -> better -> optimal.
6. `py` must be valid Python 3 and `cpp` valid C++17 **as a bare block of statements**.
7. Escape sequences are literal: write `\n` as a real backslash-n in the JSON string.

**Diagram**
- Pure ASCII. No box-drawing characters beyond `- | + > < v ^ * = . : '` and spaces.
- Show the algorithm in motion: pointer positions, window frames, recursion branches,
  DP table cells, interval merges, edge relaxations, bit layouts.
- Align columns with spaces. Max 64 columns, max 18 lines.
- NO LaTeX, NO tabs.

**Prose**
- Inline math: wrap as `$O(n^2)$`, `$2^{31}-1$`, `$\log n$`.
- Identifiers: wrap in backticks, e.g. `seen`, `nums[i]`.
- NEVER emit raw LaTeX control sequences (`\`, `{` `}` are fine only inside `py`/`cpp`/JSON).
- Be concrete and physical. No filler like "this is a common problem".
- Exactly 3 questions per problem, and they must probe *why the trick works*,
  not "what does line 4 do". Answers are shown in the PDF answer key.

## Verification before you finish
- `python3 -c "import json;d=json.load(open('pdf/content/<OUTFILE>'));print(len(d['problems']))"`
  -> must equal the number of problems assigned.
- Every record's `key` must exactly match the assigned key string.
