"""
=====================================================================
LeetCode 15 : 3Sum                                              (Medium)
https://leetcode.com/problems/3sum/
Category   : Two Pointers
---------------------------------------------------------------------
PROBLEM
    Given an integer array nums, return ALL unique triplets [a,b,c]
    with a + b + c = 0. "Unique" means no duplicate triplet: (1,-1,0)
    and (-1,0,1) are the same answer. n can reach 3000 → O(n³) is
    way too slow.
---------------------------------------------------------------------
INTUITION
    Fix one element a = nums[i]. The problem collapses to the 2-sum
    question "find b + c = -a" on the remaining slice — and 2-sum on
    a SORTED array is solved in O(n) with two pointers. Sorting also
    manufactures uniqueness for free: equal values become adjacent,
    so skipping consecutive duplicates kills mirrored triplets.
---------------------------------------------------------------------
APPROACH 1 — Sort + two pointers (BEST, O(n²))
    Sort nums. For each pivot i (skipping duplicate pivots):
      • target = -nums[i]; l = i+1, r = n-1.
      • Sum nums[l] + nums[r]: < target → l += 1, > target → r -= 1,
        == target → record, then skip duplicates on BOTH sides.
      • nums[i] > 0 → early exit: three positives can never sum to 0.
    Time  Complexity : O(n²)   Space Complexity : O(1) extra
---------------------------------------------------------------------
APPROACH 2 — Hash map with dedupe set (O(n²) time, O(n) space)
    Same pivot loop, but the inner 2-sum uses a set of seen values:
    for each j, look up -(nums[i]+nums[j]). Insert triplets into a
    set of canonical "a,b,c" tuples to kill duplicates.
    Time  Complexity : O(n²)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — how sorting kills duplicate triplets
    With sorted input, any triplet can be emitted in sorted order
    (a ≤ b ≤ c). Two different (i,j,k) index triples produce the same
    sorted VALUE triple only when the same values repeat — and the
    skip-duplicates rule jumps PAST those repeats, so the exact same
    value triple can never be recorded twice. Python's set-of-tuples
    achieves the same by hashing the sorted tuple; the hash table
    underneath (dict/set = open addressing, linear probing) is exactly:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    while C++ unordered_set chains colliding keys per bucket.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Tuple

# =====================================================================
# APPROACH 1 : Sort + two pointers
# =====================================================================
class SolutionOne:
    """
    Purpose : Return all unique value-triplets summing to zero.
    Inputs  : nums — array of integers to search inside.
    Output  : List[List[int]] — sorted triplets, no duplicates.
    """

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        n = len(nums)
        if n < 3:
            return result

        # Sorting is the ONE preprocessing step that buys both the
        # two-pointer walk AND the duplicate elimination.
        nums.sort()

        for i in range(n - 2):
            # The array is sorted: if the smallest remaining element is
            # already positive, no later triplet can ever sum to zero.
            if nums[i] > 0:
                break
            # Skip duplicate pivots — the same 'a' gives the same triplets.
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Classic sorted 2-sum on the slice right of i, target = -a.
            target = -nums[i]
            l, r = i + 1, n - 1
            while l < r:
                current_sum = nums[l] + nums[r]
                if current_sum < target:
                    l += 1               # pair too small → need a bigger b
                elif current_sum > target:
                    r -= 1               # pair too big → need a smaller c
                else:
                    # b + c == -a → record the triplet in sorted order.
                    result.append([nums[i], nums[l], nums[r]])
                    # Skip duplicate b AND duplicate c — the pair of
                    # indices may change, but the VALUE triple would be
                    # identical, so it must not be recorded again.
                    while l < r and nums[l] == nums[l + 1]:
                        l += 1
                    while l < r and nums[r] == nums[r - 1]:
                        r -= 1
                    l += 1
                    r -= 1
        return result


# =====================================================================
# APPROACH 2 : Pivot + hash-set 2-sum with a dedupe set
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return all unique value-triplets summing to zero.
    Inputs  : nums — array of integers to search inside.
    Output  : List[List[int]] — sorted triplets, no duplicates.
    """

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result: List[List[int]] = []
        n = len(nums)
        if n < 3:
            return result

        # Sort for ONLY one reason: the dedupe tuple (a,b,c) must be
        # canonical, so every triplet is serialized in sorted order.
        nums.sort()

        # Dedupe set of canonical tuples — open addressing + probing.
        seen: set[Tuple[int, int, int]] = set()

        for i in range(n - 2):
            if nums[i] > 0:
                break
            # seen-value set for the inner 2-sum: value -> visited.
            partners: set[int] = set()

            for j in range(i + 1, n):
                # The complement that would complete 0 with nums[i]+nums[j].
                need = -(nums[i] + nums[j])
                if need in partners:
                    # Canonical sorted triple (nums[i] ≤ need ≤ nums[j]
                    # because we scan j left→right) → unique key.
                    trip = (nums[i], need, nums[j])
                    if trip not in seen:
                        seen.add(trip)
                        result.append([nums[i], need, nums[j]])
                partners.add(nums[j])
        return result


# =====================================================================
# BENCHMARK — verify both solutions on real test cases + time/RAM
# =====================================================================
if __name__ == "__main__":
    # Case 1: official example — two unique triplets.
    # Case 2: only zeros — exactly ONE triplet, not three.
    # Case 3: no triplet sums to zero (all distinct, small).
    tests: List[Tuple[List[int], int]] = [
        ([-1, 0, 1, 2, -1, -4], 2),
        ([0, 0, 0, 0], 1),
        ([1, 2, 3, 4, 5], 0),
    ]

    # Aggregate time + peak memory across all cases, per approach.
    time_us: List[float] = [0.0, 0.0]
    peak_kb: List[float] = [0.0, 0.0]
    all_pass = True

    for t, (nums, expected_count) in enumerate(tests, 1):
        # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().threeSum(list(nums))
        t1 = time.perf_counter()
        _, peak_1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[0] += (t1 - t0) * 1e6
        peak_kb[0] = max(peak_kb[0], peak_1 / 1024.0)

        # --- Approach 2: same instrumentation ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().threeSum(list(nums))
        t1b = time.perf_counter()
        _, peak_2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        time_us[1] += (t1b - t0b) * 1e6
        peak_kb[1] = max(peak_kb[1], peak_2 / 1024.0)

        # Verify: count matches AND every triplet really sums to zero.
        ok = len(r1) == expected_count and len(r2) == expected_count
        ok = ok and all(sum(trip) == 0 for trip in r1)
        ok = ok and all(sum(trip) == 0 for trip in r2)
        all_pass = all_pass and ok
        print(f"Test {t}: sort2Ptr={len(r1)} hashMap={len(r2)} expected={expected_count}  {'PASS' if ok else 'FAIL'}")

    print("---")
    print(f"Approach 1 (sort + two pointers) : {time_us[0]:.2f} µs total, peak {peak_kb[0]:.2f} KB")
    print(f"Approach 2 (pivot + hash map)    : {time_us[1]:.2f} µs total, peak {peak_kb[1]:.2f} KB")
    print("PASS : all cases" if all_pass else "FAIL : at least one case")