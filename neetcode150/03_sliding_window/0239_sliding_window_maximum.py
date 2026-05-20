"""
LeetCode 239: Sliding Window Maximum
Link: https://leetcode.com/problems/sliding-window-maximum/
Difficulty: Hard
"""
import time, tracemalloc
from typing import List
from collections import deque
import heapq

# ============= Variation 1: Brute Force =============
# Algorithm: Python list slicing taking explicit `max()` for every `i` stepping window.
# Time Complexity: O(n*k)   Space Complexity: O(n)
class Solution_v1:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        return [max(nums[i:i+k]) for i in range(len(nums) - k + 1)]

# ============= Variation 2: Monotonic Deque =============
# Algorithm: Store indices dynamically. Pop left if out of bounds. Pop back if 
# current value strictly dominates stack. Peak of deque is iteratively window max.
# Time Complexity: O(n)   Space Complexity: O(k)
class Solution_v2:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque(); result = []
        for i in range(len(nums)):
            while dq and dq[0] < i - k + 1: dq.popleft()
            while dq and nums[dq[-1]] < nums[i]: dq.pop()
            dq.append(i)
            if i >= k - 1: result.append(nums[dq[0]])
        return result

# ============= Variation 3: Max Heap =============
# Algorithm: Push neg elements and tuple indices natively. Lazily pop root 
# elements if they naturally fall out of bounds (`current i - k`).
# Time Complexity: O(n log n)   Space Complexity: O(n)
class Solution_v3:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        heap = []; result = []
        for i in range(len(nums)):
            heapq.heappush(heap, (-nums[i], i))
            if i >= k - 1:
                while heap[0][1] <= i - k: heapq.heappop(heap)
                result.append(-heap[0][0])
        return result

if __name__ == "__main__":
    nums, k = [1, 3, -1, -3, 5, 3, 6, 7, 2, 4], 3
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2, Solution_v3], ["Brute", "Deque", "Heap"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().maxSlidingWindow(nums[:], k)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1560 bytes and time = 47.15 µs
# var2 mem = 1928 bytes and time = 37.02 µs
# var3 mem = 1288 bytes and time = 23.26 µs
