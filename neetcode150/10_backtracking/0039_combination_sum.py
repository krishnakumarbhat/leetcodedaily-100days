"""
=====================================================================
LeetCode 39 : Combination Sum                                    (Medium)
https://leetcode.com/problems/combination-sum/
Category   : Backtracking
---------------------------------------------------------------------
PROBLEM
    All unique combinations of distinct candidates summing to target,
    each candidate usable UNLIMITED times.
---------------------------------------------------------------------
INTUITION
    Coin-change style DFS: at each level either take the current
    candidate again (same index) or advance — target decreases so
    recursion terminates.
---------------------------------------------------------------------
APPROACH 1 · Backtracking with repeat (best)
    dfs(i, rem): rem == 0 → record. For j in i..n: skip c[j] > rem
    (prune), take, recurse(j) — same j = unlimited use — then pop.
APPROACH 2 · DP table of combinations
    dp[t] lists combos for sum t; extend dp[t-c] with c for t = c..T.
---------------------------------------------------------------------
DEEP DIVE · The one-character difference from Subsets II
    recurse(j+1) forbids reuse; recurse(j) allows it. The j from the
    LOOP start also forbids order permutations (no (2,3) after (3,2))
    because j only moves forward. Pruning c[j] > rem cuts most of the
    tree when the target is small relative to candidates.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n^(target/min)) worst case.
MEMORY COMPLEXITY: O(target/min).
=====================================================================
"""


class Solution_1:
    def combinationSum(self, candidates, target):
        out, cur = [], []

        def dfs(i, rem):
            if rem == 0:
                out.append(cur[:])
                return
            for j in range(i, len(candidates)):
                if candidates[j] > rem:
                    continue
                cur.append(candidates[j])
                dfs(j, rem - candidates[j])
                cur.pop()

        dfs(0, target)
        return out


class Solution_2:
    def combinationSum(self, candidates, target):
        dp = [[] for _ in range(target + 1)]
        dp[0] = [[]]
        for c in candidates:
            for t in range(c, target + 1):
                for combo in dp[t - c]:
                    dp[t].append(combo + [c])
        return dp[target]


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([2, 3, 6, 7], 7, 2), ([2, 3, 5], 8, 3), ([2], 1, 0)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for c, t, want in cases:
        r1, r2 = len(Solution_1().combinationSum(c, t)), len(Solution_2().combinationSum(c, t))
        ok &= r1 == r2 == want
        print(f"target={t} -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
