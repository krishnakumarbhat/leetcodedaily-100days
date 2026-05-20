"""
LeetCode 567: Permutation in String
Link: https://leetcode.com/problems/permutation-in-string/
Difficulty: Medium
"""
import time, tracemalloc
from collections import Counter

# ============= Variation 1: Sorting each window =============
# Algorithm: Sort window substring arrays independently, verifying string equality 
# against a pre-sorted matching target string explicitly.
# Time Complexity: O(n * k log k)   Space Complexity: O(k)
class Solution_v1:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1_sorted = sorted(s1)
        for i in range(len(s2) - len(s1) + 1):
            if sorted(s2[i:i+len(s1)]) == s1_sorted:
                return True
        return False

# ============= Variation 2: Sliding Window Counter =============
# Algorithm: Maintain character counters across the sliding window exactly `len(s1)`.
# Slide pointer stepping left bound decrementally while right updates incrementally.
# Time Complexity: O(n)   Space Complexity: O(26)
class Solution_v2:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2): return False
        s1_count = Counter(s1)
        window = Counter(s2[:len(s1)])
        if window == s1_count: return True
        for i in range(len(s1), len(s2)):
            window[s2[i]] += 1
            left = s2[i - len(s1)]
            window[left] -= 1
            if window[left] == 0: del window[left]
            if window == s1_count: return True
        return False

# ============= Variation 3: Matches Count =============
# Algorithm: Keep count integer counting explicitly matched 26 characters explicitly.
# For each slide, update bounds map tracking match equality strictly. 26 means success.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v3:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2): return False
        s1c, s2c = [0]*26, [0]*26
        for i in range(len(s1)):
            s1c[ord(s1[i])-ord('a')] += 1
            s2c[ord(s2[i])-ord('a')] += 1
        matches = sum(1 for i in range(26) if s1c[i]==s2c[i])
        for i in range(len(s1), len(s2)):
            if matches == 26: return True
            idx = ord(s2[i])-ord('a')
            s2c[idx] += 1
            if s2c[idx]==s1c[idx]: matches += 1
            elif s2c[idx]==s1c[idx]+1: matches -= 1
            idx = ord(s2[i-len(s1)])-ord('a')
            s2c[idx] -= 1
            if s2c[idx]==s1c[idx]: matches += 1
            elif s2c[idx]==s1c[idx]-1: matches -= 1
        return matches == 26

if __name__ == "__main__":
    s1, s2 = "ab", "eidbaooo"
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2, Solution_v3], ["Sort", "Counter", "Matches"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().checkInclusion(s1, s2)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 1584 bytes and time = 28.62 µs
# var2 mem = 6875 bytes and time = 134.11 µs
# var3 mem = 1768 bytes and time = 24.05 µs
