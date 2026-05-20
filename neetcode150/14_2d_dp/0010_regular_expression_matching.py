"""LeetCode 10: Regular Expression Matching - Hard"""
import time, tracemalloc
# Variation 1: 2D DP
class Solution_v1:
    def isMatch(self, s, p) -> bool:
        m,n=len(s),len(p)
        dp=[[False]*(n+1) for _ in range(m+1)]
        dp[0][0]=True
        for j in range(1,n+1):
            if p[j-1]=="*": dp[0][j]=dp[0][j-2]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if p[j-1]=="*":
                    dp[i][j]=dp[i][j-2]  # use 0 times
                    if p[j-2]=="." or p[j-2]==s[i-1]:
                        dp[i][j]=dp[i][j] or dp[i-1][j]
                elif p[j-1]=="." or p[j-1]==s[i-1]:
                    dp[i][j]=dp[i-1][j-1]
        return dp[m][n]
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().isMatch("aab","c*a*b")
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: match={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
