"""
LeetCode 271: Encode and Decode Strings
Link: https://leetcode.com/problems/encode-and-decode-strings/ (Premium)
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Length Prefix Encoding =============
# Algorithm: Encode the strings by prefixing each string with its length and a 
# special character (e.g., '#'). When decoding, read the length integer until '#', 
# then extract exactly that many characters. Repeat until the end of the string.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v1:
    def encode(self, strs: List[str]) -> str:
        result = ""
        for s in strs:
            result += str(len(s)) + "#" + s
        return result

    def decode(self, s: str) -> List[str]:
        result = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            length = int(s[i:j])
            result.append(s[j + 1: j + 1 + length])
            i = j + 1 + length
        return result

# ============= Variation 2: Delimiter with Escape =============
# Algorithm: Encode by replacing internal instances of the escape char ('/') and 
# delimiter ('#') to avoid conflicts. Then join strings with the delimiter.
# Decode by iterating character by character and interpreting the escape sequences.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def encode(self, strs: List[str]) -> str:
        return ''.join(s.replace('/', '//').replace('#', '/#') + '#' for s in strs)

    def decode(self, s: str) -> List[str]:
        result = []
        current = []
        i = 0
        while i < len(s):
            if s[i] == '/' and i + 1 < len(s):
                current.append(s[i + 1])
                i += 2
            elif s[i] == '#':
                result.append(''.join(current))
                current = []
                i += 1
            else:
                current.append(s[i])
                i += 1
        return result

# ============= Benchmarking =============
if __name__ == "__main__":
    strs = ["hello", "world", "foo#bar", "test/case", ""]
    solutions = [Solution_v1, Solution_v2]
    names = ["Length Prefix", "Delimiter+Escape"]

    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        sol = Sol()
        tracemalloc.start()
        t0 = time.perf_counter()
        encoded = sol.encode(strs)
        decoded = sol.decode(encoded)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): decoded={decoded}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 2403 bytes and time = 47.91 µs
# var2 mem = 1944 bytes and time = 52.11 µs
