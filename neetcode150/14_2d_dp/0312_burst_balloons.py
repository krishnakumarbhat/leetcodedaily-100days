"""LeetCode 312: Burst Balloons - Hard"""
import time, tracemalloc
from typing import List
# Variation 1: Interval DP
class Solution_v1:
    def maxCoins(self, nums: List[int]) -> int:
        nums=[1]+nums+[1]; n=len(nums)
        dp=[[0]*n for _ in range(n)]
        for length in range(2,n):
            for l in range(0,n-length):
                r=l+length
                for k in range(l+1,r):
                    dp[l][r]=max(dp[l][r],nums[l]*nums[k]*nums[r]+dp[l][k]+dp[k][r])
        return dp[0][n-1]
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().maxCoins([3,1,5,8])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: coins={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
