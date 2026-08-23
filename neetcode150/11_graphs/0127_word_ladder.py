"""
=====================================================================
LeetCode 127 : Word Ladder                                       (Hard)
https://leetcode.com/problems/word-ladder/
Category   : Graphs
---------------------------------------------------------------------
PROBLEM
    A transformation sequence from `beginWord` to `endWord` is a list
    of words where every adjacent pair differs by exactly ONE letter,
    and every word after the first must exist in `wordList`. Return
    the SHORTEST such sequence length (counting beginWord), or 0 if
    no such sequence exists.
---------------------------------------------------------------------
INTUITION
    Words are NODES of a graph; an edge connects words differing in
    one letter. Shortest path in an unweighted graph = BFS. The graph
    is implicit: neighbours are generated on the fly by mutating each
    letter to a..z (26 × L candidates, each an O(1) set probe).
---------------------------------------------------------------------
APPROACH 1 — BFS (BEST for correctness)
    Queue of (word, depth); erase each word from the dict on first
    sight so nothing is visited twice. First dequeuing of endWord is
    provably the shortest path.
    Time  Complexity : O(n · L²)   Space Complexity : O(n · L)
---------------------------------------------------------------------
APPROACH 2 — Bidirectional BFS (BEST for speed)
    Grow two frontiers (begin side + end side); expand the smaller
    one; when a generated word lands in the opposite frontier the
    waves met. Visits ~2·b^(d/2) nodes instead of b^d.
    Time  Complexity : O(n · L²)   Space Complexity : O(n · L)
---------------------------------------------------------------------
DATA STRUCTURE DEEP DIVE — BFS vs DFS on implicit graphs
    BFS explores in layers: first hit of the target is the shortest
    path. DFS finds A path, not the shortest → wrong tool here.
    Python set/dict = open addressing + linear probing:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    Every generated candidate word is just a probe into the table.
    C++ unordered_set = separate chaining (bucket + linked list).
---------------------------------------------------------------------
REAL LIFE
    • Spell-checker "did you mean?" — shortest chain of one-edit
      corrections to a valid dictionary word.
    • Network routing: BFS on the hop graph finds fewest-hops paths;
      bidirectional BFS is how routers prune reverse-search trees.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import deque
from typing import List

# =====================================================================
# APPROACH 1 : BFS on the implicit word graph
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the shortest transformation sequence length.
    Inputs  : beginWord — starting word.
              endWord   — target word.
              wordList  — dictionary of allowed intermediate words.
    Output  : int ladder length (beginWord included), 0 if impossible.
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # dict : unvisited words, as a set for O(1) membership probes.
        word_set = set(wordList)
        # endWord must be in the dict — otherwise no path exists at all.
        if endWord not in word_set:
            return 0
        # beginWord may itself be listed — remove it so the BFS never
        # revisits the start node through a cycle.
        word_set.discard(beginWord)

        # queue : frontier of (word, depth). BFS visits in layer order,
        # so the first time endWord leaves the queue is the shortest.
        queue = deque([(beginWord, 1)])

        while queue:
            word, depth = queue.popleft()
            if word == endWord:
                return depth  # BFS first-hit guarantee: shortest length

            # Generate ALL one-letter neighbours: mutate every position
            # to every letter a..z, then probe the set (O(1) each).
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    neighbor = word[:i] + c + word[i + 1:]
                    if neighbor in word_set:
                        # Erase on first sight = visited marker; also
                        # prevents infinite loops on cycles.
                        word_set.remove(neighbor)
                        queue.append((neighbor, depth + 1))
        return 0  # frontier exhausted, endWord never reached

# =====================================================================
# APPROACH 2 : Bidirectional BFS — meet in the middle
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the shortest transformation sequence length.
    Inputs  : beginWord — starting word.
              endWord   — target word.
              wordList  — dictionary of allowed intermediate words.
    Output  : int ladder length (beginWord included), 0 if impossible.
    """

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0
        word_set.discard(beginWord)

        # Two waves: `front` grows from beginWord, `back` from endWord.
        # Each set holds only the CURRENT layer of its wave.
        front, back = {beginWord}, {endWord}
        depth = 1  # each loop round = one layer on both sides

        while front and back:
            # Always expand the SMALLER wave — keeps frontiers narrow
            # and drastically cuts the number of generated words.
            if len(front) > len(back):
                front, back = back, front

            next_layer = set()
            for word in front:
                for i in range(len(word)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        neighbor = word[:i] + c + word[i + 1:]
                        # Touched the OTHER wave → the two fronts met:
                        # path length = current depth + the joining step.
                        if neighbor in back:
                            return depth + 1
                        # Unvisited dict word → claim it for this side.
                        if neighbor in word_set:
                            word_set.remove(neighbor)
                            next_layer.add(neighbor)
            front = next_layer  # advance this wave by one layer
            depth += 1
        return 0  # a wave died out → no connecting path exists

# =====================================================================
# BENCHMARK — run both approaches on 3 official-style tests
# =====================================================================
if __name__ == "__main__":
    # Test 1 (official): hit→cog via hot→dot→dog→lot→log → length 5.
    tests = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], 5),
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log"], 0),   # endWord absent
        ("a", "c", ["a", "b", "c"], 2),                            # direct edge
    ]

    all_pass = True
    for idx, (b, e, wl, expected) in enumerate(tests, start=1):
        # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().ladderLength(b, e, wl)
        t1 = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: time + peak memory ---
        tracemalloc.start()
        t2 = time.perf_counter()
        r2 = SolutionTwo().ladderLength(b, e, wl)
        t3 = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok = r1 == expected and r2 == expected and r1 == r2
        all_pass = all_pass and ok
        print(
            f"Test {idx} ({b}->{e}) {'PASS' if ok else 'FAIL'} "
            f"| A1={r1} (expect {expected}) time={(t1-t0)*1e6:.2f} µs peak={peak1/1024:.1f} KB"
            f" | A2={r2} time={(t3-t2)*1e6:.2f} µs peak={peak2/1024:.1f} KB"
        )

    print("PASS : all tests green on both approaches."
          if all_pass else "FAIL : at least one test/approach disagrees.")