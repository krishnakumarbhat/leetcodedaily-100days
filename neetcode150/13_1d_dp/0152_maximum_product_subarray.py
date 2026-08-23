"""
=====================================================================
LeetCode 152 : Maximum Product Subarray                         (Medium)
https://leetcode.com/problems/maximum-product-subarray/
Category   : 1-D dynamic programming
---------------------------------------------------------------------
PROBLEM
    Largest product of a contiguous subarray. Negatives and zeros
    break the max-sum Kadane intuition.
---------------------------------------------------------------------
INTUITION
    A negative flips the sign of every running product: today's worst
    (most negative) product becomes tomorrow's best. Track both
    extremes.
---------------------------------------------------------------------
APPROACH 1 · Kadane with running min (best)
    maxEnd = max(a, maxEnd*a, minEnd*a); minEnd = min(same);
    best = max(best, maxEnd).
APPROACH 2 · Prefix/suffix sweep
    Scan products left→right and right→left, reset at zeros, take
    the max — the winning subarray is captured by one of the sweeps.
---------------------------------------------------------------------
DEEP DIVE · Why prefix-dropping fails
    [-2, 3, -4]: dropping the negative prefix gives max 3, but the
    full array scores 24. Keeping minEnd preserves the option
    "multiply the worst prefix by the next negative", which is the
    only case where dropping loses. Zeros auto-reset both extremes.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n)
MEMORY COMPLEXITY: O(1)
=====================================================================
"""


class Solution_1:
    def maxProduct(self, nums):
        best = max_end = min_end = nums[0]
        for a in nums[1:]:
            if a < 0:
                max_end, min_end = min_end, max_end
            max_end = max(a, max_end * a)
            min_end = min(a, min_end * a)
            best = max(best, max_end)
        return best


class Solution_2:
    def maxProduct(self, nums):
        best = nums[0]
        cur = 1
        for x in nums:
            cur *= x
            best = max(best, cur)
            if x == 0:
                cur = 1
        cur = 1
        for x in reversed(nums):
            cur *= x
            best = max(best, cur)
            if x == 0:
                cur = 1
        return best


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([2, 3, -2, 4], 6), ([-2, 0, -1], 0), ([-2, 3, -4], 24), ([0], 0)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for nums, want in cases:
        r1, r2 = Solution_1().maxProduct(nums), Solution_2().maxProduct(nums)
        ok &= r1 == r2 == want
        print(f"-> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
