"""
=====================================================================
LeetCode 215 : Kth Largest Element in an Array                    (Medium)
https://leetcode.com/problems/kth-largest-element-in-an-array/
Category   : Heap / Priority queue
---------------------------------------------------------------------
PROBLEM
    Return the k-th largest element of an unsorted array (1-indexed).
    Sorting is allowed but wasteful: we only need ONE element.
---------------------------------------------------------------------
INTUITION
    Keep a min-heap of size k holding the k largest values seen so
    far; its root is exactly the k-th largest. Every push is O(log k).
---------------------------------------------------------------------
APPROACH 1 · Min-heap of size k (best)
    1. Push each value; if len(heap) > k, heappop (removes the
       smallest — the value that just fell out of the top-k).
    2. After the sweep, heap[0] is the k-th largest.
APPROACH 2 · Quickselect (Hoare's partition)
    Partition around a pivot; if the pivot lands at index len-k it IS
    the answer; otherwise recurse into the correct half. O(n) average.
---------------------------------------------------------------------
DEEP DIVE · Why a MIN-heap, not a max-heap
    A max-heap lets you pop the largest repeatedly, but the heap
    "loses" the k-th largest once you pop it. The min-heap of size k
    tracks the boundary of the top-k: new elements smaller than the
    root are ignored implicitly by the pop. Python's heapq is a
    min-heap natively — zero configuration.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n log k)   — n pushes, each O(log k).
MEMORY COMPLEXITY: O(k)          — the heap holds at most k values.
=====================================================================
"""
import heapq, random, time, tracemalloc


class Solution_1:
    """Min-heap of size k keeps the top-k boundary."""

    def findKthLargest(self, nums, k):
        heap = []
        for x in nums:
            heapq.heappush(heap, x)
            if len(heap) > k:
                heapq.heappop(heap)          # eject the smallest of top-k
        return heap[0]


class Solution_2:
    """Quickselect — Hoare partition, average O(n)."""

    def findKthLargest(self, nums, k):
        def select(lo, hi):                  # 0-indexed target index
            pivot = nums[random.randint(lo, hi)]
            left, mid, right = lo, lo, hi
            while mid <= right:              # 3-way partition
                if nums[mid] < pivot:
                    nums[left], nums[mid] = nums[mid], nums[left]
                    left += 1; mid += 1
                elif nums[mid] > pivot:
                    nums[mid], nums[right] = nums[right], nums[mid]
                    right -= 1
                else:
                    mid += 1
            if len(nums) - k < left:
                return select(lo, left - 1)
            if len(nums) - k > right:
                return select(right + 1, hi)
            return nums[left]

        return select(0, len(nums) - 1)


if __name__ == "__main__":
    cases = [([3, 2, 1, 5, 6, 4], 2, 5),
             ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
             ([1], 1, 1)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for nums, k, want in cases:
        r1 = Solution_1().findKthLargest(nums[:], k)
        r2 = Solution_2().findKthLargest(nums[:], k)
        ok &= r1 == want and r2 == want
        print(f"k={k} -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt * 1e6:.0f} us | mem: {mem:.0f} KB")
