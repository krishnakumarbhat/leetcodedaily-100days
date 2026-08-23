"""
=====================================================================
LeetCode 46 : Permutations                                        (Medium)
https://leetcode.com/problems/permutations/
Category   : Backtracking
---------------------------------------------------------------------
PROBLEM
    All n! permutations of a distinct-integer array.
---------------------------------------------------------------------
INTUITION
    Fix slot by slot; at each level pick an unused element. The
    swap-trick encodes "used" by position in the array itself.
---------------------------------------------------------------------
APPROACH 1 · Swap-based DFS (best)
    dfs(pos): pos == n → record. For j in pos..n-1: swap(pos,j),
    recurse, swap back.
APPROACH 2 · used[] bitmap + running permutation
    Mark used[i], append nums[i], recurse, pop + unmark.
---------------------------------------------------------------------
DEEP DIVE · Two state encodings, one search tree
    Swap version: after fixing position pos the elements left of pos
    are exactly the used ones — state lives in the array (zero extra
    memory, no copies). used[] version copies the permutation at each
    leaf but is easier to read. Both enumerate n! leaves.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n · n!)
MEMORY COMPLEXITY: O(n).
=====================================================================
"""


class Solution_1:
    def permute(self, nums):
        out = []
        n = len(nums)

        def dfs(pos):
            if pos == n:
                out.append(nums[:])
                return
            for j in range(pos, n):
                nums[pos], nums[j] = nums[j], nums[pos]
                dfs(pos + 1)
                nums[pos], nums[j] = nums[j], nums[pos]

        dfs(0)
        return out


class Solution_2:
    def permute(self, nums):
        out, cur = [], []
        used = [False] * len(nums)

        def dfs():
            if len(cur) == len(nums):
                out.append(cur[:])
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                cur.append(nums[i])
                dfs()
                cur.pop()
                used[i] = False

        dfs()
        return out


if __name__ == "__main__":
    import time, tracemalloc
    tracemalloc.start()
    t0 = time.perf_counter()
    r1, r2 = Solution_1().permute([1, 2, 3]), Solution_2().permute([1, 2, 3])
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    ok = len(r1) == len(r2) == 6
    print(f"A1={len(r1)} A2={len(r2)} (want 6) {'PASS' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
