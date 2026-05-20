"""LeetCode 54: Spiral Matrix - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: Boundaries simulation
class Solution_v1:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        left, right = 0, len(matrix[0])
        top, bottom = 0, len(matrix)
        while left < right and top < bottom:
            for i in range(left, right): res.append(matrix[top][i])
            top += 1
            for i in range(top, bottom): res.append(matrix[i][right - 1])
            right -= 1
            if not (left < right and top < bottom): break
            for i in range(right - 1, left - 1, -1): res.append(matrix[bottom - 1][i])
            bottom -= 1
            for i in range(bottom - 1, top - 1, -1): res.append(matrix[i][left])
            left += 1
        return res
if __name__ == "__main__":
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    tracemalloc.start(); t0=time.perf_counter()
    r = Solution_v1().spiralOrder(matrix)
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
