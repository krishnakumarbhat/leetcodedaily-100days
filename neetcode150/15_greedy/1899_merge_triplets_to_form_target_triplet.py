"""
=====================================================================
LeetCode 1899 : Merge Triplets to Form Target Triplet             (Medium)
https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
Category   : Greedy
---------------------------------------------------------------------
PROBLEM
    Merge (coordinate-wise max) any subset of triplets; can the
    result equal the target exactly?
---------------------------------------------------------------------
INTUITION
    Triplets with a coordinate > target poison every merge (max never
    shrinks). Merge ALL admissible triplets — max is monotone, so the
    full set dominates any candidate subset.
---------------------------------------------------------------------
APPROACH 1 · Filter then merge
    Keep triplets with all coordinates ≤ target; coordinate-wise max;
    compare to target.
APPROACH 2 · Running best (in-place)
    Track (a,b,c) best-so-far over admissible triplets; identical
    math, O(1) state.
---------------------------------------------------------------------
DEEP DIVE · Why "merge everything admissible" is optimal
    Since max(a,b) ≥ a, merging never destroys a coordinate. If ANY
    subset reaches the target, the full admissible set reaches it too
    (it dominates every subset coordinate-wise). And inadmissible
    triplets can't help — a coordinate beyond target can never come
    back down. Nothing to choose ⇒ greedy trivially optimal.
---------------------------------------------------------------------
TIME COMPLEXITY : O(n)
MEMORY COMPLEXITY: O(1)
=====================================================================
"""


class Solution_1:
    def mergeTriplets(self, triplets, target):
        ok = [t for t in triplets
              if all(t[i] <= target[i] for i in range(3))]
        acc = [0, 0, 0]
        for t in ok:
            for i in range(3):
                acc[i] = max(acc[i], t[i])
        return acc == target


class Solution_2:
    def mergeTriplets(self, triplets, target):
        a = b = c = 0
        for t in triplets:
            if t[0] <= target[0] and t[1] <= target[1] and t[2] <= target[2]:
                a = max(a, t[0])
                b = max(b, t[1])
                c = max(c, t[2])
        return [a, b, c] == target


if __name__ == "__main__":
    import time, tracemalloc
    cases = [([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5], True),
             ([[2, 3, 4], [1, 2, 5], [3, 2, 2]], [2, 3, 5], True),
             ([[1, 1, 1]], [1, 1, 2], False),
             ([[3, 5, 3]], [3, 5, 3], True)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for ts, t, want in cases:
        r1, r2 = Solution_1().mergeTriplets(ts, t), Solution_2().mergeTriplets(ts, t)
        ok &= r1 == r2 == want
        print(f"-> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
