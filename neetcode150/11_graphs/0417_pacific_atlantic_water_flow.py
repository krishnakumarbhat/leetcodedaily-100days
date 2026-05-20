"""LeetCode 417: Pacific Atlantic Water Flow - Medium"""
import time, tracemalloc
from collections import deque
from typing import List

# Variation 1: DFS from ocean borders inward
class Solution_v1:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        pac, atl = set(), set()
        def dfs(r, c, visit, prev_h):
            if r<0 or r>=rows or c<0 or c>=cols or (r,c) in visit or heights[r][c]<prev_h: return
            visit.add((r,c))
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]: dfs(r+dr,c+dc,visit,heights[r][c])
        for c in range(cols): dfs(0,c,pac,heights[0][c]); dfs(rows-1,c,atl,heights[rows-1][c])
        for r in range(rows): dfs(r,0,pac,heights[r][0]); dfs(r,cols-1,atl,heights[r][cols-1])
        return [[r,c] for r,c in pac & atl]

# Variation 2: BFS from ocean borders
class Solution_v2:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        rows, cols = len(heights), len(heights[0])
        def bfs(starts):
            visit = set(starts); q = deque(starts)
            while q:
                r,c = q.popleft()
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc = r+dr,c+dc
                    if 0<=nr<rows and 0<=nc<cols and (nr,nc) not in visit and heights[nr][nc]>=heights[r][c]:
                        visit.add((nr,nc)); q.append((nr,nc))
            return visit
        pac = bfs([(0,c) for c in range(cols)] + [(r,0) for r in range(rows)])
        atl = bfs([(rows-1,c) for c in range(cols)] + [(r,cols-1) for r in range(rows)])
        return [[r,c] for r,c in pac & atl]

if __name__ == "__main__":
    heights=[[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().pacificAtlantic(heights)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {len(r)} cells, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
