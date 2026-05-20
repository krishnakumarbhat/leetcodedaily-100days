"""LeetCode 105: Construct Binary Tree from Preorder and Inorder - Medium"""
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
    def buildTree(self, preorder, inorder):
        if not preorder: return None
        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        return root
class Solution_v2:
    def buildTree(self, preorder, inorder):
        inorder_map = {v:i for i,v in enumerate(inorder)}
        self.idx = 0
        def helper(l, r):
            if l > r: return None
            val = preorder[self.idx]; self.idx += 1
            node = TreeNode(val)
            node.left = helper(l, inorder_map[val]-1)
            node.right = helper(inorder_map[val]+1, r)
            return node
        return helper(0, len(inorder)-1)
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["Recursive","HashMap"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().buildTree([3,9,20,15,7],[9,3,15,20,7])
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({n}): mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
