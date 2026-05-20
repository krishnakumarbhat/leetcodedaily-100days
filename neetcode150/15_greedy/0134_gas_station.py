"""LeetCode 134: Gas Station - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: One-pass greedy
class Solution_v1:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total=tank=start=0
        for i in range(len(gas)):
            diff=gas[i]-cost[i]; total+=diff; tank+=diff
            if tank<0: start=i+1; tank=0
        return start if total>=0 else -1
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().canCompleteCircuit([1,2,3,4,5],[3,4,5,1,2])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: start={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
