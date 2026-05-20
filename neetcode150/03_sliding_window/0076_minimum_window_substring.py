"""
LeetCode 76: Minimum Window Substring
Link: https://leetcode.com/problems/minimum-window-substring/
Difficulty: Hard
"""
import time, tracemalloc
from collections import Counter

# ============= Variation 1: Brute Force =============
# Algorithm: Iterate all pairs of `i, j` verifying whether string constraints in 
# `Counter(t)` loop matches.
# Time Complexity: O(n^2 * m)   Space Complexity: O(n)
class Solution_v1:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s: return ""
        t_count = Counter(t)
        min_len = float('inf'); result = ""
        for i in range(len(s)):
            count = Counter()
            for j in range(i, len(s)):
                count[s[j]] += 1
                if all(count[c] >= t_count[c] for c in t_count):
                    if j - i + 1 < min_len:
                        min_len = j - i + 1; result = s[i:j+1]
                    break
        return result

# ============= Variation 2: Sliding Window =============
# Algorithm: Keep count of required matched chars. As right pointer expands window, 
# increment formed. When required match met, capture length and locally shrink.
# Time Complexity: O(n+m)   Space Complexity: O(n+m)
class Solution_v2:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s: return ""
        t_count = Counter(t); required = len(t_count); formed = 0
        window = {}; l = 0; ans = (float('inf'), 0, 0)
        for r in range(len(s)):
            c = s[r]; window[c] = window.get(c, 0) + 1
            if c in t_count and window[c] == t_count[c]: formed += 1
            while formed == required:
                if r - l + 1 < ans[0]: ans = (r - l + 1, l, r)
                window[s[l]] -= 1
                if s[l] in t_count and window[s[l]] < t_count[s[l]]: formed -= 1
                l += 1
        return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]

if __name__ == "__main__":
    s, t = "ADOBECODEBANC", "ABC"
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Sliding Window"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().minWindow(s, t)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 5664 bytes and time = 373.22 µs
# var2 mem = 981 bytes and time = 36.49 µs
