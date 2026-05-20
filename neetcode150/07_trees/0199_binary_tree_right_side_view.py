"""LeetCode 199: Binary Tree Right Side View - Medium"""
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
    def rightSideView(self, root):
        if not root: return []
        result, queue = [], deque([root])
        while queue:
            for i in range(len(queue)):
                node = queue.popleft()
                if i == 0: result.append(node.val)
                if node.right: queue.append(node.right)
                if node.left: queue.append(node.left)
        return result
class Solution_v2:
    def rightSideView(self, root):
        res = []
        def dfs(node, depth):
            if not node: return
            if depth == len(res): res.append(node.val)
            dfs(node.right, depth+1); dfs(node.left, depth+1)
        dfs(root, 0); return res
if __name__ == "__main__":
    for i,(S,n) in enumerate(zip([Solution_v1,Solution_v2],["BFS","DFS"]),1):
        tracemalloc.start(); t0=time.perf_counter(); r=S().rightSideView(build([1,2,3,None,5,None,4]))
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{i} ({n}): result={r}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
