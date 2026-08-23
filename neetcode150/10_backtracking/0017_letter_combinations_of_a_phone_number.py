"""
=====================================================================
LeetCode 17 : Letter Combinations of a Phone Number               (Medium)
https://leetcode.com/problems/letter-combinations-of-a-phone-number/
Category   : Backtracking
---------------------------------------------------------------------
PROBLEM
    Every letter combination the phone keypad digits could stand for.
---------------------------------------------------------------------
INTUITION
    The output is a Cartesian product over per-digit letter sets —
    backtracking enumerates it with a single shared prefix.
---------------------------------------------------------------------
APPROACH 1 · Backtracking (best)
    dfs(d): d == len(digits) → record; else loop the digit's letters,
    append, recurse(d+1), pop.
APPROACH 2 · Iterative product
    Start [""]; per digit extend every prefix by every letter.
---------------------------------------------------------------------
DEEP DIVE · Why empty input must return []
    [""] seed would yield [""] for digits="" — an invalid combination
    (digits produced no letters). Both idioms special-case it.
    Answer size = Π letters(digit); "999" → 4^3 = 64.
---------------------------------------------------------------------
TIME COMPLEXITY : O(4^n) worst case (all 9s).
MEMORY COMPLEXITY: O(n) DFS depth.
=====================================================================
"""
KEYPAD = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
          "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


class Solution_1:
    def letterCombinations(self, digits):
        if not digits:
            return []
        out, cur = [], []

        def dfs(d):
            if d == len(digits):
                out.append("".join(cur))
                return
            for ch in KEYPAD[digits[d]]:
                cur.append(ch)
                dfs(d + 1)
                cur.pop()

        dfs(0)
        return out


class Solution_2:
    def letterCombinations(self, digits):
        if not digits:
            return []
        out = [""]
        for d in digits:
            out = [p + ch for p in out for ch in KEYPAD[d]]
        return out


if __name__ == "__main__":
    import time, tracemalloc
    cases = [("23", 9), ("", 0), ("2", 3), ("999", 64)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for d, want in cases:
        r1, r2 = len(Solution_1().letterCombinations(d)), len(Solution_2().letterCombinations(d))
        ok &= r1 == r2 == want
        print(f'"{d}" -> A1={r1} A2={r2} (want {want}) {"PASS" if r1 == want and r2 == want else "FAIL"}')
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
