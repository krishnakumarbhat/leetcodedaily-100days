"""LeetCode 190: Reverse Bits - Easy"""
import time, tracemalloc
# Variation 1: Bit by bit
class Solution_v1:
    def reverseBits(self, n: int) -> int:
        res = 0
        for i in range(32):
            bit = (n >> i) & 1
            res = res | (bit << (31 - i))
        return res
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().reverseBits(43261596)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
