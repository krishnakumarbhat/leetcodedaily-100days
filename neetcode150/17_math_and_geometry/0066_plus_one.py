"""LeetCode 66: Plus One - Easy"""
import time, tracemalloc
from typing import List
# Variation 1: Reverse array carry logic
class Solution_v1:
    def plusOne(self, digits: List[int]) -> List[int]:
        digits = digits[::-1]
        one, i = 1, 0
        while one:
            if i < len(digits):
                if digits[i] == 9: digits[i] = 0
                else: digits[i] += 1; one = 0
            else:
                digits.append(1); one = 0
            i += 1
        return digits[::-1]
# Variation 2: Backwards traversal
class Solution_v2:
    def plusOne(self, digits: List[int]) -> List[int]:
        for i in range(len(digits)-1, -1, -1):
            if digits[i] == 9: digits[i] = 0
            else: digits[i] += 1; return digits
        return [1] + digits
if __name__ == "__main__":
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r = Cls().plusOne([1,2,3])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
