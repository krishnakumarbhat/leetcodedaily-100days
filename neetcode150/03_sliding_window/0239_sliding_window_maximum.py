"""
=====================================================================
LeetCode 239 : Sliding Window Maximum                         (Hard)
https://leetcode.com/problems/sliding-window-maximum/
Category   : Sliding Window
---------------------------------------------------------------------
PROBLEM
    Given `nums` and window size `k`, return an array holding the
    maximum of EVERY contiguous window of length k. Windows start
    at index 0, 1, ..., n−k.
---------------------------------------------------------------------
INTUITION
    A max-heap gives the max in O(log n) per op; a monotonic deque
    gives it in O(1) amortized. The deque keeps candidate maxima
    with TWO invariants: (1) indices strictly increasing along the
    deque, (2) values strictly DECREASING. The front is therefore
    the window's maximum, and anything smaller than the newcomer
    can never become a maximum again → discard it forever.
---------------------------------------------------------------------
APPROACH 1 — Monotonic deque of indices (BEST)
    For each i: pop front while it falls outside the window, pop
    back while values ≤ nums[i] (dominated), push i, then once the
    window is full record nums[front].
    Time  Complexity : O(n)   Space Complexity : O(k)
---------------------------------------------------------------------
APPROACH 2 — Max-heap with lazy deletion
    Push (−value, index) pairs (max-heap via negation). The root is
    the global max; before reading it, lazily pop roots that have
    slid out of the window (index ≤ i − k). Stale roots are removed
    only when they reach the top.
    Time  Complexity : O(n log n)   Space Complexity : O(n)
---------------------------------------------------------------------
DEEP DIVE — deque vs heap
    collections.deque (Python) / std::deque (C++): O(1) push/pop on
    BOTH ends — exactly what the monotonic queue needs. The heap
    (heapq / std::priority_queue) cannot remove ARBITRARY stale
    entries cheaply → lazy deletion, deferring cleanup until the
    stale root actually blocks the answer. The monotonic-deque trick
    removes the waste: each element is compared to its back
    neighbours and discarded exactly once — that single fact is what
    turns O(n log n) into O(n).
---------------------------------------------------------------------
REAL LIFE
    • Network packet monitoring: max latency over every trailing
      window of 60 s, without a per-window rescan.
    • Streaming analytics: rolling maxima of sensor/telemetry
      streams (CPU, disk queue depth) in O(1) per reading.
=====================================================================
"""

from __future__ import annotations

import time
import tracemalloc
import heapq
from collections import deque
from typing import Deque, List, Tuple


# =====================================================================
# APPROACH 1 : Monotonic deque of indices (O(n))
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the maximum of every length-k window of `nums`.
    Inputs  : nums — the array to slide over.
              k    — window size (1 ≤ k ≤ n).
    Output  : List[int] of size n−k+1 with window maxima.
    """

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # dq : INDICES, front→back = increasing index, decreasing value.
        # Front is always the current window's maximum.
        dq: Deque[int] = deque()
        result: List[int] = []

        for i, num in enumerate(nums):
            # Invariant 1: drop indices that slid out of the window.
            # Window is [i−k+1 .. i], so front must satisfy ≥ i−k+1.
            while dq and dq[0] < i - k + 1:
                dq.popleft()
            # Invariant 2: while the back value is ≤ nums[i], that
            # back index is dominated — nums[i] is newer AND bigger,
            # so it will outlive it as the window's max. Pop forever.
            while dq and nums[dq[-1]] <= num:
                dq.pop()
            # nums[i] enters as the new (potential) maximum tail.
            dq.append(i)
            # Window complete? Then the front is its maximum.
            if i >= k - 1:
                result.append(nums[dq[0]])
        return result


# =====================================================================
# APPROACH 2 : Max-heap with lazy deletion (O(n log n))
# =====================================================================
class SolutionTwo:
    """
    Purpose : Return the maximum of every length-k window of `nums`.
    Inputs  : nums — the array to slide over.
              k    — window size (1 ≤ k ≤ n).
    Output  : List[int] of size n−k+1 with window maxima.
    """

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # heap : max-heap stored as (−value, index) pairs — heapq is
        # a MIN-heap, so negating values makes the root the maximum.
        heap: List[Tuple[int, int]] = []
        result: List[int] = []

        for i, num in enumerate(nums):
            # Every newcomer enters the heap; it may be the answer.
            heapq.heappush(heap, (-num, i))

            # Window [i−k+1 .. i] is complete → record its maximum.
            if i >= k - 1:
                # Lazy deletion: the root might be a stale index that
                # already slid out of the window — evict until the
                # root is one we can still legally use.
                while heap[0][1] <= i - k:
                    heapq.heappop(heap)
                # Root = largest value among live in-window indices.
                result.append(-heap[0][0])
        return result


# =====================================================================
# BENCHMARK — run both approaches on 3 tests + a longer series,
# compare time and peak memory (tracemalloc), print PASS/FAIL.
# =====================================================================
if __name__ == "__main__":
    tests: List[Tuple[List[int], int, List[int]]] = [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),  # official
        ([1], 1, [1]),                # single element, k=1
        ([9, 8, 7, 6], 2, [9, 8, 7]), # decreasing series
    ]

    all_pass = True
    for nums, k, expected in tests:
        r1 = SolutionOne().maxSlidingWindow(nums, k)
        r2 = SolutionTwo().maxSlidingWindow(nums, k)
        ok = r1 == expected and r2 == expected
        all_pass = all_pass and ok
        print(f"{'PASS' if ok else 'FAIL'} nums={nums} k={k} expected={expected}  deque={r1}  heap={r2}")

    # Longer zig-zag series so both data structures do real work.
    bench: List[int] = [(i * 37) % 1000 for i in range(20000)]

    # --- Approach 1: time + peak memory ---
    tracemalloc.start()
    t0 = time.perf_counter()
    b1 = SolutionOne().maxSlidingWindow(bench, 100)
    t1 = time.perf_counter()
    _, peak_1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # --- Approach 2: time + peak memory ---
    tracemalloc.start()
    t2 = time.perf_counter()
    b2 = SolutionTwo().maxSlidingWindow(bench, 100)
    t3 = time.perf_counter()
    _, peak_2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (monotonic deque) : size={len(b1)}  time={(t1 - t0) * 1e6:.2f} µs  peak-mem={peak_1} bytes")
    print(f"Approach 2 (max heap + lazy) : size={len(b2)}  time={(t3 - t2) * 1e6:.2f} µs  peak-mem={peak_2} bytes")

    # Both approaches must produce identical maxima on the big series.
    all_pass = all_pass and (b1 == b2)
    print("PASS : all test cases and benchmark agree." if all_pass
          else "FAIL : at least one answer is wrong.")
