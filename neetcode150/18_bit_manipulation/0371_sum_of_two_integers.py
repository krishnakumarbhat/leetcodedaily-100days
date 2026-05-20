"""LeetCode 371: Sum of Two Integers - Medium"""
import time, tracemalloc
# Variation 1: Python specific bit-manipulation with 32-bit mask
class Solution_v1:
    def getSum(self, a: int, b: int) -> int:
        mask = 0xFFFFFFFF
        while b != 0:
            tmp = (a & b) << 1
            a = (a ^ b) & mask
            b = tmp & mask
        if a > 0x7FFFFFFF: return ~(a ^ mask)
        return a
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().getSum(1, 2)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
