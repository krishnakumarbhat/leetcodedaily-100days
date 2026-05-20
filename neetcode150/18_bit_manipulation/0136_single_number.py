"""LeetCode 136: Single Number - Easy"""
import time, tracemalloc
from typing import List
# Variation 1: XOR
class Solution_v1:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for n in nums: res = n ^ res
        return res
# Variation 2: Hash Set
class Solution_v2:
    def singleNumber(self, nums: List[int]) -> int:
        return 2*sum(set(nums)) - sum(nums)
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().singleNumber([4,1,2,1,2])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
