"""LeetCode 235: Lowest Common Ancestor of BST - Medium"""
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
    def lowestCommonAncestor(self, root, p, q):
        while root:
            if p.val < root.val and q.val < root.val: root = root.left
            elif p.val > root.val and q.val > root.val: root = root.right
            else: return root
class Solution_v2:
    def lowestCommonAncestor(self, root, p, q):
        if not root: return None
        if p.val < root.val and q.val < root.val: return self.lowestCommonAncestor(root.left, p, q)
        if p.val > root.val and q.val > root.val: return self.lowestCommonAncestor(root.right, p, q)
        return root
if __name__ == "__main__":
    root = build([6,2,8,0,4,7,9,None,None,3,5]); p = root.left; q = root.right
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Iterative","Recursive"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().lowestCommonAncestor(build([6,2,8,0,4,7,9,None,None,3,5]),TreeNode(2),TreeNode(8))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({n}): result={r.val if r else None}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
