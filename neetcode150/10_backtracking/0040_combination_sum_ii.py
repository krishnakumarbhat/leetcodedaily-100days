"""
=====================================================================
LeetCode 40 : Combination Sum II                                 (Medium)
https://leetcode.com/problems/combination-sum-ii/
Category   : Backtracking / duplicates
---------------------------------------------------------------------
PROBLEM
    All unique combos summing to target; each candidate used AT MOST
    ONCE and input may contain duplicates.
---------------------------------------------------------------------
INTUITION
    Sort + two rules: move j+1 (each element once) and skip equal
    neighbors (unique combos). Sorted input lets us break when the
    candidate already exceeds the remaining target.
---------------------------------------------------------------------
APPROACH 1 · Sorted DFS (best)
    for j in i..n: if j > i and c[j]==c[j-1]: continue; if c[j] > rem:
    break; take, recurse(j+1), pop.
APPROACH 2 · Frequency-map branching
    Group values with counts; branch per distinct value 0..cnt copies.
---------------------------------------------------------------------
DEEP DIVE · break vs continue after sorting
    In Combination Sum I (unlimited use, unsorted) we `continue`
    because a big candidate doesn't rule out smaller ones later. Here
    sorting guarantees c[j] > rem ⇒ every later candidate is also too
    big, so `break` prunes harder with identical semantics.
---------------------------------------------------------------------
TIME COMPLEXITY : O(2^n) worst case.
MEMORY COMPLEXITY: O(n).
=====================================================================
"""


class Solution_1:
    def combinationSum2(self, candidates, target):
        candidates.sort()
        out, cur = [], []

        def dfs(i, rem):
            if rem == 0:
                out.append(cur[:])
                return
            for j in range(i, len(candidates)):
                if candidates[j] > rem:
                    break
                if j > i and candidates[j] == candidates[j - 1]:
                    continue
                cur.append(candidates[j])
                dfs(j + 1, rem - candidates[j])
                cur.pop()

        dfs(0, target)
        return out


class Solution_2:
    def combinationSum2(self, candidates, target):
        from collections import Counter
        freq = list(Counter(candidates).items())
        out, cur = [], []

        def dfs(idx, rem):
            if rem == 0:
                out.append(cur[:])
                return
            if idx == len(freq):
                return
            v, cnt = freq[idx]
            dfs(idx + 1, rem)
            for copies in range(1, cnt + 1):
                if rem < v * copies:
                    break
                cur.extend([v] * copies)
                dfs(idx + 1, rem - v * copies)
                del cur[-copies:]

        dfs(0, target)
        return out


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([10, 1, 2, 7, 6, 1, 5], 8, 4), ([2, 5, 2, 1, 2], 5, 2), ([1, 1, 1, 1], 2, 1)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for c, t, want in cases:
        r1, r2 = len(Solution_1().combinationSum2(c, t)), len(Solution_2().combinationSum2(c, t))
        ok &= r1 == r2 == want
        print(f"target={t} -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
