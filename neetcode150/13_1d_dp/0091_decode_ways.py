"""LeetCode 91: Decode Ways - Medium"""
import time, tracemalloc

# Variation 1: DP iterative
class Solution_v1:
    def numDecodings(self, s: str) -> int:
        n=len(s); dp=[0]*(n+1); dp[0]=1; dp[1]=0 if s[0]=="0" else 1
        for i in range(2,n+1):
            if s[i-1]!="0": dp[i]+=dp[i-1]
            two=int(s[i-2:i])
            if 10<=two<=26: dp[i]+=dp[i-2]
        return dp[n]

# Variation 2: Recursion + memo
class Solution_v2:
    def numDecodings(self, s: str) -> int:
        from functools import lru_cache
        @lru_cache(None)
        def dp(i):
            if i==len(s): return 1
            if s[i]=="0": return 0
            res=dp(i+1)
            if i+1<len(s) and int(s[i:i+2])<=26: res+=dp(i+2)
            return res
        return dp(0)

if __name__ == "__main__":
    s="226"
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().numDecodings(s)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: ways={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
