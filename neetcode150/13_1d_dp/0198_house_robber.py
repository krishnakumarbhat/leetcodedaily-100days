"""LeetCode 198: House Robber - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: DP two-variable
class Solution_v1:
    def rob(self, nums: List[int]) -> int:
        prev2,prev1=0,0
        for n in nums: prev2,prev1=prev1,max(prev1,prev2+n)
        return prev1

# Variation 2: DP array
class Solution_v2:
    def rob(self, nums: List[int]) -> int:
        if not nums: return 0
        n=len(nums); dp=[0]*(n+1); dp[1]=nums[0]
        for i in range(2,n+1): dp[i]=max(dp[i-1],dp[i-2]+nums[i-1])
        return dp[n]

# Variation 3: Recursion + memo
class Solution_v3:
    def rob(self, nums: List[int]) -> int:
        from functools import lru_cache
        @lru_cache(None)
        def dp(i): return 0 if i>=len(nums) else max(dp(i+1),nums[i]+dp(i+2))
        return dp(0)

if __name__ == "__main__":
    nums=[2,7,9,3,1]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2,Solution_v3],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().rob(nums[:])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: rob={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
