"""LeetCode 98: Validate Binary Search Tree - Medium"""
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

class Solution_v1:
    def isValidBST(self, root):
        def valid(node, lo, hi):
            if not node: return True
            if not (lo < node.val < hi): return False
            return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)
        return valid(root, float('-inf'), float('inf'))
class Solution_v2:
    def isValidBST(self, root):
        stack, prev = [], float('-inf')
        while stack or root:
            while root: stack.append(root); root = root.left
            root = stack.pop()
            if root.val <= prev: return False
            prev = root.val; root = root.right
        return True
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Recursive","Inorder"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().isValidBST(build([2,1,3]))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({n}): result={r}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
