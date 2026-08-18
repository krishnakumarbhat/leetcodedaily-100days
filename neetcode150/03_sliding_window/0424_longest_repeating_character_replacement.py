"""
LeetCode 424: Longest Repeating Character Replacement
Link: https://leetcode.com/problems/longest-repeating-character-replacement/
Difficulty: Medium
"""
import time, tracemalloc

# ============= Variation 1: Brute Force =============
# Algorithm: Iterate starting position. Tally occurrences counting inner loops natively.
# Stop expanding window logic when constraints `len - max_count > k` met.
# Time Complexity: O(n^2)   Space Complexity: O(26)
class Solution_v1:
    def characterReplacement(self, s: str, k: int) -> int:
        res = 0
        for i in range(len(s)):
            count = {}; max_freq = 0
            for j in range(i, len(s)):
                count[s[j]] = count.get(s[j], 0) + 1
                max_freq = max(max_freq, count[s[j]])
                if (j - i + 1) - max_freq <= k:
                    res = max(res, j - i + 1)
                else: break
        return res

# ============= Variation 2: Sliding Window =============
# Algorithm: Track absolute maximum frequency continuously. When validity bounds
# `(r - l + 1) - max_freq > k` fails, slide the left pointer incrementing constraints.
# Time Complexity: O(n)   Space Complexity: O(26)
class Solution_v2:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}; l = max_freq = res = 0
        for r in range(len(s)):
            count[s[r]] = count.get(s[r], 0) + 1
            max_freq = max(max_freq, count[s[r]])
            while (r - l + 1) - max_freq > k:
                count[s[l]] -= 1; l += 1
            res = max(res, r - l + 1)
        return res

if __name__ == "__main__":
    s, k = "AABABBA", 2
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Brute Force", "Sliding Window"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().characterReplacement(s, k)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 688 bytes and time = 54.62 µs
# var2 mem = 632 bytes and time = 17.95 µs
