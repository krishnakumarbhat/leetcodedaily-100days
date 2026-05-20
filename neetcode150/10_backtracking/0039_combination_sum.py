"""LeetCode 39: Combination Sum - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: Backtracking (pick/skip)
class Solution_v1:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        def bt(i, cur, total):
            if total == target: res.append(cur[:]); return
            if i >= len(candidates) or total > target: return
            cur.append(candidates[i]); bt(i, cur, total + candidates[i]); cur.pop()
            bt(i + 1, cur, total)
        bt(0, [], 0); return res

# Variation 2: Sorted + early termination backtracking
class Solution_v2:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort(); res = []
        def bt(i, cur, remaining):
            if remaining == 0: res.append(cur[:]); return
            for j in range(i, len(candidates)):
                if candidates[j] > remaining: break
                cur.append(candidates[j]); bt(j, cur, remaining - candidates[j]); cur.pop()
        bt(0, [], target); return res

if __name__ == "__main__":
    candidates = [2, 3, 6, 7]; target = 7
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().combinationSum(candidates[:], target)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {sorted([sorted(x) for x in r])}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
