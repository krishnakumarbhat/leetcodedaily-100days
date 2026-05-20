"""LeetCode 286: Walls and Gates (Fill Rooms) - Medium"""
import time, tracemalloc
from collections import deque
from typing import List
import copy

INF = 2147483647

# Variation 1: Multi-source BFS from gates
class Solution_v1:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        if not rooms: return
        rows,cols=len(rooms),len(rooms[0]); q=deque()
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c]==0: q.append((r,c))
        while q:
            r,c=q.popleft()
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<rows and 0<=nc<cols and rooms[nr][nc]==INF:
                    rooms[nr][nc]=rooms[r][c]+1; q.append((nr,nc))

# Variation 2: DFS from each gate
class Solution_v2:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        rows,cols=len(rooms),len(rooms[0])
        def dfs(r,c,dist):
            if r<0 or r>=rows or c<0 or c>=cols or rooms[r][c]<dist: return
            rooms[r][c]=dist
            dfs(r+1,c,dist+1);dfs(r-1,c,dist+1);dfs(r,c+1,dist+1);dfs(r,c-1,dist+1)
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c]==0: dfs(r,c,0)

if __name__ == "__main__":
    grid_orig=[[INF,-1,0,INF],[INF,INF,INF,-1],[INF,-1,INF,-1],[0,-1,INF,INF]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        g=copy.deepcopy(grid_orig)
        tracemalloc.start(); t0=time.perf_counter()
        Cls().wallsAndGates(g)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: done, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
