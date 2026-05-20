"""LeetCode 62: Unique Paths - Medium"""
import time, tracemalloc
# Variation 1: 2D DP
class Solution_v1:
    def uniquePaths(self, m, n):
        dp=[[1]*n for _ in range(m)]
        for r in range(1,m):
            for c in range(1,n): dp[r][c]=dp[r-1][c]+dp[r][c-1]
        return dp[m-1][n-1]
# Variation 2: 1D DP
class Solution_v2:
    def uniquePaths(self, m, n):
        dp=[1]*n
        for _ in range(1,m):
            for c in range(1,n): dp[c]+=dp[c-1]
        return dp[n-1]
# Variation 3: Math C(m+n-2, m-1)
class Solution_v3:
    def uniquePaths(self, m, n):
        from math import comb
        return comb(m+n-2, m-1)
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2,Solution_v3],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().uniquePaths(3,7)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: paths={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
