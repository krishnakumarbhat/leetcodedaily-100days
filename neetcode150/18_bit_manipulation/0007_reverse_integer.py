"""LeetCode 7: Reverse Integer - Medium"""
import time, tracemalloc
import math
# Variation 1: Mod and division math
class Solution_v1:
    def reverse(self, x: int) -> int:
        MIN = -2147483648; MAX = 2147483647
        res = 0
        while x:
            digit = int(math.fmod(x, 10))
            x = int(x / 10)
            if res > MAX // 10 or (res == MAX // 10 and digit >= MAX % 10): return 0
            if res < MIN // 10 or (res == MIN // 10 and digit <= MIN % 10): return 0
            res = (res * 10) + digit
        return res
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().reverse(123)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
