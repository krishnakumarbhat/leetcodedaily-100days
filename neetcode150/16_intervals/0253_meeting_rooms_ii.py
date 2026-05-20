"""LeetCode 253: Meeting Rooms II - Medium"""
import time, tracemalloc
from typing import List
import heapq
# Variation 1: Min-heap
class Solution_v1:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        intervals.sort(); heap=[]
        for s,e in intervals:
            if heap and heap[0]<=s: heapq.heapreplace(heap,e)
            else: heapq.heappush(heap,e)
        return len(heap)
# Variation 2: Line sweep
class Solution_v2:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        events=[]
        for s,e in intervals: events+=[(s,1),(e,-1)]
        events.sort(); cur=mx=0
        for _,d in events: cur+=d; mx=max(mx,cur)
        return mx
if __name__ == "__main__":
    iv=[[0,30],[5,10],[15,20]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().minMeetingRooms(iv[:])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: rooms={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
