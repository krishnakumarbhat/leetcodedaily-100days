"""LeetCode 778: Swim in Rising Water - Hard"""
import time, tracemalloc
import heapq
from typing import List

# Variation 1: Dijkstra (min-heap on max elevation path)
class Solution_v1:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n=len(grid); visited=set()
        heap=[(grid[0][0],0,0)]
        while heap:
            t,r,c=heapq.heappop(heap)
            if (r,c) in visited: continue
            visited.add((r,c))
            if r==n-1 and c==n-1: return t
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<n and 0<=nc<n and (nr,nc) not in visited:
                    heapq.heappush(heap,(max(t,grid[nr][nc]),nr,nc))
        return -1

# Variation 2: Binary search + BFS
class Solution_v2:
    def swimInWater(self, grid: List[List[int]]) -> int:
        from collections import deque
        n=len(grid)
        def canReach(t):
            if grid[0][0]>t: return False
            q=deque([(0,0)]); vis={( 0,0)}
            while q:
                r,c=q.popleft()
                if r==n-1 and c==n-1: return True
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<n and 0<=nc<n and (nr,nc) not in vis and grid[nr][nc]<=t:
                        vis.add((nr,nc)); q.append((nr,nc))
            return False
        lo,hi=0,n*n-1
        while lo<hi:
            mid=(lo+hi)//2
            if canReach(mid): hi=mid
            else: lo=mid+1
        return lo

if __name__ == "__main__":
    grid=[[0,2],[1,3]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().swimInWater(grid)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: time={r}, mem={mem}bytes, time_us={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
