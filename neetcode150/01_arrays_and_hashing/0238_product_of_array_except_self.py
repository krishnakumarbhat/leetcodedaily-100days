"""
=====================================================================
LeetCode 238 : Product of Array Except Self                    (Medium)
https://leetcode.com/problems/product-of-array-except-self/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Return answer[i] = product of ALL elements except nums[i].
    MUST run in O(n) WITHOUT using division.
---------------------------------------------------------------------
INTUITION
    answer[i] = (product LEFT of i) × (product RIGHT of i).
    Prefix pass fills the output left-to-right, then one suffix
    variable folds the right side in — O(1) extra memory.
---------------------------------------------------------------------
APPROACH 1 — Prefix × suffix in the output array (BEST)
    Time  Complexity : O(n)   Space Complexity : O(1) extra.
---------------------------------------------------------------------
APPROACH 2 — Divide-by-self (CONTRAST, rejected by the problem)
    answer[i] = total / nums[i]. O(n)/O(1) but: division is banned,
    and a zero input CRASHES the division (or corrupts every other
    answer when there are two+ zeros). Listed only to explain why
    the prefix/suffix trick exists.
---------------------------------------------------------------------
NUMPY NOTE : for pure computation numpy's np.prod / cumprod would
    vectorize this in C speed — but LeetCode forbids external libs.
    Conceptually, np.cumprod IS the prefix product used here.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List


# =====================================================================
# APPROACH 1 : Prefix × suffix without division — O(n) / O(1)
# =====================================================================
class Solution_PrefixSuffix:
    """
    Purpose : Compute product of all elements except each one.
    Inputs  : nums — the input array.
    Output  : list where answer[i] = product of nums except nums[i].
    """

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # The answer list doubles as working memory → O(1) extra.
        answer = [0] * len(nums)

        # ---- Pass 1 : prefix products ----
        # answer[i] = product of everything to the LEFT of i.
        answer[0] = 1  # nothing is left of index 0 → neutral product 1
        for i in range(1, len(nums)):
            # left-of-i = left-of-(i-1) × nums[i-1] — incremental product.
            answer[i] = answer[i - 1] * nums[i - 1]

        # ---- Pass 2 : fold in suffix products ----
        # suffix = product of everything to the RIGHT of the current i.
        suffix = 1  # nothing is right of the last index
        for i in range(len(nums) - 1, -1, -1):
            # prefix(left of i) × suffix(right of i) = answer for i.
            answer[i] *= suffix
            # move left one step: the suffix grows with nums[i].
            suffix *= nums[i]

        return answer


# =====================================================================
# APPROACH 2 : Divide-by-self — shown ONLY as a contrast
# =====================================================================
class Solution_DivideBySelf:
    """
    Purpose : Contrast implementation using division (invalid here).
    Inputs  : nums — the input array.
    Output  : list where answer[i] = product of nums except nums[i].
    NOTE    : NOT an accepted solution — division is banned by the
              problem and zeros break it mathematically.
    """

    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # total : product of every element.
        total = 1
        for num in nums:
            total *= num

        # Each slot = total / itself — division is the forbidden tool.
        return [total // num for num in nums]  # ZeroDivisionError on 0


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    # Official example (2*3*4=24, 1*3*4=12, 1*2*4=8, 1*2*3=6).
    nums = [1, 2, 3, 4]

    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_PrefixSuffix().productExceptSelf(nums)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Ground truth computed independently from the definition.
    expected = []
    for i in range(len(nums)):
        prod = 1
        for j in range(len(nums)):
            if i != j:
                prod *= nums[j]
        expected.append(prod)

    print(f"Approach 1 (prefix × suffix) : {r1}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print("PASS : prefix×suffix matches the definition." if r1 == expected else "FAIL : wrong answer.")