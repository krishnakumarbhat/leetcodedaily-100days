"""LeetCode 763: Partition Labels - Medium"""
import time, tracemalloc
# Variation 1: Last occurrence greedy
class Solution_v1:
    def partitionLabels(self, s: str):
        last={c:i for i,c in enumerate(s)}
        start=end=0; res=[]
        for i,c in enumerate(s):
            end=max(end,last[c])
            if i==end: res.append(end-start+1); start=i+1
        return res
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    r=Solution_v1().partitionLabels("ababcbacadefegdehijhklij")
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
