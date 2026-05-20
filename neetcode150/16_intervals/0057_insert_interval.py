"""LeetCode 57: Insert Interval - Medium"""
import time, tracemalloc
from typing import List
class Solution_v1:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        res=[]; i=0; n=len(intervals)
        while i<n and intervals[i][1]<newInterval[0]: res.append(intervals[i]); i+=1
        while i<n and intervals[i][0]<=newInterval[1]: newInterval[0]=min(newInterval[0],intervals[i][0]); newInterval[1]=max(newInterval[1],intervals[i][1]); i+=1
        res.append(newInterval)
        return res+intervals[i:]
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().insert([[1,3],[6,9]],[2,5])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
