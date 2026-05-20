"""LeetCode 104: Maximum Depth of Binary Tree - Easy"""
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

# ============= Variation 1: Recursive DFS =============
# Time: O(n)   Space: O(h)
class Solution_v1:
    def maxDepth(self, root): return 0 if not root else 1+max(self.maxDepth(root.left),self.maxDepth(root.right))

# ============= Variation 2: BFS =============
# Time: O(n)   Space: O(n)
class Solution_v2:
    def maxDepth(self, root):
        if not root: return 0
        q = deque([root]); depth = 0
        while q:
            depth += 1
            for _ in range(len(q)):
                n = q.popleft()
                if n.left: q.append(n.left)
                if n.right: q.append(n.right)
        return depth

# ============= Variation 3: Iterative DFS =============
# Time: O(n)   Space: O(h)
class Solution_v3:
    def maxDepth(self, root):
        if not root: return 0
        stack = [(root, 1)]; mx = 0
        while stack:
            node, d = stack.pop(); mx = max(mx, d)
            if node.left: stack.append((node.left, d+1))
            if node.right: stack.append((node.right, d+1))
        return mx

if __name__ == "__main__":
    data = [3,9,20,None,None,15,7]
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2,Solution_v3],["RecDFS","BFS","IterDFS"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().maxDepth(build(data))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({n}): result={r}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
