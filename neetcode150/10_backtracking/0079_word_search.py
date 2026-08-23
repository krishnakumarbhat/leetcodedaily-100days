"""
=====================================================================
LeetCode 79 : Word Search                                         (Medium)
https://leetcode.com/problems/word-search/
Category   : Backtracking on a grid
---------------------------------------------------------------------
PROBLEM
    Does `word` appear as a path of adjacent cells (up/down/left/
    right), each cell used at most once, in an m×n board?
---------------------------------------------------------------------
INTUITION
    Try every cell as the start; DFS-match the word character by
    character, marking cells visited, unmarking on failure.
---------------------------------------------------------------------
APPROACH 1 · In-place sentinel marking (best)
    Overwrite the matched cell with a sentinel that can never equal a
    letter, restore it after the 4-neighbour recursion.
APPROACH 2 · visited[][] grid
    Same search with an explicit bool matrix.
---------------------------------------------------------------------
DEEP DIVE · The sentinel state machine
    '\0' can never match an input letter, so "used" is encoded in the
    board itself — no allocation, no restore on the success path
    (early return unwinds without restoring, which is safe because we
    already found the answer). Worst case (all cells match the first
    char): O(m·n·3^L).
---------------------------------------------------------------------
TIME COMPLEXITY : O(m·n·3^L) worst.
MEMORY COMPLEXITY: O(L) recursion depth.
=====================================================================
"""


class Solution_1:
    def exist(self, board, word):
        m, n = len(board), len(board[0])

        def dfs(i, j, k):
            if k == len(word):
                return True
            if not (0 <= i < m and 0 <= j < n) or board[i][j] != word[k]:
                return False
            save = board[i][j]
            board[i][j] = "\0"
            found = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or
                     dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
            board[i][j] = save
            return found

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False


class Solution_2:
    def exist(self, board, word):
        m, n = len(board), len(board[0])
        vis = [[False] * n for _ in range(m)]

        def dfs(i, j, k):
            if k == len(word):
                return True
            if not (0 <= i < m and 0 <= j < n) or vis[i][j] or board[i][j] != word[k]:
                return False
            vis[i][j] = True
            found = (dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or
                     dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1))
            vis[i][j] = False
            return found

        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False


if __name__ == "__main__":
    import time, tracemalloc
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    cases = [("ABCCED", True), ("SEE", True), ("ABCB", False)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for w, want in cases:
        r1, r2 = Solution_1().exist([row[:] for row in board], w), Solution_2().exist([row[:] for row in board], w)
        ok &= r1 == r2 == want
        print(f'"{w}" -> A1={r1} A2={r2} (want {want}) {"PASS" if r1 == want and r2 == want else "FAIL"}')
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
