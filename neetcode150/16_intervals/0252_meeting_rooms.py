"""LeetCode 252: Meeting Rooms - Easy"""
import time, tracemalloc
from typing import List
class Solution_v1:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort()
        for i in range(1,len(intervals)):
            if intervals[i][0]<intervals[i-1][1]: return False
        return True
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().canAttendMeetings([[0,30],[5,10],[15,20]])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
