"""LeetCode 518: Coin Change II - Medium"""
import time, tracemalloc
from typing import List
# Variation 1: 1D DP (unbounded knapsack)
class Solution_v1:
    def change(self, amount: int, coins: List[int]) -> int:
        dp=[0]*(amount+1); dp[0]=1
        for c in coins:
            for a in range(c,amount+1): dp[a]+=dp[a-c]
        return dp[amount]
# Variation 2: 2D DP
class Solution_v2:
    def change(self, amount: int, coins: List[int]) -> int:
        m=len(coins); dp=[[0]*(amount+1) for _ in range(m+1)]
        for i in range(m+1): dp[i][0]=1
        for i in range(1,m+1):
            for a in range(amount+1):
                dp[i][a]=dp[i-1][a]
                if a>=coins[i-1]: dp[i][a]+=dp[i][a-coins[i-1]]
        return dp[m][amount]
if __name__ == "__main__":
    coins=[1,2,5]; amount=5
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().change(amount,coins)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: ways={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
