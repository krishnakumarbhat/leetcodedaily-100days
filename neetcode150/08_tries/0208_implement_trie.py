"""
=====================================================================
LeetCode 208 : Implement Trie (Prefix Tree)                     (Medium)
https://leetcode.com/problems/implement-trie-prefix-tree/
Category   : Tries
---------------------------------------------------------------------
PROBLEM
    Implement a trie (prefix tree) supporting three operations:
        insert(word)        : store the word.
        search(word)        : true iff `word` was inserted VERBATIM.
        startsWith(prefix)  : true iff SOME inserted word begins with
                              `prefix`. All words are lowercase letters.
---------------------------------------------------------------------
INTUITION
    A hash set answers "is this EXACT string stored?" in O(1), but
    "does ANY stored word START with this prefix?" has no hash to
    probe — it would scan every stored word (O(n·L)). A trie stores
    words along a SHARED spine: identical prefixes occupy the SAME
    nodes, so a prefix query is one root→leaf walk shared by every
    matching word. Each node holds one letter; the path root→node
    spells out a prefix.
---------------------------------------------------------------------
APPROACH 1 — 26-array trie (BEST for a fixed lowercase alphabet)
    Node = { children[26], isEnd }. children[i] is the child for
    letter 'a'+i; isEnd marks where an inserted word terminates.
    insert    : walk letters, allocate missing children, set isEnd.
    search    : walk letters; missing child ⇒ false; return isEnd.
    startsWith: walk letters; missing child ⇒ false; else true — NO
                isEnd check, any descendant counts.
    Time  Complexity : O(L) per op — L = word length.
    Space Complexity : O(26·n·L) worst case — n·L nodes, each holding
                       a 26-slot list; prefix sharing shrinks this.
---------------------------------------------------------------------
APPROACH 2 — Hash set + linear prefix scan (contrast)
    Store every word verbatim in a Python set (open addressing with
    LINEAR PROBING: h(k, i) = (hash(k) + i) mod m, i = 0, 1, 2, …).
    search    : O(1) average — one probe sequence.
    startsWith: scan ALL stored words and prefix-compare each — O(n·L),
                because a hash set cannot answer prefix queries.
    Time  Complexity : search O(1) avg; startsWith O(n·L).
    Space Complexity : O(n·L).
---------------------------------------------------------------------
DEEP DIVE — trie vs hash map
    The trie is a 26-way tree: every node has 26 child slots (one
    branch per letter position) + an isEnd flag. Words sharing a
    prefix share EVERY node of that prefix — "app" then "apple"
    costs only 2 extra nodes, not 5. Hash sets (dict/set probing
    h(k,i) = (hash(k)+i) mod m) give O(1) EXACT matches but cannot
    do prefix queries — a prefix is not a key. The trie converts
    them into a single O(L) walk at the price of memory: each node
    pre-allocates 26 slots (26×8 B ≈ 208 B) even when 1–2 children
    exist. Fixed small alphabet → list children (index = ord(c)-97);
    unbounded alphabets (Unicode) → dict children allocate only
    what is used.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

# =====================================================================
# APPROACH 1 : 26-array trie (best)
# =====================================================================
class SolutionOne:
    """
    Purpose : Implement a trie backed by 26-slot child arrays.
    Inputs  : None at construction; words arrive via insert/search/
              startsWith calls.
    Output  : insert stores words; search and startsWith answer
              membership / prefix questions.
    """

    class _Node:
        """Internal trie node: 26 child slots + end-of-word flag."""

        __slots__ = ("children", "isEnd")

        def __init__(self) -> None:
            # One slot per lowercase letter; None = no child for it.
            self.children: List[Optional["SolutionOne._Node"]] = [None] * 26
            self.isEnd: bool = False  # True = a word terminates here

    def __init__(self) -> None:
        # Sentinel root; the empty prefix lives above the real letters.
        self.root: SolutionOne._Node = SolutionOne._Node()

    def insert(self, word: str) -> None:
        """Purpose : Store `word` in the trie.
        Inputs  : word — lowercase string to insert.
        Output  : None (trie gains the word; duplicates idempotent)."""
        node = self.root
        for ch in word:
            idx = ord(ch) - 97  # 'a'→0 … 'z'→25 — one multiply to find child
            if node.children[idx] is None:
                node.children[idx] = SolutionOne._Node()  # grow the path
            node = node.children[idx]  # descend one level
        node.isEnd = True  # mark word completion at the final node

    def search(self, word: str) -> bool:
        """Purpose : Report whether `word` was inserted verbatim.
        Inputs  : word — lowercase string to look up.
        Output  : True iff a node exists for every letter AND the last
                  node is a word-end."""
        node = self.root
        for ch in word:
            node = node.children[ord(ch) - 97]
            if node is None:
                return False  # path dies here → word absent
        return node.isEnd  # must END exactly at this node

    def startsWith(self, prefix: str) -> bool:
        """Purpose : Report whether any inserted word begins with prefix.
        Inputs  : prefix — lowercase string to match as a prefix.
        Output  : True iff a node exists for every letter of prefix
                  (any word finishing below it makes the prefix valid)."""
        node = self.root
        for ch in prefix:
            node = node.children[ord(ch) - 97]
            if node is None:
                return False
        return True  # a path exists → some word continues from here

# =====================================================================
# APPROACH 2 : hash set + linear prefix scan (no trie at all)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Implement the same API using a plain hash set.
    Inputs  : None at construction; words arrive via method calls.
    Output  : search does O(1)-average membership; startsWith is a
              slow O(n·L) linear scan of every stored word.
    """

    def __init__(self) -> None:
        # Python set = open addressing, linear probing
        # h(k, i) = (hash(k) + i) mod m — exact-match store only.
        self.words: set[str] = set()

    def insert(self, word: str) -> None:
        """Purpose : Store `word` verbatim in the set.
        Inputs  : word — lowercase string.
        Output  : None."""
        self.words.add(word)

    def search(self, word: str) -> bool:
        """Purpose : Exact membership test.
        Inputs  : word — lowercase string.
        Output  : True iff word is present — O(1) average probe."""
        return word in self.words

    def startsWith(self, prefix: str) -> bool:
        """Purpose : Prefix test without a prefix data structure.
        Inputs  : prefix — lowercase string.
        Output  : True iff some stored word starts with it — scans ALL
                  words (O(n·L)) because sets cannot answer range or
                  prefix queries."""
        return any(w.startswith(prefix) for w in self.words)


# =====================================================================
# BENCHMARK — run both approaches on 3 batches, time + peak memory
# =====================================================================
def _run_batch(solver, ops: List[str], expect: List[bool]) -> bool:
    """Purpose : Execute one batch of ops against a solver and verify
                  every search/prefix answer.
    Inputs  : solver — object with insert/search/startsWith.
              ops    — e.g. ["insert apple", "search app", "prefix app"].
              expect — expected booleans for the non-insert ops.
    Output  : True iff every answer matched."""
    j = 0
    for op in ops:
        if op.startswith("insert "):
            solver.insert(op[7:])  # inserts never fail
            continue
        got = solver.search(op[7:]) if op.startswith("search ") else solver.startsWith(op[7:])
        if got != expect[j]:
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
    # Three batches: shared-prefix depth, exact-vs-prefix semantics,
    # and a long-prefix miss — every search/prefix op carries the
    # expected boolean.
    TESTS: List[Tuple[str, List[str], List[bool]]] = [
        ("problem example",
         ["insert apple", "search apple", "search app", "prefix app",
          "insert app", "search app"],
         [True, False, True, True]),
        ("shared prefixes",
         ["insert a", "insert ab", "insert abc", "insert abd",
          "search ab", "prefix ab", "search abd", "search abe", "prefix abc"],
         [True, True, True, False, True]),
        ("long prefix miss",
         ["insert zookeeper", "insert zoo", "insert zoom",
          "search zoo", "prefix zo", "prefix zooo", "search zook", "search zoom"],
         [True, True, False, False, True]),
    ]

    ok1 = _bench("Approach 1 (26-array trie) ", TESTS)
    ok2 = _bench("Approach 2 (hash set + scan)", TESTS)

    print("PASS : both approaches return the expected answers on all batches."
          if ok1 and ok2 else "FAIL : at least one answer was wrong.")
