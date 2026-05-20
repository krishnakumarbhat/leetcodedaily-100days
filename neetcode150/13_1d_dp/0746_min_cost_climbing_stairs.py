"""LeetCode 746: Min Cost Climbing Stairs - Easy"""
import time, tracemalloc
from typing import List

# Variation 1: DP in-place
class Solution_v1:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n=len(cost)
        for i in range(2,n): cost[i]+=min(cost[i-1],cost[i-2])
        return min(cost[-1],cost[-2])

# Variation 2: DP with extra space
class Solution_v2:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n=len(cost); dp=[0]*(n+1)
        for i in range(2,n+1): dp[i]=min(dp[i-1]+cost[i-1],dp[i-2]+cost[i-2])
        return dp[n]

if __name__ == "__main__":
    import copy; cost=[10,15,20]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        c=copy.deepcopy(cost)
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().minCostClimbingStairs(c)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: cost={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
