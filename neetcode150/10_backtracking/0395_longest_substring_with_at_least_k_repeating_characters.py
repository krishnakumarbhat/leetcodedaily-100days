"""
=====================================================================
LeetCode 395 : Longest Substring with At Least K Repeating Chars  (Medium)
https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/
Category   : Backtracking / divide & conquer
---------------------------------------------------------------------
PROBLEM
    Longest substring where every character appears ≥ k times.
---------------------------------------------------------------------
INTUITION
    A char with total count < k can never belong to a valid substring
    — it splits the problem into independent gaps; recurse per gap.
---------------------------------------------------------------------
APPROACH 1 · Divide & conquer on blocker chars (best)
    Count in s; all counts ≥ k → whole string valid. Else split at
    each blocker and take the max over pieces.
APPROACH 2 · Sliding window per distinct-count
    For c in 1..26: longest window with ≤ c distinct letters where
    every letter occurs ≥ k times — the O(26n) two-pointer classic.
---------------------------------------------------------------------
DEEP DIVE · Why splitting on blockers is exact
    If 'x' occurs 2 < k times, any valid substring excludes x and
    lies entirely within one gap between x's. Gaps are independent,
    so recursion over gaps is complete and correct. A2's twist:
    "every char ≥ k" alone isn't a monotone window predicate, but
    fixing the distinct count IS — hence the 26 sweeps.
---------------------------------------------------------------------
TIME COMPLEXITY : A1 O(n²) worst; A2 O(26n).
MEMORY COMPLEXITY: O(n) / O(1) counters.
=====================================================================
"""
from collections import Counter


class Solution_1:
    def longestSubstring(self, s, k):
        if not s or len(s) < k:
            return 0
        cnt = Counter(s)
        for ch, c in cnt.items():
            if c < k:
                return max(self.longestSubstring(piece, k)
                           for piece in s.split(ch))
        return len(s)


class Solution_2:
    def longestSubstring(self, s, k):
        n, best = len(s), 0
        for distinct in range(1, 27):
            cnt = [0] * 26
            uniq = ok_cnt = 0
            l = 0
            for r in range(n):
                idx = ord(s[r]) - 97
                if cnt[idx] == 0:
                    uniq += 1
                cnt[idx] += 1
                if cnt[idx] == k:
                    ok_cnt += 1
                while uniq > distinct:
                    i = ord(s[l]) - 97
                    if cnt[i] == k:
                        ok_cnt -= 1
                    cnt[i] -= 1
                    if cnt[i] == 0:
                        uniq -= 1
                    l += 1
                if uniq == ok_cnt:
                    best = max(best, r - l + 1)
        return best


if __name__ == "__main__":
    import time, tracemalloc
    cases = [("aaabb", 3, 3), ("ababbc", 2, 5), ("ababacb", 3, 0), ("a", 1, 1)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for s, k, want in cases:
        r1, r2 = Solution_1().longestSubstring(s, k), Solution_2().longestSubstring(s, k)
        ok &= r1 == r2 == want
        print(f'"{s}" k={k} -> A1={r1} A2={r2} (want {want}) {"PASS" if r1 == want and r2 == want else "FAIL"}')
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
