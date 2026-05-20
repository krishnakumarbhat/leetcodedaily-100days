"""
LeetCode 155: Min Stack
Link: https://leetcode.com/problems/min-stack/
Difficulty: Medium
"""
import time, tracemalloc

# ============= Variation 1: Two Stacks =============
# Algorithm: Maintain a main stack for values and a parallel `min_stack` to 
# store the minimum value up to that point. Pushing and popping affects both.
# Time Complexity: O(1) all ops   Space Complexity: O(n)
class MinStack_v1:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    def push(self, val: int) -> None:
        self.stack.append(val)
        self.min_stack.append(min(val, self.min_stack[-1] if self.min_stack else val))
    def pop(self) -> None:
        self.stack.pop(); self.min_stack.pop()
    def top(self) -> int:
        return self.stack[-1]
    def getMin(self) -> int:
        return self.min_stack[-1]

# ============= Variation 2: Stack with Tuples =============
# Algorithm: Store a tuple (current_value, current_minimum) on every push. 
# This eliminates the need for a separate physical stack while keeping space O(n).
# Time Complexity: O(1) all ops   Space Complexity: O(n)
class MinStack_v2:
    def __init__(self):
        self.stack = []  # (val, current_min)
    def push(self, val: int) -> None:
        cur_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, cur_min))
    def pop(self) -> None:
        self.stack.pop()
    def top(self) -> int:
        return self.stack[-1][0]
    def getMin(self) -> int:
        return self.stack[-1][1]

if __name__ == "__main__":
    for i, (Cls, name) in enumerate(zip([MinStack_v1, MinStack_v2], ["Two Stacks", "Tuples"]), 1):
        tracemalloc.start(); t0 = time.perf_counter()
        ms = Cls(); ms.push(-2); ms.push(0); ms.push(-3)
        r = ms.getMin(); ms.pop(); r2 = ms.top(); r3 = ms.getMin()
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({name}): min={r}, top={r2}, min={r3}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} µs")
# var1 mem = 2064 bytes and time = 25.55 µs
# var2 mem = 2152 bytes and time = 13.83 µs
