"""LeetCode 200: Number of Islands - Medium"""
import time, tracemalloc
from collections import deque
from typing import List
import copy

# Variation 1: DFS recursive
class Solution_v1:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid: return 0
        rows, cols, count = len(grid), len(grid[0]), 0
        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1': return
            grid[r][c] = '0'
            dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1': count += 1; dfs(r, c)
        return count

# Variation 2: BFS
class Solution_v2:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid: return 0
        rows, cols, count = len(grid), len(grid[0]), 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1; q = deque([(r,c)]); grid[r][c] = '0'
                    while q:
                        cr, cc = q.popleft()
                        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                            nr, nc = cr+dr, cc+dc
                            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]=='1':
                                grid[nr][nc] = '0'; q.append((nr, nc))
        return count

# Variation 3: Union Find
class Solution_v3:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid: return 0
        rows, cols = len(grid), len(grid[0])
        parent = list(range(rows * cols)); rank = [0] * (rows * cols)
        count = sum(grid[r][c] == '1' for r in range(rows) for c in range(cols))
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(a, b):
            nonlocal count
            pa, pb = find(a), find(b)
            if pa == pb: return
            if rank[pa] < rank[pb]: pa, pb = pb, pa
            parent[pb] = pa
            if rank[pa] == rank[pb]: rank[pa] += 1
            count -= 1
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    for dr,dc in [(1,0),(0,1)]:
                        nr, nc = r+dr, c+dc
                        if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]=='1':
                            union(r*cols+c, nr*cols+nc)
        return count

if __name__ == "__main__":
    grid_orig = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3], 1):
        g = copy.deepcopy(grid_orig)
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().numIslands(g)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: islands={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
