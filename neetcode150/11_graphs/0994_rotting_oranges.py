"""LeetCode 994: Rotting Oranges - Medium"""
import time, tracemalloc
from collections import deque
from typing import List
import copy

# Variation 1: Multi-source BFS
class Solution_v1:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows,cols=len(grid),len(grid[0]); q=deque(); fresh=0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]==2: q.append((r,c,0))
                elif grid[r][c]==1: fresh+=1
        time_val=0
        while q:
            r,c,t=q.popleft(); time_val=max(time_val,t)
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1:
                    grid[nr][nc]=2; fresh-=1; q.append((nr,nc,t+1))
        return time_val if fresh==0 else -1

# Variation 2: Level-by-level BFS
class Solution_v2:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows,cols=len(grid),len(grid[0]); q=deque(); fresh=0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]==2: q.append((r,c))
                elif grid[r][c]==1: fresh+=1
        minutes=0
        while q and fresh:
            minutes+=1
            for _ in range(len(q)):
                r,c=q.popleft()
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==1:
                        grid[nr][nc]=2; fresh-=1; q.append((nr,nc))
        return minutes if fresh==0 else -1

if __name__ == "__main__":
    grid_orig=[[2,1,1],[1,1,0],[0,1,1]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        g=copy.deepcopy(grid_orig)
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().orangesRotting(g)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: minutes={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
