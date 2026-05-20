"""LeetCode 322: Coin Change - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: BFS (level = amount, nodes = coins) O(amount*len(coins))
class Solution_v1:
    def coinChange(self, coins: List[int], amount: int) -> int:
        from collections import deque
        if amount==0: return 0
        q=deque([(0,0)]); visited={0}
        while q:
            cur,steps=q.popleft()
            for c in coins:
                nxt=cur+c
                if nxt==amount: return steps+1
                if nxt<amount and nxt not in visited: visited.add(nxt); q.append((nxt,steps+1))
        return -1

# Variation 2: DP bottom-up
class Solution_v2:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp=[float("inf")]*(amount+1); dp[0]=0
        for a in range(1,amount+1):
            for c in coins:
                if c<=a: dp[a]=min(dp[a],dp[a-c]+1)
        return dp[amount] if dp[amount]!=float("inf") else -1

# Variation 3: DFS + memo (top-down)
class Solution_v3:
    def coinChange(self, coins: List[int], amount: int) -> int:
        from functools import lru_cache
        @lru_cache(None)
        def dp(rem):
            if rem<0: return float("inf")
            if rem==0: return 0
            return 1+min(dp(rem-c) for c in coins)
        r=dp(amount)
        return r if r!=float("inf") else -1

if __name__ == "__main__":
    coins=[1,5,11]; amount=15
    for Vi,Cls in enumerate([Solution_v1,Solution_v2,Solution_v3],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().coinChange(coins,amount)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: coins={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
