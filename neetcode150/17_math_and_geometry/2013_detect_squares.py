"""LeetCode 2013: Detect Squares - Medium"""
import time, tracemalloc
from collections import defaultdict
from typing import List
# Variation 1: Hash map of points
class DetectSquares_v1:
    def __init__(self):
        self.ptsCount = defaultdict(int)
        self.pts = []
    def add(self, point: List[int]) -> None:
        self.ptsCount[tuple(point)] += 1
        self.pts.append(point)
    def count(self, point: List[int]) -> int:
        res = 0; px, py = point
        for x, y in self.pts:
            if (abs(py - y) != abs(px - x)) or x == px or y == py: continue
            res += self.ptsCount[(x, py)] * self.ptsCount[(px, y)]
        return res
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    obj = DetectSquares_v1()
    obj.add([3,10]); obj.add([11,2]); obj.add([3,2])
    r = obj.count([11,10])
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
