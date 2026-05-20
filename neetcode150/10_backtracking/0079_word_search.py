"""LeetCode 79: Word Search - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: DFS backtracking (mark visited by modifying board)
class Solution_v1:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        def dfs(r, c, i):
            if i == len(word): return True
            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[i]: return False
            tmp = board[r][c]; board[r][c] = '#'
            found = (dfs(r+1,c,i+1) or dfs(r-1,c,i+1) or dfs(r,c+1,i+1) or dfs(r,c-1,i+1))
            board[r][c] = tmp
            return found
        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

# Variation 2: DFS with separate visited set
class Solution_v2:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        visited = set()
        def dfs(r, c, i):
            if i == len(word): return True
            if r < 0 or r >= rows or c < 0 or c >= cols or (r,c) in visited or board[r][c] != word[i]: return False
            visited.add((r, c))
            result = (dfs(r+1,c,i+1) or dfs(r-1,c,i+1) or dfs(r,c+1,i+1) or dfs(r,c-1,i+1))
            visited.remove((r, c))
            return result
        return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

if __name__ == "__main__":
    import copy
    board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
    word = "ABCCED"
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        b = copy.deepcopy(board)
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().exist(b, word)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: found={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
