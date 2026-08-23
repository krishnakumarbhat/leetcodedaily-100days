"""
=====================================================================
LeetCode 90 : Subsets II                                          (Medium)
https://leetcode.com/problems/subsets-ii/
Category   : Backtracking / duplicates
---------------------------------------------------------------------
PROBLEM
    All unique subsets of an array WITH duplicates.
---------------------------------------------------------------------
INTUITION
    Sort so equal values are adjacent; at each level use every
    distinct value only once (skip the second copy onward).
---------------------------------------------------------------------
APPROACH 1 · Backtracking with skip-duplicates (best)
    dfs(i) records cur, then for j in i..n: skip j if c[j]==c[j-1]
    (j>i), append c[j], recurse(j+1), pop.
APPROACH 2 · Set of sorted tuples
    Generate every subset via bitmask, sort tuples, dedupe with a set.
---------------------------------------------------------------------
DEEP DIVE · Why skipping the SECOND copy is enough
    Two duplicate values v produce identical subtrees only when used
    at the SAME level; the first v's subtree already contains every
    subset using v (any number of later copies). Skipping equal
    neighbors after a choice kills exactly the redundant subtrees —
    nothing is lost.
---------------------------------------------------------------------
TIME COMPLEXITY : O(2^n) worst case (all distinct).
MEMORY COMPLEXITY: O(n).
=====================================================================
"""


class Solution_1:
    def subsetsWithDup(self, nums):
        nums.sort()
        out, cur = [], []

        def dfs(i):
            out.append(cur[:])
            for j in range(i, len(nums)):
                if j > i and nums[j] == nums[j - 1]:
                    continue
                cur.append(nums[j])
                dfs(j + 1)
                cur.pop()

        dfs(0)
        return out


class Solution_2:
    def subsetsWithDup(self, nums):
        nums.sort()
        seen = set()
        for mask in range(1 << len(nums)):
            cur = tuple(nums[j] for j in range(len(nums)) if mask & (1 << j))
            seen.add(cur)
        return [list(t) for t in seen]


if __name__ == "__main__":
    import time, tracemalloc
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_1().subsetsWithDup([1, 2, 2])
    r2 = Solution_2().subsetsWithDup([1, 2, 2])
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    ok = len(r1) == len(r2) == 6
    print(f"A1={len(r1)} A2={len(r2)} (want 6) {'PASS' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
