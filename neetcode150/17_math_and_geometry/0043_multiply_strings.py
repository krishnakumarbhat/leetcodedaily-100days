"""LeetCode 43: Multiply Strings - Medium"""
import time, tracemalloc
# Variation 1: Digits array simulation
class Solution_v1:
    def multiply(self, num1: str, num2: str) -> str:
        if "0" in [num1, num2]: return "0"
        res = [0] * (len(num1) + len(num2))
        num1, num2 = num1[::-1], num2[::-1]
        for i1 in range(len(num1)):
            for i2 in range(len(num2)):
                digit = int(num1[i1]) * int(num2[i2])
                res[i1 + i2] += digit
                res[i1 + i2 + 1] += res[i1 + i2] // 10
                res[i1 + i2] = res[i1 + i2] % 10
        res, beg = res[::-1], 0
        while beg < len(res) and res[beg] == 0: beg += 1
        return "".join(map(str, res[beg:]))
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().multiply("123", "456")
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: res={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
