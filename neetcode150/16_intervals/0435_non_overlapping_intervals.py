"""LeetCode 435: Non-overlapping Intervals - Medium"""
import time, tracemalloc
from typing import List
class Solution_v1:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x:x[1]); count=0; end=float("-inf")
        for s,e in intervals:
            if s>=end: end=e
            else: count+=1
        return count
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: erase={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
