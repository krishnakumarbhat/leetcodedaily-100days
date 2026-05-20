"""
LeetCode 22: Generate Parentheses
Link: https://leetcode.com/problems/generate-parentheses/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Backtracking =============
# Algorithm: Recursively build the string using available open and close counts. 
# Keep `open_c < n` and `close_c < open_c` to maintain validity.
# Time Complexity: O(4^n/sqrt(n))   Space Complexity: O(n)
class Solution_v1:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        def backtrack(s, open_c, close_c):
            if len(s) == 2 * n:
                result.append(s); return
            if open_c < n: backtrack(s + '(', open_c + 1, close_c)
            if close_c < open_c: backtrack(s + ')', open_c, close_c + 1)
        backtrack('', 0, 0)
        return result

# ============= Variation 2: Iterative (BFS) =============
# Algorithm: Use a queue to store intermediate strings and their bracket counts. 
# Level-by-level generation until string length hits `2n`.
# Time Complexity: O(4^n/sqrt(n))   Space Complexity: O(4^n/sqrt(n))
class Solution_v2:
    def generateParenthesis(self, n: int) -> List[str]:
        from collections import deque
        queue = deque([('', 0, 0)])
        result = []
        while queue:
            s, o, c = queue.popleft()
            if len(s) == 2 * n: result.append(s); continue
            if o < n: queue.append((s + '(', o + 1, c))
            if c < o: queue.append((s + ')', o, c + 1))
        return result

if __name__ == "__main__":
    n = 3
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Backtracking", "BFS"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().generateParenthesis(n)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): count={len(result)}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 4557 bytes and time = 55.53 µs
# var2 mem = 1499 bytes and time = 58.01 µs
