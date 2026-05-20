"""LeetCode 1851: Minimum Interval to Include Each Query - Hard"""
import time, tracemalloc
from typing import List
import heapq
class Solution_v1:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort(); q_sorted=sorted(enumerate(queries),key=lambda x:x[1])
        res=[-1]*len(queries); heap=[]; i=0
        for idx,q in q_sorted:
            while i<len(intervals) and intervals[i][0]<=q:
                l,r=intervals[i]; heapq.heappush(heap,(r-l+1,r)); i+=1
            while heap and heap[0][1]<q: heapq.heappop(heap)
            if heap: res[idx]=heap[0][0]
        return res
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().minInterval([[1,4],[2,4],[3,6],[4,4]],[2,3,4,5])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
