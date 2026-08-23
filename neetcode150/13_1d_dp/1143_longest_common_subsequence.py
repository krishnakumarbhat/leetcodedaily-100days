"""
=====================================================================
LeetCode 1143 : Longest Common Subsequence                      (Medium)
https://leetcode.com/problems/longest-common-subsequence/
Category   : 1-D dynamic programming
---------------------------------------------------------------------
PROBLEM
    Length of the longest common subsequence of two strings.
---------------------------------------------------------------------
INTUITION
    dp[i][j] = LCS of the first i chars of text1 and first j of
    text2. Equal chars → 1 + dp[i-1][j-1]; else the max of dropping
    either tail. Rolling rows cut memory to O(min(m,n)).
---------------------------------------------------------------------
APPROACH 1 · Full DP table
    Standard 2D recurrence, easy to read and verify.
APPROACH 2 · Rolling two rows (memory-optimized)
    prev/cur rows; identical recurrence, O(n) memory.
---------------------------------------------------------------------
DEEP DIVE · Longest-path interpretation
    State (i,j) on a grid; a diagonal step (match) earns +1, right/
    down steps are free — dp is a longest path. Optimal substructure
    holds because a prefix of an optimal LCS is optimal for the
    corresponding prefix pair. 1000×1000 strings = 1M table cells
    (~8 MB) vs 8 KB for the rolling variant.
---------------------------------------------------------------------
TIME COMPLEXITY : O(m·n)
MEMORY COMPLEXITY: O(m·n) or O(n) rolling.
=====================================================================
"""


class Solution_1:
    def longestCommonSubsequence(self, text1, text2):
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]


class Solution_2:
    def longestCommonSubsequence(self, text1, text2):
        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)
        for i in range(1, m + 1):
            cur = [0] * (n + 1)
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1
                else:
                    cur[j] = max(prev[j], cur[j - 1])
            prev = cur
        return prev[n]


if __name__ == "__main__":
    import time, tracemalloc
    cases = [("abcde", "ace", 3), ("abc", "abc", 3), ("abc", "def", 0),
             ("bsbininm", "jmjkbkjkv", 1)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for a, b, want in cases:
        r1, r2 = Solution_1().longestCommonSubsequence(a, b), Solution_2().longestCommonSubsequence(a, b)
        ok &= r1 == r2 == want
        print(f'"{a}" x "{b}" -> A1={r1} A2={r2} (want {want}) {"PASS" if r1 == want and r2 == want else "FAIL"}')
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt*1e6:.0f} us | mem: {mem:.0f} KB")
