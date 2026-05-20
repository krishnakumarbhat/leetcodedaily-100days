"""LeetCode 139: Word Break - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: DP array
class Solution_v1:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words=set(wordDict); n=len(s); dp=[False]*(n+1); dp[0]=True
        for i in range(1,n+1):
            for j in range(i):
                if dp[j] and s[j:i] in words: dp[i]=True; break
        return dp[n]

# Variation 2: BFS
class Solution_v2:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        from collections import deque
        words=set(wordDict); q=deque([0]); visited=set()
        while q:
            start=q.popleft()
            if start==len(s): return True
            if start in visited: continue
            visited.add(start)
            for end in range(start+1,len(s)+1):
                if s[start:end] in words: q.append(end)
        return False

if __name__ == "__main__":
    s="leetcode"; wd=["leet","code"]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().wordBreak(s,wd)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: can_break={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
