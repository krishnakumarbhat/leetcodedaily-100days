"""
=====================================================================
LeetCode 269 : Alien Dictionary                                  (Hard)
https://leetcode.com/problems/alien-dictionary/
Category   : Advanced graphs / topological sort
---------------------------------------------------------------------
PROBLEM
    Recover the alien alphabet order from words sorted in it. Return
    "" if the data is inconsistent (cycle / bad prefix).
---------------------------------------------------------------------
INTUITION
    Each adjacent pair contributes one constraint (first differing
    letter, a→b). Topologically sort the constraint DAG.
---------------------------------------------------------------------
APPROACH 1 · Kahn's algorithm (best)
    1. Build edges a→b + indegrees; queue zero-indegree letters.
    2. Pop → append; decrement children; leftovers = cycle → "".
APPROACH 2 · DFS with 3-color cycle detection
    White/gray/black states; gray revisit = cycle; append post-order
    and reverse.
---------------------------------------------------------------------
DEEP DIVE · The two failure modes
    (1) "abc" before "ab": a prefix that should be first — returns "".
    (2) A cycle in constraints can never exist in a real alphabet.
    Any valid topological order is accepted (there may be many);
    Kahn gives one deterministically, DFS gives another.
---------------------------------------------------------------------
TIME COMPLEXITY : O(C) — total characters over all words.
MEMORY COMPLEXITY: O(1) — ≤ 26 letters.
=====================================================================
"""


class Solution_1:
    def alienOrder(self, words):
        adj = {c: set() for w in words for c in w}
        indeg = {c: 0 for c in adj}
        for a, b in zip(words, words[1:]):
            for ca, cb in zip(a, b):
                if ca != cb:
                    if cb not in adj[ca]:
                        adj[ca].add(cb)
                        indeg[cb] += 1
                    break
            else:
                if len(a) > len(b):
                    return ""
        q = [c for c in adj if indeg[c] == 0]
        order = []
        while q:
            u = q.pop(0)
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return "".join(order) if len(order) == len(adj) else ""


class Solution_2:
    def alienOrder(self, words):
        adj = {c: set() for w in words for c in w}
        for a, b in zip(words, words[1:]):
            for ca, cb in zip(a, b):
                if ca != cb:
                    adj[ca].add(cb)
                    break
            else:
                if len(a) > len(b):
                    return ""
        WHITE, GRAY, BLACK = 0, 1, 2
        state = {c: WHITE for c in adj}
        order = []

        def dfs(u):
            state[u] = GRAY
            for v in adj[u]:
                if state[v] == GRAY:
                    return False
                if state[v] == WHITE and not dfs(v):
                    return False
            state[u] = BLACK
            order.append(u)
            return True

        if not all(dfs(c) for c in adj if state[c] == WHITE):
            return ""
        return "".join(reversed(order))


if __name__ == "__main__":
    import time, tracemalloc
    cases = [(["wrt", "wrf", "er", "ett", "rftt"], "wertf"),
             (["z", "x"], "zx"),
             (["z", "x", "z"], ""),
             (["ab", "abc"], "abc")]

    def is_ok(r, want):
        return r == want or (want != "" and len(r) == len(want) and sorted(r) == sorted(want))

    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for w, want in cases:
        r1, r2 = Solution_1().alienOrder(w), Solution_2().alienOrder(w)
        ok &= is_ok(r1, want) and is_ok(r2, want)
        print(f"[{w[0]}...] -> A1={r1} A2={r2} (want {want}) {'PASS' if is_ok(r1, want) and is_ok(r2, want) else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
