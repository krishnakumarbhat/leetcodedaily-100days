"""LeetCode 494: Target Sum - Medium"""
import time, tracemalloc
from typing import List
from collections import defaultdict
# Variation 1: DFS brute force O(2^n)
class Solution_v1:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        def dfs(i, total):
            if i==len(nums): return 1 if total==target else 0
            return dfs(i+1,total+nums[i])+dfs(i+1,total-nums[i])
        return dfs(0,0)
# Variation 2: DP with hashmap
class Solution_v2:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp=defaultdict(int); dp[0]=1
        for n in nums:
            ndp=defaultdict(int)
            for s,cnt in dp.items():
                ndp[s+n]+=cnt; ndp[s-n]+=cnt
            dp=ndp
        return dp[target]
if __name__ == "__main__":
    nums=[1,1,1,1,1]; target=3
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().findTargetSumWays(nums,target)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: ways={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
