"""LeetCode 50: Pow(x, n) - Medium"""
import time, tracemalloc
# Variation 1: Fast exponentiation Recursive
class Solution_v1:
    def myPow(self, x: float, n: int) -> float:
        def helper(x, n):
            if x == 0: return 0
            if n == 0: return 1
            res = helper(x * x, n // 2)
            return x * res if n % 2 else res
        res = helper(x, abs(n))
        return res if n >= 0 else 1 / res
# Variation 2: Fast exponentiation Iterative
class Solution_v2:
    def myPow(self, x: float, n: int) -> float:
        if n < 0: x = 1 / x; n = -n
        res = 1
        while n:
            if n % 2: res *= x
            x *= x; n //= 2
        return res
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().myPow(2.0, 10)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
