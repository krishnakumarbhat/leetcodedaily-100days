"""LeetCode 55: Jump Game - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: Greedy max reach
class Solution_v1:
    def canJump(self, nums: List[int]) -> bool:
        reach=0
        for i,n in enumerate(nums):
            if i>reach: return False
            reach=max(reach,i+n)
        return True
# Variation 2: DP from right
class Solution_v2:
    def canJump(self, nums: List[int]) -> bool:
        goal=len(nums)-1
        for i in range(len(nums)-2,-1,-1):
            if i+nums[i]>=goal: goal=i
        return goal==0
if __name__ == "__main__":
    nums=[2,3,1,1,4]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().canJump(nums[:])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: can={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
