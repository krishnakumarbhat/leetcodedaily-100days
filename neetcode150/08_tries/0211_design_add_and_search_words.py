"""
=====================================================================
LeetCode 211 : Design Add and Search Words Data Structure       (Medium)
https://leetcode.com/problems/design-add-and-search-words-data-structure/
Category   : Tries
---------------------------------------------------------------------
PROBLEM
    Design a word dictionary with:
        addWord(word)  : store the word (lowercase letters only).
        search(word)   : true iff some stored word matches. The query
                         may contain the wildcard '.' matching ANY
                         single letter (e.g. "b.." matches "bad").
---------------------------------------------------------------------
INTUITION
    Words live in a trie (shared prefixes → O(L) walks). The twist is
    the '.' wildcard: at a '.' we do not know WHICH child to follow —
    we must branch into every child and let the rest of the pattern
    decide. Branching is "search" in the deep sense: either DFS
    (recurse, exhaust one branch fully before the next) or BFS
    (advance every candidate one level in lockstep).
---------------------------------------------------------------------
APPROACH 1 — Trie + recursive DFS (best)
    Walk the trie with an index i into the pattern.
        pattern[i] == '.' → try EVERY child; true if any matches.
        pattern[i] == 'c' → follow only child 'c'; missing ⇒ false.
        i == len(pattern) → answer = isEnd of the current node.
    The '.' branch is O(26) per level worst case; letters stay O(1).
    Time  Complexity : O(26^d) worst case, d = number of '.'; O(L)
                       without wildcards. addWord is O(L).
    Space Complexity : O(26·n·L) trie nodes worst case + O(L) call stack.
---------------------------------------------------------------------
APPROACH 2 — Trie + iterative BFS (level-by-level frontier)
    Keep a FRONTIER of candidate nodes. For each pattern char:
        '.' → frontier = ALL children of every candidate.
        'c' → frontier = only the 'c'-children of candidates.
    Empty frontier ⇒ no match. Finally, true iff some surviving node
    has isEnd. Same complexity as DFS, no recursion stack, and every
    candidate advances in lockstep — the natural "wavefront" view.
    Time  Complexity : O(26^d) worst case, O(L) without wildcards.
    Space Complexity : O(26^d) frontier worst case.
---------------------------------------------------------------------
DEEP DIVE — why a trie, and the wildcard cost
    Without '.' this is exactly LeetCode 208's trie: node = 26 child
    slots + isEnd. With '.', search becomes a tree WALK with branching:
    every '.' multiplies the live paths by up to 26, so d wildcards
    cost up to 26^d node visits. DFS visits one path to its end before
    backtracking; BFS visits all paths one level at a time — identical
    work, different order. Python dict children (open addressing,
    linear probing h(k,i) = (hash(k)+i) mod m) are lean for '.'-scanning:
    iterating only existing children beats scanning 26 fixed slots.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List, Tuple

class _TrieNode:
    """Shared trie node: dict of letter→child + end-of-word flag."""

    __slots__ = ("children", "isEnd")

    def __init__(self) -> None:
        # dict children: only EXISTING letters occupy memory (lean for '.')
        self.children: dict[str, _TrieNode] = {}
        self.isEnd: bool = False  # an inserted word terminates here

# =====================================================================
# APPROACH 1 : trie + recursive DFS wildcard search (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Word dictionary whose search supports '.' wildcards,
              implemented as trie + depth-first search.
    Inputs  : None at construction; words arrive via addWord/search.
    Output  : addWord stores; search answers wildcard matching.
    """

    def __init__(self) -> None:
        # Sentinel root; the empty prefix lives above the real letters.
        self.root: _TrieNode = _TrieNode()

    def addWord(self, word: str) -> None:
        """Purpose : Store `word` in the trie (standard insert walk).
        Inputs  : word — lowercase string.
        Output  : None."""
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())  # grow path
        node.isEnd = True  # mark word completion

    def search(self, word: str) -> bool:
        """Purpose : Match a pattern containing '.' wildcards (DFS).
        Inputs  : word — pattern; '.' matches any single letter.
        Output  : True iff some inserted word matches the pattern."""

        def dfs(node: _TrieNode, i: int) -> bool:
            # Pattern is spent → success only if this node ends a word.
            if i == len(word):
                return node.isEnd
            ch = word[i]
            if ch == ".":
                # Wildcard: ANY child may be the next step — try them all.
                return any(dfs(child, i + 1) for child in node.children.values())
            child = node.children.get(ch)
            # Fixed letter: exactly one path to follow.
            return child is not None and dfs(child, i + 1)

        return dfs(self.root, 0)

# =====================================================================
# APPROACH 2 : trie + iterative BFS wildcard search (frontier waves)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Word dictionary whose search supports '.' wildcards,
              implemented as trie + breadth-first frontier sweep.
    Inputs  : None at construction; words arrive via addWord/search.
    Output  : addWord stores; search answers wildcard matching.
    """

    def __init__(self) -> None:
        self.root: _TrieNode = _TrieNode()

    def addWord(self, word: str) -> None:
        """Purpose : Store `word` in the trie.
        Inputs  : word — lowercase string.
        Output  : None."""
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        node.isEnd = True

    def search(self, word: str) -> bool:
        """Purpose : Match a pattern with '.' wildcards using a frontier.
        Inputs  : word — pattern; '.' matches any single letter.
        Output  : True iff some inserted word matches."""
        frontier: deque[_TrieNode] = deque([self.root])  # nodes alive so far
        for ch in word:
            next_frontier: deque[_TrieNode] = deque()
            while frontier:
                node = frontier.popleft()
                if ch == ".":
                    # Wildcard: the frontier fans out into ALL children.
                    next_frontier.extend(node.children.values())
                elif ch in node.children:
                    # Fixed letter: keep only the matching child.
                    next_frontier.append(node.children[ch])
            frontier = next_frontier
            if not frontier:
                return False  # every branch died → no possible match
        # Any surviving path that ends a word is a match.
        return any(node.isEnd for node in frontier)


# =====================================================================
# BENCHMARK — run both approaches on 3 batches, time + peak memory
# =====================================================================
def _run_batch(solver, ops: List[str], expect: List[bool]) -> bool:
    """Purpose : Execute one batch against a solver and verify answers.
    Inputs  : solver — object with addWord/search.
              ops    — e.g. ["add bad", "search .ad"].
              expect — expected booleans for the search ops.
    Output  : True iff every answer matched."""
    j = 0
    for op in ops:
        if op.startswith("add "):
            solver.addWord(op[4:])  # adds never fail
            continue
        if solver.search(op[7:]) != expect[j]:
            return False
        j += 1
    return True


def _bench(label: str, tests: List[Tuple[str, List[str], List[bool]]]) -> bool:
    """Purpose : Time + memory-measure one solver class over all batches.
    Inputs  : label — human-readable solver name.
              tests — (name, ops, expected) triples.
    Output  : True iff all batches passed."""
    all_ok = True
    for name, ops, expect in tests:
        tracemalloc.start()
        t0 = time.perf_counter()
        ok = _run_batch(SolutionOne() if "Approach 1" in label else SolutionTwo(), ops, expect)
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        all_ok = all_ok and ok
        print(f"{label} | {name} : {'PASS' if ok else 'FAIL'}  "
              f"time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak} bytes")
    return all_ok


if __name__ == "__main__":
    # Three batches: the official example, wildcards in the middle/end,
    # and an empty-word edge case. "add " carries a trailing space and
    # stores the empty string.
    TESTS: List[Tuple[str, List[str], List[bool]]] = [
        ("problem example",
         ["add bad", "add dad", "add mad",
          "search pad", "search .ad", "search b.."],
         [False, True, True]),
        ("middle + tail wildcards",
         ["add hello", "add world", "add help",
          "search h.llo", "search h.llx", "search ...lo",
          "search he..o", "search w.r.x", "search .....", "search help."],
         [True, False, True, True, False, True, False]),
        ("empty word edge",
         ["add ", "search ", "search .", "search a"],
         [True, False, False]),
    ]

    ok1 = _bench("Approach 1 (trie + DFS)   ", TESTS)
    ok2 = _bench("Approach 2 (trie + BFS)   ", TESTS)

    print("PASS : both approaches return the expected answers on all batches."
          if ok1 and ok2 else "FAIL : at least one answer was wrong.")
