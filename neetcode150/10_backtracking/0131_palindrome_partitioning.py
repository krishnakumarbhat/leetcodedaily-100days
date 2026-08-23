"""
=====================================================================
LeetCode 131 : Palindrome Partitioning                            (Medium)
https://leetcode.com/problems/palindrome-partitioning/
Category   : Backtracking
---------------------------------------------------------------------
PROBLEM
    All ways to split s into all-palindrome substrings.
---------------------------------------------------------------------
INTUITION
    Cut after every possible palindrome prefix, recurse on the rest —
    backtracking over cut positions.
---------------------------------------------------------------------
APPROACH 1 · DFS + direct palindrome probe (best for short input)
    dfs(start): start == n → record. For end in start..n: if the
    slice is a palindrome, take it, recurse(end+1).
APPROACH 2 · Precomputed palindrome table
    isPal[i][j] via DP in O(n²), then O(1) queries in the same DFS.
---------------------------------------------------------------------
DEEP DIVE · Table vs probe trade-off
    The probe costs O(n) per cut probe — fine for small strings, but
    a 2^n-shaped search tree makes the table worthwhile past n ≈ 20.
    DP identity: s[i]==s[j] and (j-i < 2 or isPal[i+1][j-1]).
---------------------------------------------------------------------
TIME COMPLEXITY : A1 O(n·2^n) worst; A2 O(2^n) + O(n²) build.
MEMORY COMPLEXITY: O(n²) for the table in A2.
=====================================================================
"""


class Solution_1:
    def partition(self, s):
        out, cur = [], []

        def is_pal(l, r):
            return s[l:r + 1] == s[l:r + 1][::-1]

        def dfs(start):
            if start == len(s):
                out.append(cur[:])
                return
            for end in range(start, len(s)):
                if not is_pal(start, end):
                    continue
                cur.append(s[start:end + 1])
                dfs(end + 1)
                cur.pop()

        dfs(0)
        return out


class Solution_2:
    def partition(self, s):
        n = len(s)
        pal = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
        out, cur = [], []

        def dfs(start):
            if start == n:
                out.append(cur[:])
                return
            for end in range(start, n):
                if not pal[start][end]:
                    continue
                cur.append(s[start:end + 1])
                dfs(end + 1)
                cur.pop()

        dfs(0)
        return out


if __name__ == "__main__":
    import time, tracemalloc
    cases = [("aab", 2), ("a", 1), ("aaa", 4)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for s, want in cases:
        r1, r2 = len(Solution_1().partition(s)), len(Solution_2().partition(s))
        ok &= r1 == r2 == want
        print(f'"{s}" -> A1={r1} A2={r2} (want {want}) {"PASS" if r1 == want and r2 == want else "FAIL"}')
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
