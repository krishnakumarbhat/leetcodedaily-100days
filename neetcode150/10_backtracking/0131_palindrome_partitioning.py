"""LeetCode 131: Palindrome Partitioning - Medium"""
import time, tracemalloc
from typing import List

def is_palindrome(s, l, r):
    while l < r:
        if s[l] != s[r]: return False
        l += 1; r -= 1
    return True

# Variation 1: Backtracking with inline palindrome check
class Solution_v1:
    def partition(self, s: str) -> List[List[str]]:
        res = []
        def bt(i, cur):
            if i == len(s): res.append(cur[:]); return
            for j in range(i, len(s)):
                sub = s[i:j+1]
                if sub == sub[::-1]:
                    cur.append(sub); bt(j + 1, cur); cur.pop()
        bt(0, []); return res

# Variation 2: DP precompute palindrome + backtracking
class Solution_v2:
    def partition(self, s: str) -> List[List[str]]:
        n = len(s)
        dp = [[False]*n for _ in range(n)]
        for i in range(n): dp[i][i] = True
        for length in range(2, n+1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    dp[i][j] = (length == 2) or dp[i+1][j-1]
        res = []
        def bt(i, cur):
            if i == n: res.append(cur[:]); return
            for j in range(i, n):
                if dp[i][j]:
                    cur.append(s[i:j+1]); bt(j+1, cur); cur.pop()
        bt(0, []); return res

if __name__ == "__main__":
    s = "aab"
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().partition(s)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
