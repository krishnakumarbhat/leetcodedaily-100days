"""
=====================================================================
LeetCode 1046 : Last Stone Weight                                (Easy)
https://leetcode.com/problems/last-stone-weight/
Category   : Heap / Priority queue
---------------------------------------------------------------------
PROBLEM
    Smash the two heaviest stones each round: equal weights destroy
    both; unequal weights keep the difference. Return the survivor
    weight (0 if nothing survives).
---------------------------------------------------------------------
INTUITION
    Each round needs the two LARGEST weights and inserts one new
    weight — a max-heap models the process directly in O(log n) per
    operation (heapq is a min-heap, so store negative weights).
---------------------------------------------------------------------
APPROACH 1 · Max-heap simulation (best)
    Negate every weight (heapq = min-heap). While ≥ 2 stones: pop two,
    smash, push back the difference as a negative if non-zero.
APPROACH 2 · Repeated sort (naive baseline)
    Sort descending each round, combine the two front elements.
---------------------------------------------------------------------
DEEP DIVE · Negative-weight idiom in Python
    heapq exposes only min-heaps, but a max-heap is one negation away:
    store -w and every pop() returns -largest. Arithmetic on the
    negatives mirrors the positives: a - b == -((-a) - (-b))... careful:
    we pop -a and -b (largest weights a ≥ b), remainder a-b becomes
    -(a-b) = (-a) - (-b) ... simplest: store w, pop gives -a, -b;
    push -(abs diff) when diff > 0. We implement that directly.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n log n) — n pushes + n/2 smash rounds.
MEMORY COMPLEXITY: O(n).
=====================================================================
"""
import heapq, time, tracemalloc


class Solution_1:
    """Max-heap simulation via negation."""

    def lastStoneWeight(self, stones):
        heap = [-w for w in stones]
        heapq.heapify(heap)
        while len(heap) > 1:
            a = -heapq.heappop(heap)         # heaviest
            b = -heapq.heappop(heap)         # second heaviest
            if a != b:
                heapq.heappush(heap, -(a - b))
        return -heap[0] if heap else 0


class Solution_2:
    """Repeated-sort baseline: O(n^2 log n)."""

    def lastStoneWeight(self, stones):
        stones = stones[:]
        while len(stones) > 1:
            stones.sort()
            a, b = stones.pop(), stones.pop()
            if a != b:
                stones.append(a - b)
        return stones[0] if stones else 0


if __name__ == "__main__":
    cases = [([2, 7, 4, 1, 8, 1], 1), ([1], 1), ([1, 1], 0)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for stones, want in cases:
        r1 = Solution_1().lastStoneWeight(stones[:])
        r2 = Solution_2().lastStoneWeight(stones[:])
        ok &= r1 == want and r2 == want
        print(f"-> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt * 1e6:.0f} us | mem: {mem:.0f} KB")
