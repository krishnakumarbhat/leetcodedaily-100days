"""
=====================================================================
LeetCode 212 : Word Search II                                       (Hard)
https://leetcode.com/problems/word-search-ii/
Category   : Tries
---------------------------------------------------------------------
PROBLEM
    Given an m×n board of letters and a list of words, return EVERY
    word that can be spelled by moving between ADJACENT cells (up /
    down / left / right, diagonals excluded). A cell may be used at
    most once per word.
---------------------------------------------------------------------
INTUITION
    N words on one board → run ONE shared search instead of N
    independent ones. Insert all words into a trie, then walk the
    board with grid-DFS; at every cell, check whether the letter
    continues the current trie path. A path that reaches a word-end
    is a hit. Because many words share prefixes, a single DFS tree
    serves all of them — this is the "why trie" moment.
---------------------------------------------------------------------
APPROACH 1 — Trie + grid DFS backtracking (foundation)
    Build the trie (each terminal node stores its full word, which
    doubles as a "found" marker). For every cell, DFS: prune when the
    letter has no trie child; mark cells '#' while visiting to stop
    re-use, restore on backtrack. When a node's stored word is found,
    record it and CLEAR the stored word so it is never reported again.
    Time  Complexity : O(m·n·4^L) worst case — L = max word length,
                       but the trie prunes dead prefixes early.
    Space Complexity : O(26·n·L) trie + O(L) recursion depth.
---------------------------------------------------------------------
APPROACH 2 — Trie + grid DFS with branch pruning (BEST)
    Same walk, plus a refs counter on every node = number of words
    still reachable through it. When a node's last remaining word is
    found, refs drops to 0 and the whole dead branch is DELETED from
    the trie — future DFS never re-explores it. This removes the
    classic "found word still costs DFS time on every later cell"
    waste.
    Time  Complexity : O(m·n·4^L) worst case, faster in practice.
    Space Complexity : O(26·n·L) trie + O(L) recursion depth.
---------------------------------------------------------------------
DEEP DIVE — pruning + shared prefixes
    A plain hash set of words cannot guide the walk: from cell (r,c)
    you would have to ask "which words start with the letters spelled
    so far?" — a PREFIX query, exactly what hash maps cannot answer
    (probing h(k,i) = (hash(k)+i) mod m finds only exact keys). The
    trie answers it in O(1) per letter: one child lookup decides
    whether to descend or prune. Deleting used words (A2) turns the
    trie into a live accumulator — each word is discovered exactly
    once and its branch dies afterwards, so later cells stop paying
    for it. Memory math: n words of avg length L share prefix nodes;
    worst case n·L nodes × 26 pointers each.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
import copy
from typing import List, Tuple

class _TrieNode:
    """Shared trie node: letter→child dict, stored word, refs counter."""

    __slots__ = ("children", "word", "refs")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.word: str | None = None  # non-None ⇒ word ends here, unfound
        self.refs: int = 0            # words still reachable through this node

def _insert(root: _TrieNode, w: str) -> None:
    """Purpose : Insert `w` into the trie, bumping refs on every node.
    Inputs  : root — trie root; w — lowercase word.
    Output  : None (trie gains the word)."""
    node = root
    node.refs += 1
    for ch in w:
        if ch not in node.children:
            node.children[ch] = _TrieNode()
        node = node.children[ch]
        node.refs += 1
    node.word = w  # terminal node remembers its own word

# =====================================================================
# APPROACH 1 : trie + grid DFS backtracking (foundation)
# =====================================================================
class SolutionOne:
    """
    Purpose : Find all board-spellable words via a trie + backtracking
              DFS; no branch pruning.
    Inputs  : findWords(board, words).
    Output  : List[str] of every found word (discovery order).
    """

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Purpose : Return every word in `words` spellable on `board`.
        Inputs  : board — m×n grid of letters; words — search list.
        Output  : List[str] of found words."""
        root = _TrieNode()
        for w in words:
            _insert(root, w)
        rows, cols = len(board), len(board[0])
        found: List[str] = []

        def dfs(r: int, c: int, node: _TrieNode) -> None:
            # Prune: off the grid, cell in use, or no trie child.
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if board[r][c] == "#":
                return
            ch = board[r][c]
            child = node.children.get(ch)
            if child is None:
                return  # no word continues this way — prune the branch
            if child.word is not None:
                found.append(child.word)  # path spells a full word
                child.word = None         # never report it again
            board[r][c] = "#"             # claim the cell (no re-use)
            dfs(r + 1, c, child)          # four adjacent neighbours
            dfs(r - 1, c, child)
            dfs(r, c + 1, child)
            dfs(r, c - 1, child)
            board[r][c] = ch              # backtrack: release the cell

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)           # start a walk at every cell
        return found

# =====================================================================
# APPROACH 2 : trie + grid DFS with branch pruning (best)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Find all board-spellable words via a trie + backtracking
              DFS that DELETES exhausted branches (refs counter).
    Inputs  : findWords(board, words).
    Output  : List[str] of every found word (discovery order).
    """

    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """Purpose : Return every word in `words` spellable on `board`.
        Inputs  : board — m×n grid of letters; words — search list.
        Output  : List[str] of found words."""
        root = _TrieNode()
        for w in words:
            _insert(root, w)
        rows, cols = len(board), len(board[0])
        found: List[str] = []

        def dfs(r: int, c: int, node: _TrieNode) -> None:
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return
            if board[r][c] == "#":
                return
            ch = board[r][c]
            child = node.children.get(ch)
            if child is None or child.refs <= 0:
                return  # branch already exhausted — skip it entirely
            if child.word is not None:
                found.append(child.word)
                child.word = None
                child.refs -= 1  # one fewer word left in this branch
            board[r][c] = "#"
            dfs(r + 1, c, child)
            dfs(r - 1, c, child)
            dfs(r, c + 1, child)
            dfs(r, c - 1, child)
            board[r][c] = ch
            if child.refs <= 0:
                del node.children[ch]  # prune: no words left below → delete

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)
        return found


# =====================================================================
# BENCHMARK — run both approaches on 3 boards, time + peak memory
# =====================================================================
def _bench(label: str, boards: List[List[List[str]]],
           word_lists: List[List[str]],
           expected: List[List[str]]) -> bool:
    """Purpose : Time + memory-measure one solver class over all boards.
    Inputs  : label — solver name; boards/word_lists/expected — triples
              of test inputs and ground truth.
    Output  : True iff every board matched the expected word set."""
    all_ok = True
    for t, (board, words) in enumerate(zip(boards, word_lists), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        got = (SolutionOne if "Approach 1" in label else SolutionTwo)(
        ).findWords(copy.deepcopy(board), list(words))  # fresh board: '#'
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        ok = sorted(got) == sorted(expected[t - 1])  # order-free compare
        all_ok = all_ok and ok
        print(f"{label} | test {t} : {'PASS' if ok else 'FAIL'}  "
              f"found {len(got)} word(s)  time = {(t1 - t0) * 1e6:.2f} µs  "
              f"peak-mem = {peak} bytes")
    return all_ok


if __name__ == "__main__":
    # Board 1: the official example → oath, eat. Board 2: only ADJACENT
    # cells count — ab (right), ac (down), bd (down) are findable;
    # cb/ad are diagonal and cannot be built. Board 3: single cell.
    BOARDS: List[List[List[str]]] = [
        [["o", "a", "a", "n"], ["e", "t", "a", "e"],
         ["i", "h", "k", "r"], ["i", "f", "l", "v"]],
        [["a", "b"], ["c", "d"]],
        [["a"]],
    ]
    WORD_LISTS: List[List[str]] = [
        ["oath", "pea", "eat", "rain"],
        ["ab", "cb", "ad", "abcd", "ac", "bd"],
        ["a", "b", "aa", "abc"],
    ]
    EXPECTED: List[List[str]] = [
        ["oath", "eat"],
        ["ab", "ac", "bd"],
        ["a"],
    ]

    ok1 = _bench("Approach 1 (DFS basic)     ", BOARDS, WORD_LISTS, EXPECTED)
    ok2 = _bench("Approach 2 (DFS + pruning) ", BOARDS, WORD_LISTS, EXPECTED)

    print("PASS : both approaches find exactly the expected words on every board."
          if ok1 and ok2 else "FAIL : at least one answer was wrong.")
