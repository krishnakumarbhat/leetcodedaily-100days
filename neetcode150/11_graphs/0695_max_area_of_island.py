"""LeetCode 695: Max Area of Island - Medium"""
import time, tracemalloc
from collections import deque
from typing import List
import copy

# Variation 1: DFS recursive
class Solution_v1:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols, mx = len(grid), len(grid[0]), 0
        def dfs(r, c):
            if r<0 or r>=rows or c<0 or c>=cols or grid[r][c]!=1: return 0
            grid[r][c]=0
            return 1+dfs(r+1,c)+dfs(r-1,c)+dfs(r,c+1)+dfs(r,c-1)
        for r in range(rows):
            for c in range(cols): mx=max(mx, dfs(r,c))
        return mx

# Variation 2: BFS
class Solution_v2:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        rows, cols, mx = len(grid), len(grid[0]), 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]==1:
                    area=0; q=deque([(r,c)]); grid[r][c]=0
                    while q:
                        cr,cc=q.popleft(); area+=1
                        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                            nr,nc=cr+dr,cc+dc
                            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1:
                                grid[nr][nc]=0; q.append((nr,nc))
                    mx=max(mx, area)
        return mx

if __name__ == "__main__":
    grid_orig=[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        g=copy.deepcopy(grid_orig)
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().maxAreaOfIsland(g)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: max_area={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
