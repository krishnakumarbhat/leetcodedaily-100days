"""LeetCode 678: Valid Parenthesis String - Medium"""
import time, tracemalloc
# Variation 1: Greedy count low/high
class Solution_v1:
    def checkValidString(self, s: str) -> bool:
        lo=hi=0
        for c in s:
            if c=="(": lo+=1; hi+=1
            elif c==")": lo-=1; hi-=1
            else: lo-=1; hi+=1
            if hi<0: return False
            lo=max(lo,0)
        return lo==0
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().checkValidString("(*)")
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
