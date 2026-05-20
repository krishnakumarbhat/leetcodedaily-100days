"""
LeetCode 347: Top K Frequent Elements
Link: https://leetcode.com/problems/top-k-frequent-elements/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List
from collections import Counter
import heapq

# ============= Variation 1: Sorting =============
# Algorithm: Hash map to count frequencies, then sort the unique keys by 
# their frequency in descending order, returning the first k elements.
# Time Complexity: O(n log n)   Space Complexity: O(n)
class Solution_v1:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        return [x for x, _ in count.most_common(k)]

# ============= Variation 2: Min Heap =============
# Algorithm: Hash map to count frequencies. Maintain a min-heap of size k.
# Iterating through frequencies, push to heap. If size > k, pop the minimum.
# The remaining k elements in the heap are the most frequent.
# Time Complexity: O(n log k)   Space Complexity: O(n)
class Solution_v2:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)

# ============= Variation 3: Bucket Sort =============
# Algorithm: Hash map to count frequencies. Create an array of lists ('buckets') 
# where index represents the frequency and the list contains numbers with that 
# frequency. Loop backwards from the highest possible frequency (n) down to 0, 
# gathering elements until we have k elements.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v3:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)
        result = []
        for i in range(len(buckets) - 1, -1, -1):
            for num in buckets[i]:
                result.append(num)
                if len(result) == k:
                    return result
        return result

# ============= Benchmarking =============
if __name__ == "__main__":
    nums = [1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 5, 5]
    k = 2
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Sorting", "Min Heap", "Bucket Sort"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().topKFrequent(nums[:], k)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 7211 bytes and time = 144.99 µs
# var2 mem = 1264 bytes and time = 34.25 µs
# var3 mem = 2240 bytes and time = 31.40 µs
