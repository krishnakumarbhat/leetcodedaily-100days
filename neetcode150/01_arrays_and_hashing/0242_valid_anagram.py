"""
LeetCode 242: Valid Anagram
Link: https://leetcode.com/problems/valid-anagram/
Difficulty: Easy
"""
import time, tracemalloc
from collections import Counter

# ============= Variation 1: Sorting =============
# Algorithm: Sort both strings. If they are anagrams, they will be identical after sorting.
# Time Complexity: O(n log n)   Space Complexity: O(n)
class Solution_v1:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)

# ============= Variation 2: Hash Map (Counter) =============
# Algorithm: Count the frequency of each character in both strings using a hash map 
# (or Python's Counter). If the maps are identical, they are anagrams.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)

# ============= Variation 3: Array Count (26 chars) =============
# Algorithm: Assuming lowercase English letters, use an array of size 26.
# Increment for chars in s, decrement for chars in t. Check if all counts are 0.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v3:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        count = [0] * 26
        for i in range(len(s)):
            count[ord(s[i]) - ord('a')] += 1
            count[ord(t[i]) - ord('a')] -= 1
        return all(c == 0 for c in count)

# ============= Benchmarking =============
if __name__ == "__main__":
    s, t = "anagram", "nagaram"
    solutions = [Solution_v1, Solution_v2, Solution_v3]
    names = ["Sorting", "Counter", "Array Count"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().isAnagram(s, t)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 248 bytes and time = 14.99 µs
# var2 mem = 5531 bytes and time = 98.58 µs
# var3 mem = 1424 bytes and time = 17.37 µs
