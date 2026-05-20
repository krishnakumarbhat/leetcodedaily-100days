"""
LeetCode 3: Longest Substring Without Repeating Characters
Link: https://leetcode.com/problems/longest-substring-without-repeating-characters/
Difficulty: Medium
"""
import time, tracemalloc

# ============= Variation 1: Brute Force =============
# Algorithm: Use two nested loops to check every substring. Use a set inside the inner loop 
# to track repeated characters. If a char is repeated, break the loop. Return max length.
# Time Complexity: O(n^3)   Space Complexity: O(min(n, m))
class Solution_v1:
    def lengthOfLongestSubstring(self, s: str) -> int:
        res = 0
        for i in range(len(s)):
            seen = set()
            for j in range(i, len(s)):
                if s[j] in seen: break
                seen.add(s[j])
                res = max(res, j - i + 1)
        return res

# ============= Variation 2: Sliding Window with Set =============
# Algorithm: Increment an `r` pointer dynamically to add characters to the set.
# If a duplicate string exists, incrementally remove characters backwards off `l` pointer.
# Time Complexity: O(n)   Space Complexity: O(min(n, m))
class Solution_v2:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        l = res = 0
        for r in range(len(s)):
            while s[r] in char_set:
                char_set.remove(s[l]); l += 1
            char_set.add(s[r])
            res = max(res, r - l + 1)
        return res

# ============= Variation 3: Sliding Window with HashMap =============
# Algorithm: Same as Sliding Window but use a map to keep indexes, skipping redundant 
# left shifts. `l` is set to max of itself and the stored index `mp[s[r]] + 1`.
# Time Complexity: O(n)   Space Complexity: O(min(n, m))
class Solution_v3:
    def lengthOfLongestSubstring(self, s: str) -> int:
        mp = {}
        l = res = 0
        for r in range(len(s)):
            if s[r] in mp and mp[s[r]] >= l:
                l = mp[s[r]] + 1
            mp[s[r]] = r
            res = max(res, r - l + 1)
        return res

if __name__ == "__main__":
    s = "abcabcbbdefgh"
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2, Solution_v3], ["Brute Force", "SW Set", "SW Map"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().lengthOfLongestSubstring(s)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1512 bytes and time = 59.13 µs
# var2 mem = 1080 bytes and time = 20.60 µs
# var3 mem = 904 bytes and time = 15.43 µs
