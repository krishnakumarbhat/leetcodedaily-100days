"""LeetCode 226: Invert Binary Tree - Easy"""
import time, tracemalloc
from typing import List, Optional
from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right
def build(vals):
    if not vals: return None
    root = TreeNode(vals[0]); queue = deque([root]); i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i]); queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i]); queue.append(node.right)
        i += 1
    return root

# ============= Variation 1: Recursive (DFS) =============
# Time: O(n)   Space: O(h)
class Solution_v1:
    def invertTree(self, root):
        if not root: return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root

# ============= Variation 2: Iterative (BFS) =============
# Time: O(n)   Space: O(n)
class Solution_v2:
    def invertTree(self, root):
        if not root: return None
        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        return root

# ============= Variation 3: Iterative (Stack/DFS) =============
# Time: O(n)   Space: O(h)
class Solution_v3:
    def invertTree(self, root):
        if not root: return None
        stack = [root]
        while stack:
            node = stack.pop()
            node.left, node.right = node.right, node.left
            if node.left: stack.append(node.left)
            if node.right: stack.append(node.right)
        return root

if __name__ == "__main__":
    data = [4,2,7,1,3,6,9]
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2,Solution_v3],["DFS","BFS","Stack"]),1):
        tracemalloc.start(); t0=time.perf_counter()
        S().invertTree(build(data))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({n}): mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
