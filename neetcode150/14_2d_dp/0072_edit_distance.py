"""LeetCode 72: Edit Distance - Medium"""
import time, tracemalloc
# Variation 1: 2D DP
class Solution_v1:
    def minDistance(self, w1, w2) -> int:
        m,n=len(w1),len(w2)
        dp=[[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0]=i
        for j in range(n+1): dp[0][j]=j
        for i in range(1,m+1):
            for j in range(1,n+1):
                if w1[i-1]==w2[j-1]: dp[i][j]=dp[i-1][j-1]
                else: dp[i][j]=1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])
        return dp[m][n]
# Variation 2: 1D rolling
class Solution_v2:
    def minDistance(self, w1, w2) -> int:
        m,n=len(w1),len(w2)
        dp=list(range(n+1))
        for i in range(1,m+1):
            prev=dp[0]; dp[0]=i
            for j in range(1,n+1):
                temp=dp[j]
                if w1[i-1]==w2[j-1]: dp[j]=prev
                else: dp[j]=1+min(dp[j],dp[j-1],prev)
                prev=temp
        return dp[n]
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().minDistance("horse","ros")
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: dist={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
