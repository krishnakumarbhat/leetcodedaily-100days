"""
=====================================================================
LeetCode 49 : Group Anagrams                                    (Medium)
https://leetcode.com/problems/group-anagrams/
Category   : Arrays & Hashing
---------------------------------------------------------------------
PROBLEM
    Given an array of strings, group the anagrams together.
---------------------------------------------------------------------
INTUITION
    Two words are anagrams iff their ORDER-INSENSITIVE fingerprint
    matches. Fingerprint options: (a) 26-letter count TUPLE, (b) the
    sorted word. Hash the fingerprint → anagrams share a bucket.
---------------------------------------------------------------------
APPROACH 1 — Count-tuple key (BEST for long words)
    Time  Complexity : O(n·k)   Space Complexity : O(n·k)
    (n words × k letters each)
    WHY tuple: Python tuples are IMMUTABLE and therefore HASHABLE —
    they can be dict keys. Lists are mutable → unhashable → rejected.
---------------------------------------------------------------------
APPROACH 2 — Sorted-string key
    Time  Complexity : O(n·k log k)   Space Complexity : O(n·k)
    Simpler to write; slower on long words (k log k per word).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from collections import defaultdict
from typing import List


# =====================================================================
# APPROACH 1 : 26-count tuple fingerprint
# =====================================================================
class Solution_CountKey:
    """
    Purpose : Group all anagrams of the input words together.
    Inputs  : strs — list of words to group.
    Output  : list of groups; each group holds its anagrams.
    """

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # fingerprint (tuple of 26 counts) → list of words in that bucket.
        # defaultdict(list) auto-creates the list on first key access.
        groups: dict[tuple, list] = defaultdict(list)

        # Fingerprint every word exactly once.
        for word in strs:
            # count[0..25] = occurrences of 'a'..'z' in this word.
            count = [0] * 26
            for ch in word:
                # ord(ch) - ord('a') maps 'a'→0 … 'z'→25.
                count[ord(ch) - ord('a')] += 1

            # list → tuple: tuples are hashable, lists are not.
            # (1,0,2,...) is the word's order-insensitive fingerprint.
            key = tuple(count)

            # All words sharing the fingerprint land in the same bucket.
            groups[key].append(word)

        # dict_values → list of lists, the required output shape.
        return list(groups.values())


# =====================================================================
# APPROACH 2 : sorted-word fingerprint
# =====================================================================
class Solution_SortedKey:
    """
    Purpose : Group all anagrams of the input words together.
    Inputs  : strs — list of words to group.
    Output  : list of groups; each group holds its anagrams.
    """

    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # sorted word → group (canonical form as dict key).
        groups: dict[str, list] = defaultdict(list)

        # Fingerprint every word once.
        for word in strs:
            # Sorting erases order: "eat","tea","ate" all become "aet".
            key = "".join(sorted(word))

            # Same sorted form ⟺ same letter multiset ⟺ same group.
            groups[key].append(word)

        # Flatten into the required output shape.
        return list(groups.values())


# =====================================================================
# BENCHMARK — time + peak memory for both approaches
# =====================================================================
if __name__ == "__main__":
    strs = ["eat", "tea", "tan", "ate", "nat", "bat",
            "listen", "silent", "enlist", "inlets"]

    tracemalloc.start()
    t0 = time.perf_counter()
    r1 = Solution_CountKey().groupAnagrams(strs)
    t1 = time.perf_counter()
    _, peak1 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t2 = time.perf_counter()
    r2 = Solution_SortedKey().groupAnagrams(strs)
    t3 = time.perf_counter()
    _, peak2 = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Approach 1 (count-tuple key) : {len(r1)} groups  time = {(t1 - t0) * 1e6:.2f} µs  peak-mem = {peak1} bytes")
    print(f"Approach 2 (sorted key)      : {len(r2)} groups  time = {(t3 - t2) * 1e6:.2f} µs  peak-mem = {peak2} bytes")
    print("PASS : both approaches agree." if len(r1) == len(r2) else "FAIL : approaches disagree.")