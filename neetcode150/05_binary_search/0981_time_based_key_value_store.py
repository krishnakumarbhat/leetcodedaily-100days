"""
LeetCode 981: Time Based Key-Value Store
Link: https://leetcode.com/problems/time-based-key-value-store/
Difficulty: Medium
"""
import time, tracemalloc
from collections import defaultdict
import bisect

# ============= Variation 1: Binary Search =============
# Algorithm: Store a list of `(timestamp, value)` pairs for each key. 
# Use binary search on the timestamps to find the largest timestamp <= target.
# Time Complexity: O(log n) per get   Space Complexity: O(n)
class TimeMap_v1:
    def __init__(self):
        self.store = defaultdict(list)
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))
    def get(self, key: str, timestamp: int) -> str:
        vals = self.store[key]
        l, r, result = 0, len(vals) - 1, ""
        while l <= r:
            mid = (l + r) // 2
            if vals[mid][0] <= timestamp:
                result = vals[mid][1]; l = mid + 1
            else: r = mid - 1
        return result

if __name__ == "__main__":
    tracemalloc.start(); t0 = time.perf_counter()
    tm = TimeMap_v1()
    tm.set("foo", "bar", 1); tm.set("foo", "bar2", 4)
    r1 = tm.get("foo", 1); r2 = tm.get("foo", 3); r3 = tm.get("foo", 5)
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (BS): get(1)={r1}, get(3)={r2}, get(5)={r3}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 712 bytes and time = 37.56 µs
