"""
LeetCode 4: Median of Two Sorted Arrays
Link: https://leetcode.com/problems/median-of-two-sorted-arrays/
Difficulty: Hard
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Merge + Sort =============
# Algorithm: Concatenate both arrays and sort them. Find the middle element(s) 
# to calculate the median.
# Time Complexity: O((m+n) log(m+n))   Space Complexity: O(m+n)
class Solution_v1:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = sorted(nums1 + nums2)
        n = len(merged)
        if n % 2: return merged[n // 2]
        return (merged[n // 2 - 1] + merged[n // 2]) / 2

# ============= Variation 2: Binary Search =============
# Algorithm: Partition both arrays such that the left halves have equal or one 
# more total element than right halves. Use binary search on the smaller array 
# to find the correct partition point where `Aleft <= Bright` and `Bleft <= Aright`.
# Time Complexity: O(log(min(m,n)))   Space Complexity: O(1)
class Solution_v2:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        if len(A) > len(B): A, B = B, A
        total = len(A) + len(B)
        half = total // 2
        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2
            j = half - i - 2
            Aleft = A[i] if i >= 0 else float('-inf')
            Aright = A[i + 1] if (i + 1) < len(A) else float('inf')
            Bleft = B[j] if j >= 0 else float('-inf')
            Bright = B[j + 1] if (j + 1) < len(B) else float('inf')
            if Aleft <= Bright and Bleft <= Aright:
                if total % 2: return min(Aright, Bright)
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright: r = i - 1
            else: l = i + 1

if __name__ == "__main__":
    nums1, nums2 = [1, 3, 5, 7], [2, 4, 6, 8, 10]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Merge+Sort", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().findMedianSortedArrays(nums1[:], nums2[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1728 bytes and time = 18.25 µs
# var2 mem = 752 bytes and time = 9.76 µs
