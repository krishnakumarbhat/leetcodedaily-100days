"""LeetCode 17: Letter Combinations of a Phone Number - Medium"""
import time, tracemalloc
from typing import List
from itertools import product

PHONE = {"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}

# Variation 1: DFS backtracking
class Solution_v1:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits: return []
        res = []
        def bt(i, cur):
            if i == len(digits): res.append(cur); return
            for c in PHONE[digits[i]]: bt(i + 1, cur + c)
        bt(0, ""); return res

# Variation 2: BFS iterative (expand current combinations)
class Solution_v2:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits: return []
        res = [""]
        for d in digits:
            res = [combo + c for combo in res for c in PHONE[d]]
        return res

# Variation 3: itertools.product
class Solution_v3:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits: return []
        return ["".join(combo) for combo in product(*[PHONE[d] for d in digits])]

if __name__ == "__main__":
    digits = "23"
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().letterCombinations(digits)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {sorted(r)}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
