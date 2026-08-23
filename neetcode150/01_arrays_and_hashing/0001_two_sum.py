"""
=====================================================================
LeetCode 1 : Two Sum                                             (Easy)
https://leetcode.com/problems/two-sum/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Given an array of integers `nums` and an integer `target`, return
    the indices of the two numbers that add up to `target`.
    Exactly ONE valid answer exists. You may not use the same element
    twice.
---------------------------------------------------------------------
INTUITION
    For every number we only care about ONE thing: "have I already
    seen its partner `target - num` earlier?" A hash map turns that
    question from an O(n) scan into an O(1) lookup.
---------------------------------------------------------------------
APPROACH 1 — One-pass hash map (BEST)
    Walk the array once. Before inserting `num`, check whether its
    complement `target - num` is already in the map.
    Time  Complexity : O(n)   Space Complexity : O(n)
    WHY dict (and not a list / sort): dict is an open-addressing hash
    table using LINEAR PROBING:
        h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
    Collisions walk to the next free slot inside ONE contiguous array
    → excellent cache locality + tiny memory footprint.
---------------------------------------------------------------------
APPROACH 2 — Sort + two pointers (no hash map)
    Pair each value with its original index, sort, then let `l` and
    `r` meet in the middle adjusting by the sum sign.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
REAL LIFE
    • Caches (LRU on dicts), autocomplete, duplicate detection in
      banking ledgers — "have I seen this key?" is a hash-table op.
    • Any 'find a partner for every item' problem (pairing, hashing
      file chunks, spell-check suggestions).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Optional

# =====================================================================
# APPROACH 1 : One-pass hash map (best)
# =====================================================================
class Solution_OnePassHashmap:
    """
    Purpose : Return the two indices whose values sum to `target`.
    Inputs  : nums   — list of integers to search inside.
              target — the sum we must form with two distinct elements.
    Output  : List[int] of size 2 with the answer indices.
    """

    def twoSum(self, nums: List[int], target: int) -> Optional[List[int]]:
        # seen : value -> index  (Python dict = open addressing, linear probing)
        seen: dict[int, int] = {}

        # Walk every element exactly once — this is the single O(n) pass.
        for i, num in enumerate(nums):

            # complement = the partner that would complete the sum.
            need = target - num

            # Probe the table BEFORE inserting: the partner must come from
            # an EARLIER index, so we can never reuse the same element.
            if need in seen:
                # found → answer = (partner's stored index, current index)
                return [seen[need], i]

            # Partner not seen yet → remember this value for the future.
            seen[num] = i

        # Problem guarantees an answer, but keep the return contract honest.
        return None

# =====================================================================
# APPROACH 2 : Sort + two pointers (no hash map at all)
# =====================================================================
class Solution_SortTwoPointers:
    """
    Purpose : Return the two indices whose values sum to `target`.
    Inputs  : nums   — list of integers to search inside.
              target — the sum we must form with two distinct elements.
    Output  : List[int] of size 2 with the answer indices.
    """

    def twoSum(self, nums: List[int], target: int) -> Optional[List[int]]:
        # Bundle every value with its ORIGINAL index — sorting would
        # otherwise destroy the indices we are asked to return.
        pairs = [(num, i) for i, num in enumerate(nums)]

        # Sort by value (tuples sort by first element first) — O(n log n).
        pairs.sort()

        # Two pointers: l hunts from the small end, r from the big end.
        l, r = 0, len(pairs) - 1

        # The pointers converge, so we inspect O(n) pairs total.
        while l < r:
            # Current sum of the two pointed-to values.
            current_sum = pairs[l][0] + pairs[r][0]

            if current_sum == target:
                # Exact match → hand back the original indices.
                return [pairs[l][1], pairs[r][1]]
            if current_sum < target:
                # Sum too small → the only way to grow it is to move the
                # left pointer toward bigger values.
                l += 1
            else:
                # Sum too big → shrink it by pulling the right pointer
                # toward smaller values.
                r -= 1

        # Unreachable per problem statement; keeps the type checker happy.
        return None


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Fixed sample from the official examples + extra elements so the
    # benchmark is not trivially fast. NOTE: extra values may create
    # ADDITIONAL valid pairs — the check only requires a valid pair.
    nums = [2, 7, 11, 15, 3, 6, 1, 4, 9, 8, 5, 10]
    target = 9

    # --- Approach 1: time + peak memory (tracemalloc snapshot) ---
    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_OnePassHashmap().twoSum(nums, target)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t0b = time.perf_counter()
    r2 = Solution_SortTwoPointers().twoSum(nums, target)
    t1b = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Print both results in a compact, comparable format.
    print(f"Approach 1 (one-pass hash map) : {r1}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak_1} bytes")
    print(f"Approach 2 (sort + two pointers): {r2}  time = {(t1b - t0b) * 1e6:.2f} µs  peak-mem = {peak_2} bytes")

    # Sanity check: each answer must (a) use distinct indices and
    # (b) actually sum to the target — the real acceptance criteria.
    def valid(r: Optional[List[int]]) -> bool:
        return r is not None and len(r) == 2 and r[0] != r[1] and nums[r[0]] + nums[r[1]] == target

    print("PASS : both approaches return valid pairs summing to target."
          if valid(r1) and valid(r2)
          else "FAIL : at least one answer is wrong.")