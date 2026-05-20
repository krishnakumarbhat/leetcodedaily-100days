"""LeetCode 647: Palindromic Substrings - Medium"""
import time, tracemalloc

# Variation 1: Expand around center
class Solution_v1:
    def countSubstrings(self, s: str) -> int:
        count=0
        def expand(l,r):
            nonlocal count
            while l>=0 and r<len(s) and s[l]==s[r]: count+=1; l-=1; r+=1
        for i in range(len(s)): expand(i,i); expand(i,i+1)
        return count

# Variation 2: DP table
class Solution_v2:
    def countSubstrings(self, s: str) -> int:
        n=len(s); dp=[[False]*n for _ in range(n)]; count=0
        for i in range(n-1,-1,-1):
            for j in range(i,n):
                if s[i]==s[j] and (j-i<=2 or dp[i+1][j-1]):
                    dp[i][j]=True; count+=1
        return count

if __name__ == "__main__":
    s="aaa"
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().countSubstrings(s)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: count={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
