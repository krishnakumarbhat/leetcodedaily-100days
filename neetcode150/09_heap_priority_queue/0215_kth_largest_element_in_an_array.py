"""LeetCode 215: Kth Largest Element in an Array - Medium"""
import time, tracemalloc
import heapq, random
from typing import List

# Variation 1: Sort descending O(n log n)
class Solution_v1:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        return sorted(nums, reverse=True)[k - 1]

# Variation 2: Min-heap of size k O(n log k)
class Solution_v2:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for n in nums:
            heapq.heappush(heap, n)
            if len(heap) > k: heapq.heappop(heap)
        return heap[0]

# Variation 3: QuickSelect O(n) average
class Solution_v3:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        k = len(nums) - k  # convert to kth smallest index
        def quickselect(l, r):
            pivot, p = nums[r], l
            for i in range(l, r):
                if nums[i] <= pivot:
                    nums[p], nums[i] = nums[i], nums[p]; p += 1
            nums[p], nums[r] = nums[r], nums[p]
            if p < k: return quickselect(p + 1, r)
            elif p > k: return quickselect(l, p - 1)
            return nums[p]
        return quickselect(0, len(nums) - 1)

# Variation 4: Randomized QuickSelect O(n) avg with shuffle
class Solution_v4:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        random.shuffle(nums)
        k = len(nums) - k
        def qs(l, r):
            pivot, p = nums[r], l
            for i in range(l, r):
                if nums[i] <= pivot:
                    nums[p], nums[i] = nums[i], nums[p]; p += 1
            nums[p], nums[r] = nums[r], nums[p]
            if p < k: return qs(p + 1, r)
            elif p > k: return qs(l, p - 1)
            return nums[p]
        return qs(0, len(nums) - 1)

if __name__ == "__main__":
    import copy
    nums = [3, 2, 1, 5, 6, 4]; k = 2
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3, Solution_v4], 1):
        n = copy.deepcopy(nums)
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().findKthLargest(n, k)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: result={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
# var4 mem = {} and time = {}
