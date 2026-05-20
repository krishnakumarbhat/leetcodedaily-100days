"""
LeetCode 20: Valid Parentheses
Link: https://leetcode.com/problems/valid-parentheses/
Difficulty: Easy
"""
import time, tracemalloc

# ============= Variation 1: Replace Pairs =============
# Algorithm: Continuously scrub the string for valid pairs `()`, `{}`, `[]` and 
# replace them with nothing. If the string clears to empty, it was valid.
# Time Complexity: O(n^2)   Space Complexity: O(n)
class Solution_v1:
    def isValid(self, s: str) -> bool:
        while '()' in s or '{}' in s or '[]' in s:
            s = s.replace('()', '').replace('{}', '').replace('[]', '')
        return s == ''

# ============= Variation 2: Stack =============
# Algorithm: Use a stack to track open brackets. When a closing bracket appears, 
# it must match the top of the stack. If it does, pop; otherwise, invalid.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v2:
    def isValid(self, s: str) -> bool:
        stack = []
        mapping = {')': '(', '}': '{', ']': '['}
        for c in s:
            if c in mapping:
                if not stack or stack[-1] != mapping[c]: return False
                stack.pop()
            else:
                stack.append(c)
        return not stack

if __name__ == "__main__":
    s = "()[]{}"
    for i, (Sol, name) in enumerate(zip([Solution_v1, Solution_v2], ["Replace", "Stack"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        result = Sol().isValid(s)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 152 bytes and time = 12.00 µs
# var2 mem = 576 bytes and time = 14.13 µs
