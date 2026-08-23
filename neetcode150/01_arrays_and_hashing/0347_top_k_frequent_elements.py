"""
=====================================================================
LeetCode 347 : Top K Frequent Elements                          (Medium)
https://leetcode.com/problems/top-k-frequent-elements/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Given an integer array nums and an integer k, return the k most
    frequent elements (any order).
---------------------------------------------------------------------
INTUITION
    Two jobs: (1) count frequencies — hash map, O(n); (2) pick the
    k largest frequencies. Since frequencies live in [1..n], a
    frequency-indexed BUCKET ARRAY collects the answer in O(n).
---------------------------------------------------------------------
APPROACH 1 — Counter + bucket sort (BEST)
    buckets[f] = values appearing exactly f times. Walk buckets from
    high f down until k collected.
    Time  Complexity : O(n)   Space Complexity : O(n)
    WHY bucket sort beats a heap here: the frequency range is bounded
    by n, so counting-style sort is LINEAR; a heap pays O(log k) per
    push even when k ≈ n.
---------------------------------------------------------------------
APPROACH 2 — Counter + min-heap of size k
    Time  Complexity : O(n log k)   Space Complexity : O(n)
    Wins when k ≪ n and data arrives streaming (no full array).
=====================================================================
"""

from __future__ import annotations
import heapq
import time
import tracemalloc
from collections import Counter
from typing import List


# =====================================================================
# APPROACH 1 : Counter + bucket sort — O(n)
# =====================================================================
class Solution_BucketSort:
    """
    Purpose : Return the k most frequent elements of nums.
    Inputs  : nums — array of integers; k — how many top elements.
    Output  : list with the k most frequent values.
    """

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # count : value → frequency. Counter is a dict subclass
        # (open addressing + linear probing) — O(n) counting pass.
        count = Counter(nums)

        # buckets[f] = values that appear exactly f times.
        # Frequency never exceeds n → list of n+1 empty lists suffices.
        buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
        for value, freq in count.items():
            buckets[freq].append(value)

        # Collect answers from the highest frequency downward.
        result: List[int] = []
        for freq in range(len(buckets) - 1, 0, -1):
            for value in buckets[freq]:
                result.append(value)
                # Stop the moment we have k elements — O(n) total.
                if len(result) == k:
                    return result
        return result


# =====================================================================
# APPROACH 2 : Counter + min-heap of size k — O(n log k)
# =====================================================================
class Solution_MinHeap:
    """
    Purpose : Return the k most frequent elements of nums.
    Inputs  : nums — array of integers; k — how many top elements.
    Output  : list with the k most frequent values.
    """

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # count : value → frequency (same counting pass as approach 1).
        count = Counter(nums)

        # Min-heap of (frequency, value): smallest frequency on top.
        # heapq maintains the heap invariant in O(log k) per push.
        heap: List[tuple] = []

        # Push every (freq, value); evict the smallest when over k.
        for value, freq in count.items():
            heapq.heappush(heap, (freq, value))
            # Size k+1 → the least frequent of the kept ones must leave.
            if len(heap) > k:
                heapq.heappop(heap)

        # The heap now holds exactly the k largest frequencies.
        return [value for _, value in heap]


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    # Official example with plenty of duplicates.
    nums = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6]
    k = 3  # expect {4, 5, 1} in some order

    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_BucketSort().topKFrequent(nums, k)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    r2 = Solution_MinHeap().topKFrequent(nums, k)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (bucket sort)      : {sorted(r1)}  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (min-heap k)       : {sorted(r2)}  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree." if sorted(r1) == sorted(r2) else "FAIL : approaches disagree.")