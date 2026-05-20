"""LeetCode 338: Counting Bits - Easy"""
import time, tracemalloc
from typing import List
# Variation 1: DP + Bit Shift
class Solution_v1:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        offset = 1
        for i in range(1, n + 1):
            if offset * 2 == i: offset = i
            dp[i] = 1 + dp[i - offset]
        return dp
# Variation 2: n & (n - 1) DP
class Solution_v2:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1
        return dp
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().countBits(5)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
