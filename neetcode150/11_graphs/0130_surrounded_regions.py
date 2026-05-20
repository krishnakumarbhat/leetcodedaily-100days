"""LeetCode 130: Surrounded Regions - Medium"""
import time, tracemalloc
from typing import List
import copy

# Variation 1: DFS mark border-connected O first
class Solution_v1:
    def solve(self, board: List[List[str]]) -> None:
        rows,cols=len(board),len(board[0])
        def dfs(r,c):
            if r<0 or r>=rows or c<0 or c>=cols or board[r][c]!="O": return
            board[r][c]="T"
            dfs(r+1,c);dfs(r-1,c);dfs(r,c+1);dfs(r,c-1)
        for r in range(rows):
            for c in [0,cols-1]: dfs(r,c)
        for c in range(cols):
            for r in [0,rows-1]: dfs(r,c)
        for r in range(rows):
            for c in range(cols):
                if board[r][c]=="O": board[r][c]="X"
                elif board[r][c]=="T": board[r][c]="O"

# Variation 2: Union Find - union border O with virtual node
class Solution_v2:
    def solve(self, board: List[List[str]]) -> None:
        if not board: return
        rows,cols=len(board),len(board[0])
        dummy=rows*cols
        parent=list(range(rows*cols+1))
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        def union(a,b): parent[find(a)]=find(b)
        for r in range(rows):
            for c in range(cols):
                if board[r][c]=="O":
                    if r==0 or r==rows-1 or c==0 or c==cols-1: union(r*cols+c,dummy)
                    else:
                        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                            if board[r+dr][c+dc]=="O": union(r*cols+c,(r+dr)*cols+(c+dc))
        for r in range(rows):
            for c in range(cols):
                if board[r][c]=="O" and find(r*cols+c)!=find(dummy): board[r][c]="X"

if __name__ == "__main__":
    board_orig=[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        b=copy.deepcopy(board_orig)
        tracemalloc.start(); t0=time.perf_counter()
        Cls().solve(b)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {b}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
