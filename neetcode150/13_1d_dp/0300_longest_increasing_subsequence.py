"""LeetCode 300: LIS - Medium"""
import time, tracemalloc
import bisect
from typing import List

# Variation 1: DP O(n^2)
class Solution_v1:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp=[1]*len(nums)
        for i in range(len(nums)):
            for j in range(i): 
                if nums[j]<nums[i]: dp[i]=max(dp[i],dp[j]+1)
        return max(dp)

# Variation 2: Patience sort (binary search) O(n log n)
class Solution_v2:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails=[]
        for n in nums:
            pos=bisect.bisect_left(tails,n)
            if pos==len(tails): tails.append(n)
            else: tails[pos]=n
        return len(tails)

if __name__ == "__main__":
    nums=[10,9,2,5,3,7,101,18]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().lengthOfLIS(nums)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: lis={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
