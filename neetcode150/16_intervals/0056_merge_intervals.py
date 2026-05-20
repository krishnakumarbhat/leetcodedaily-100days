"""LeetCode 56: Merge Intervals - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: Sort and merge
class Solution_v1:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(); res=[intervals[0]]
        for s,e in intervals[1:]:
            if s<=res[-1][1]: res[-1][1]=max(res[-1][1],e)
            else: res.append([s,e])
        return res
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().merge([[1,3],[2,6],[8,10],[15,18]])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
