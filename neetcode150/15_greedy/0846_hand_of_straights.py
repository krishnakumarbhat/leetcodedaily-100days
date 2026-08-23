"""
=====================================================================
LeetCode 846 : Hand of Straights                                  (Medium)
https://leetcode.com/problems/hand-of-straights/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Can the cards be split into groups of `groupSize` consecutive
    values, each card used once?
---------------------------------------------------------------------
INTUITION
    The smallest remaining card must START a run (nothing smaller
    remains) — the choice is forced, which is what makes the greedy
    correct.
---------------------------------------------------------------------
APPROACH 1 · Sorted counter + greedy runs (best)
    Count cards; repeatedly take the smallest value v and consume
    v..v+groupSize-1; any gap fails.
APPROACH 2 · Sort + pointer scan
    Sort, walk runs skipping already-used cards.
---------------------------------------------------------------------
DEEP DIVE · Forced decisions = provably optimal
    Smallest remaining x can't be mid-run (x-1 consumed or absent),
    so it must open a run, and that run is fully determined. No
    branch to choose, no suboptimal alternative — greedy is optimal
    by construction. Counter dict keys are sorted on demand, making
    "smallest remaining" O(log n) amortized.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n log n)
MEMORY COMPLEXITY: O(n)
=====================================================================
"""
from collections import Counter


class Solution_1:
    def isNStraightHand(self, hand, groupSize):
        if len(hand) % groupSize:
            return False
        cnt = Counter(hand)
        for first in sorted(cnt):
            if cnt[first] == 0:
                continue
            need = cnt[first]
            for v in range(first, first + groupSize):
                if cnt[v] < need:
                    return False
                cnt[v] -= need
        return True


class Solution_2:
    def isNStraightHand(self, hand, groupSize):
        if len(hand) % groupSize:
            return False
        hand.sort()
        used = [False] * len(hand)
        for i in range(len(hand)):
            if used[i]:
                continue
            prev, placed = hand[i], 1
            used[i] = True
            j = i + 1
            while j < len(hand) and placed < groupSize:
                if not used[j] and hand[j] == prev + 1:
                    used[j] = True
                    prev = hand[j]
                    placed += 1
                j += 1
            if placed < groupSize:
                return False
        return True


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([1, 2, 3, 6, 2, 3, 4, 7, 8], 3, True),
             ([1, 2, 3, 4, 5], 4, False),
             ([1, 2, 3, 4, 5, 6], 2, True),
             ([8, 10, 12], 3, False)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for hand, g, want in cases:
        r1, r2 = Solution_1().isNStraightHand(hand[:], g), Solution_2().isNStraightHand(hand[:], g)
        ok &= r1 == r2 == want
        print(f"-> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
