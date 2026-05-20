"""LeetCode 45: Jump Game II - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: Greedy (BFS levels)
class Solution_v1:
    def jump(self, nums: List[int]) -> int:
        jumps=cur_end=far=0
        for i in range(len(nums)-1):
            far=max(far,i+nums[i])
            if i==cur_end: jumps+=1; cur_end=far
        return jumps
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().jump([2,3,1,1,4])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: jumps={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
