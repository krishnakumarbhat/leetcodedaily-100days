"""LeetCode 416: Partition Equal Subset Sum - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: DP bitset / set of achievable sums
class Solution_v1:
    def canPartition(self, nums: List[int]) -> bool:
        total=sum(nums)
        if total%2: return False
        target=total//2; dp={0}
        for n in nums:
            dp={x+n for x in dp}|dp
        return target in dp

# Variation 2: DP boolean array
class Solution_v2:
    def canPartition(self, nums: List[int]) -> bool:
        total=sum(nums)
        if total%2: return False
        target=total//2; dp=[False]*(target+1); dp[0]=True
        for n in nums:
            for j in range(target,n-1,-1):
                dp[j]=dp[j] or dp[j-n]
        return dp[target]

if __name__ == "__main__":
    nums=[1,5,11,5]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().canPartition(nums)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: can_partition={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
