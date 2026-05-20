"""LeetCode 309: Stock with Cooldown - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: State machine DP (hold, sold, rest)
class Solution_v1:
    def maxProfit(self, prices: List[int]) -> int:
        hold,sold,rest=float("-inf"),0,0
        for p in prices:
            hold,sold,rest=max(hold,rest-p),hold+p,max(rest,sold)
        return max(sold,rest)
# Variation 2: Recursive memo
class Solution_v2:
    def maxProfit(self, prices: List[int]) -> int:
        from functools import lru_cache
        @lru_cache(None)
        def dp(i,holding):
            if i>=len(prices): return 0
            if holding:
                return max(dp(i+1,True), prices[i]+dp(i+2,False))
            return max(dp(i+1,False), dp(i+1,True)-prices[i])
        return dp(0,False)
if __name__ == "__main__":
    prices=[1,2,3,0,2]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().maxProfit(prices)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: profit={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
