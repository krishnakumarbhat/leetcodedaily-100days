"""
LeetCode 74: Search a 2D Matrix
Link: https://leetcode.com/problems/search-a-2d-matrix/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Iterate through each row and use the `in` operator to search.
# Time Complexity: O(m*n)   Space Complexity: O(1)
class Solution_v1:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            if target in row: return True
        return False

# ============= Variation 2: Binary Search (flattened) =============
# Algorithm: Treat the 2D matrix as a virtual 1D array. Map the 1D index `mid` 
# to 2D coordinates `[mid // n][mid % n]`.
# Time Complexity: O(log(m*n))   Space Complexity: O(1)
class Solution_v2:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        l, r = 0, m * n - 1
        while l <= r:
            mid = (l + r) // 2
            val = matrix[mid // n][mid % n]
            if val == target: return True
            elif val < target: l = mid + 1
            else: r = mid - 1
        return False

if __name__ == "__main__":
    matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]; target = 3
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Binary Search"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().searchMatrix(matrix, target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1544 bytes and time = 8.90 µs
# var2 mem = 528 bytes and time = 8.41 µs
