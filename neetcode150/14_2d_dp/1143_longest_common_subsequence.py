"""LeetCode 1143: Longest Common Subsequence - Medium"""
import time, tracemalloc
# Variation 1: 2D DP
class Solution_v1:
    def longestCommonSubsequence(self, t1, t2):
        m,n=len(t1),len(t2)
        dp=[[0]*(n+1) for _ in range(m+1)]
        for i in range(1,m+1):
            for j in range(1,n+1):
                if t1[i-1]==t2[j-1]: dp[i][j]=1+dp[i-1][j-1]
                else: dp[i][j]=max(dp[i-1][j],dp[i][j-1])
        return dp[m][n]
# Variation 2: 1D rolling array
class Solution_v2:
    def longestCommonSubsequence(self, t1, t2):
        m,n=len(t1),len(t2)
        prev,cur=[0]*(n+1),[0]*(n+1)
        for i in range(1,m+1):
            for j in range(1,n+1):
                if t1[i-1]==t2[j-1]: cur[j]=1+prev[j-1]
                else: cur[j]=max(prev[j],cur[j-1])
            prev,cur=cur,[0]*(n+1)
        return prev[n]
if __name__ == "__main__":
    a,b="abcde","ace"
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().longestCommonSubsequence(a,b)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: lcs={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
