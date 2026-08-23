"""
=====================================================================
LeetCode 201 : Bitwise AND of Numbers Range                       (Medium)
https://leetcode.com/problems/bitwise-and-of-numbers-range/
Category   : Math / bit manipulation
---------------------------------------------------------------------
PROBLEM
    Bitwise AND of every integer in [left, right] inclusive.
---------------------------------------------------------------------
INTUITION
    A result bit is 1 only if ALL numbers in the range have it —
    i.e. it lies in the common PREFIX of left and right. Bits past
    the first difference flip inside the range and die.
---------------------------------------------------------------------
APPROACH 1 · Clear the lowest set bit (best)
    while left < right: right &= right - 1. Converges to the common
    prefix.
APPROACH 2 · Shift both until equal, shift back
    Shift left/right rightwards until they match; the prefix shifted
    back left is the answer.
---------------------------------------------------------------------
DEEP DIVE · Why the prefix survives
    Where left and right first differ, the range spans the carry
    boundary (e.g. 5=101 to 7=111: the middle bit flips) — so that
    bit and everything below is 0 in the AND. Only bits where both
    endpoints (hence every number) agree stay 1. right&(right-1)
    removes the lowest set bit; iterating until right ≤ left lands
    exactly on the shared prefix.
---------------------------------------------------------------------
TIME COMPLEXITY : O(1) — at most 31 iterations.
MEMORY COMPLEXITY: O(1)
=====================================================================
"""


class Solution_1:
    def rangeBitwiseAnd(self, left, right):
        while left < right:
            right &= right - 1
        return right


class Solution_2:
    def rangeBitwiseAnd(self, left, right):
        shift = 0
        while left != right:
            left >>= 1
            right >>= 1
            shift += 1
        return left << shift


if __name__ == "__main__":
    import time, tracemalloc
    cases = [(5, 7, 4), (0, 0, 0), (1, 2147483647, 0), (1073741824, 2147483646, 1073741824)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for l, r, want in cases:
        r1, r2 = Solution_1().rangeBitwiseAnd(l, r), Solution_2().rangeBitwiseAnd(l, r)
        ok &= r1 == r2 == want
        print(f"[{l},{r}] -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
