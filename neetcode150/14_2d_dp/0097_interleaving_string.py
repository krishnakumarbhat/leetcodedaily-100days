"""LeetCode 97: Interleaving String - Medium"""
import time, tracemalloc
# Variation 1: 2D DP
class Solution_v1:
    def isInterleave(self, s1, s2, s3) -> bool:
        m,n=len(s1),len(s2)
        if m+n!=len(s3): return False
        dp=[[False]*(n+1) for _ in range(m+1)]
        dp[0][0]=True
        for i in range(1,m+1): dp[i][0]=dp[i-1][0] and s1[i-1]==s3[i-1]
        for j in range(1,n+1): dp[0][j]=dp[0][j-1] and s2[j-1]==s3[j-1]
        for i in range(1,m+1):
            for j in range(1,n+1):
                dp[i][j]=(dp[i-1][j] and s1[i-1]==s3[i+j-1]) or (dp[i][j-1] and s2[j-1]==s3[i+j-1])
        return dp[m][n]
# Variation 2: BFS
class Solution_v2:
    def isInterleave(self, s1, s2, s3) -> bool:
        from collections import deque
        m,n=len(s1),len(s2)
        if m+n!=len(s3): return False
        q=deque([(0,0)]); seen=set()
        while q:
            i,j=q.popleft()
            if i+j==len(s3): return True
            if (i,j) in seen: continue
            seen.add((i,j))
            if i<m and s1[i]==s3[i+j]: q.append((i+1,j))
            if j<n and s2[j]==s3[i+j]: q.append((i,j+1))
        return False
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().isInterleave("aabcc","dbbca","aadbbcbcac")
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
