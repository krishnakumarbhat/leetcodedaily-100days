"""LeetCode 213: House Robber II - Medium"""
import time, tracemalloc
from typing import List

def rob_linear(nums):
    prev2,prev1=0,0
    for n in nums: prev2,prev1=prev1,max(prev1,prev2+n)
    return prev1

# Variation 1: Two passes (skip first / skip last)
class Solution_v1:
    def rob(self, nums: List[int]) -> int:
        if len(nums)==1: return nums[0]
        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

if __name__ == "__main__":
    nums=[2,3,2]
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().rob(nums)
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: rob={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
