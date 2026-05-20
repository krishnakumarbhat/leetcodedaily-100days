"""LeetCode 297: Serialize and Deserialize Binary Tree - Hard"""
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

class Codec_v1:
    def serialize(self, root):
        res = []
        def dfs(node):
            if not node: res.append("N"); return
            res.append(str(node.val)); dfs(node.left); dfs(node.right)
        dfs(root); return ",".join(res)
    def deserialize(self, data):
        vals = iter(data.split(","))
        def dfs():
            v = next(vals)
            if v == "N": return None
            node = TreeNode(int(v)); node.left = dfs(); node.right = dfs()
            return node
        return dfs()
if __name__ == "__main__":
    tracemalloc.start(); t0=time.perf_counter()
    c = Codec_v1(); s = c.serialize(build([1,2,3,None,None,4,5])); r = c.deserialize(s)
    t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"var1: serialized={s}, mem = {mem} bytes, time = {(t1-t0)*1e6:.2f} us")
# var1 mem = {} and time = {}
