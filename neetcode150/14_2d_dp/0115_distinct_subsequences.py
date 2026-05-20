"""LeetCode 115: Distinct Subsequences - Hard"""
import time, tracemalloc
# Variation 1: 2D DP
class Solution_v1:
    def numDistinct(self, s, t) -> int:
        m,n=len(s),len(t)
        dp=[[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0]=1
        for i in range(1,m+1):
            for j in range(1,n+1):
                dp[i][j]=dp[i-1][j]
                if s[i-1]==t[j-1]: dp[i][j]+=dp[i-1][j-1]
        return dp[m][n]
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().numDistinct("rabbbit","rabbit")
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
