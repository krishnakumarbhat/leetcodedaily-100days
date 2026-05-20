"""
LeetCode 150: Evaluate Reverse Polish Notation
Link: https://leetcode.com/problems/evaluate-reverse-polish-notation/
Difficulty: Medium
"""
import time, tracemalloc
from typing import List

# ============= Variation 1: Stack =============
# Algorithm: Push numbers onto a stack. When an operator is reached, pop the top 
# two numbers, apply the operation, and push the result back onto the stack.
# Time Complexity: O(n)   Space Complexity: O(n)
class Solution_v1:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for t in tokens:
            if t in '+-*/':
                b, a = stack.pop(), stack.pop()
                if t == '+': stack.append(a + b)
                elif t == '-': stack.append(a - b)
                elif t == '*': stack.append(a * b)
                else: stack.append(int(a / b))
            else:
                stack.append(int(t))
        return stack[0]

if __name__ == "__main__":
    tokens = ["2", "1", "+", "3", "*"]
    tracemalloc.start(); t0 = time.perf_counter()
    result = Solution_v1().evalRPN(tokens)
    t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1 (Stack): result={result}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 628 bytes and time = 34.94 µs
