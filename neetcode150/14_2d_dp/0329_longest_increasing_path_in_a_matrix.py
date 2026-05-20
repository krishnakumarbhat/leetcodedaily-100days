"""LeetCode 329: Longest Increasing Path in a Matrix - Hard"""
import time, tracemalloc
from typing import List
from functools import lru_cache
# Variation 1: DFS + memo
class Solution_v1:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows,cols=len(matrix),len(matrix[0])
        @lru_cache(None)
        def dfs(r,c):
            best=1
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<rows and 0<=nc<cols and matrix[nr][nc]>matrix[r][c]:
                    best=max(best,1+dfs(nr,nc))
            return best
        return max(dfs(r,c) for r in range(rows) for c in range(cols))
if __name__ == "__main__":
    matrix=[[9,9,4],[6,6,8],[2,1,1]]
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().longestIncreasingPath(matrix)
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: lip={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
