"""
LeetCode 125: Valid Palindrome
Link: https://leetcode.com/problems/valid-palindrome/
Difficulty: Easy
"""
import time, tracemalloc

# ============= Variation 1: Filter + Reverse =============
# Algorithm: Create an entirely new string skipping non-alphanumeric chars and 
# forcing `.lower()`. Palindromes read the same backwards, so verify string equals its reversed self.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v1:
    def isPalindrome(self, s: str) -> bool:
        filtered = ''.join(c.lower() for c in s if c.isalnum())
        return filtered == filtered[::-1]

# ============= Variation 2: Two Pointers =============
# Algorithm: Left pointer goes right, Right pointer goes left. Both bypass spaces 
# and symbols natively. Validate that matching lowercase letters equal.
# Time Complexity: O(n)   Space Complexity: O(1)
class Solution_v2:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum(): l += 1
            while l < r and not s[r].isalnum(): r -= 1
            if s[l].lower() != s[r].lower(): return False
            l += 1; r -= 1
        return True

# ============= Benchmarking =============
if __name__ == "__main__":
    s = "A man, a plan, a canal: Panama"
    solutions = [Solution_v1, Solution_v2]
    names = ["Filter+Reverse", "Two Pointers"]
    for i, (Sol, name) in enumerate(zip(solutions, names), 1):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = Sol().isPalindrome(s)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")

# var1 mem = 1464 bytes and time = 42.85 µs
# var2 mem = 148 bytes and time = 16.72 µs
