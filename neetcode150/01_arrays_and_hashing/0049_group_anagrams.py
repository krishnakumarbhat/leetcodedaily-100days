"""
LeetCode 49: Group Anagrams
Link: https://leetcode.com/problems/group-anagrams/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List
from collections import defaultdict

# ============= Variation 1: Sorted Key =============
# Algorithm: Iterate over the strings. For each string, sort it to create a key.
# All anagrams will have the exact same sorted key. Append the original string
# to the list matching that key in a default dictionary.
# Time Complexity: O(n * k log k)   Space Complexity: O(n * k)
class Solution_v1:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            key = tuple(sorted(s))
            groups[key].append(s)
        return list(groups.values())

# ============= Variation 2: Character Count Key =============
# Algorithm: Iterate over strings. For each string, compute a 26-element array counting
# character frequencies. Convert this array to a tuple to use as a dictionary key.
# This avoids the O(k log k) sorting overhead.
# Time Complexity: O(n * k)   Space Complexity: O(n * k)
class Solution_v2:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            groups[tuple(count)].append(s)
        return list(groups.values())

# ============= Benchmarking =============
if __name__ == "__main__":
    strs = ["eat", "tea", "tan", "ate", "nat", "bat", "tab", "ant", "ten"]
    solutions = [Solution_v1, Solution_v2]
    names = ["Sorted Key", "Char Count Key"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().groupAnagrams(strs[:])
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): groups={len(result)}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 2304 bytes and time = 53.44 µs
# var2 mem = 2584 bytes and time = 48.86 µs
