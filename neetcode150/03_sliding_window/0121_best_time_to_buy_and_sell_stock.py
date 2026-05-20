"""
LeetCode 121: Best Time to Buy and Sell Stock
Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
Difficulty: Easy
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Brute Force =============
# Algorithm: Brute iterate all starting indices (buy) and ending indices (sell).
# Time Complexity: O(n^2)   Space Complexity: O(1)
class Solution_v1:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                max_profit = max(max_profit, prices[j] - prices[i])
        return max_profit

# ============= Variation 2: One Pass (Kadane's style) =============
# Algorithm: Cache the minimum price linearly reading over numbers. Sell price 
# assumes buying strictly from recorded bounds.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v2:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        max_profit = 0
        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)
        return max_profit

if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4, 8, 2, 9, 1]
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "One Pass"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().maxProfit(prices[:])
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 772 bytes and time = 48.14 µs
# var2 mem = 736 bytes and time = 18.81 µs
