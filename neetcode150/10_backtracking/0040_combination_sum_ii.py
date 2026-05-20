"""LeetCode 40: Combination Sum II - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: Sort + skip duplicates at same level
class Solution_v1:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort(); res = []
        def bt(i, cur, remaining):
            if remaining == 0: res.append(cur[:]); return
            for j in range(i, len(candidates)):
                if remaining - candidates[j] < 0: break
                if j > i and candidates[j] == candidates[j - 1]: continue
                cur.append(candidates[j]); bt(j + 1, cur, remaining - candidates[j]); cur.pop()
        bt(0, [], target); return res

# Variation 2: Counter-based to handle duplicates
class Solution_v2:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        from collections import Counter
        count = sorted(Counter(candidates).items()); res = []
        def bt(i, cur, remaining):
            if remaining == 0: res.append(cur[:]); return
            if i == len(count): return
            num, cnt = count[i]
            bt(i + 1, cur, remaining)  # skip this num entirely
            for k in range(1, cnt + 1):
                if num * k > remaining: break
                cur.extend([num] * k); bt(i + 1, cur, remaining - num * k); del cur[-k:]
        bt(0, [], target); return res

if __name__ == "__main__":
    candidates = [10, 1, 2, 7, 6, 1, 5]; target = 8
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().combinationSum2(candidates[:], target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {sorted([sorted(x) for x in r])}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
