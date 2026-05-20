"""LeetCode 1448: Count Good Nodes in Binary Tree - Medium"""
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
    def goodNodes(self, root):
        def dfs(node, max_val):
            if not node: return 0
            res = 1 if node.val >= max_val else 0
            max_val = max(max_val, node.val)
            return res + dfs(node.left, max_val) + dfs(node.right, max_val)
        return dfs(root, root.val)
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter(); r=Solution_v1().goodNodes(build([3,1,4,3,None,1,5]))
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: result={r}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
