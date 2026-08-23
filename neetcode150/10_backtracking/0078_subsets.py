"""
=====================================================================
LeetCode 78 : Subsets                                             (Medium)
https://leetcode.com/problems/subsets/
Category   : Backtracking
---------------------------------------------------------------------
PROBLEM
    Return the full power set of a distinct-integer array.
---------------------------------------------------------------------
INTUITION
    Each element is in or out — 2^n subsets. DFS branches on both
    choices; bitmask counting is the mechanical alternative.
---------------------------------------------------------------------
APPROACH 1 · Backtracking include/exclude (best)
    dfs(i): i == n → record. Else dfs(i+1) (exclude) and dfs(i+1)
    with nums[i] appended (include).
APPROACH 2 · Bitmask enumeration
    mask in 0..2^n-1: pick nums[j] iff bit j set.
---------------------------------------------------------------------
DEEP DIVE · What "backtracking" literally does here
    The append/pop pair is the backtrack: append explores the
    include-branch, pop restores the shared list so the exclude
    sibling starts from an identical prefix. Total leaves 2^n,
    each copied once → O(n·2^n).
---------------------------------------------------------------------
TIME COMPLEXITY : O(n · 2^n)
MEMORY COMPLEXITY: O(n) recursion depth.
=====================================================================
"""


class Solution_1:
    def subsets(self, nums):
        out, cur = [], []

        def dfs(i):
            if i == len(nums):
                out.append(cur[:])
                return
            dfs(i + 1)
            cur.append(nums[i])
            dfs(i + 1)
            cur.pop()

        dfs(0)
        return out


class Solution_2:
    def subsets(self, nums):
        out = []
        for mask in range(1 << len(nums)):
            out.append([nums[j] for j in range(len(nums)) if mask & (1 << j)])
        return out


if __name__ == "__main__":
    import time, tracemalloc
    nums = [1, 2, 3]
    tracemalloc.start()
    t0 = time.perf_counter()
    r1, r2 = Solution_1().subsets(nums), Solution_2().subsets(nums)
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    ok = len(r1) == len(r2) == 8
    print(f"A1={len(r1)} A2={len(r2)} (want 8) {'PASS' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
