"""LeetCode 133: Clone Graph - Medium"""
import time, tracemalloc
from collections import deque

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors else []

# Variation 1: DFS with hashmap
class Solution_v1:
    def cloneGraph(self, node):
        if not node: return None
        mp = {}
        def dfs(n):
            if n in mp: return mp[n]
            clone = Node(n.val); mp[n] = clone
            clone.neighbors = [dfs(nb) for nb in n.neighbors]
            return clone
        return dfs(node)

# Variation 2: BFS with hashmap
class Solution_v2:
    def cloneGraph(self, node):
        if not node: return None
        mp = {node: Node(node.val)}; q = deque([node])
        while q:
            n = q.popleft()
            for nb in n.neighbors:
                if nb not in mp: mp[nb] = Node(nb.val); q.append(nb)
                mp[n].neighbors.append(mp[nb])
        return mp[node]

if __name__ == "__main__":
    n1=Node(1); n2=Node(2); n3=Node(3); n4=Node(4)
    n1.neighbors=[n2,n4]; n2.neighbors=[n1,n3]; n3.neighbors=[n2,n4]; n4.neighbors=[n1,n3]
    for Vi, Cls in enumerate([Solution_v1, Solution_v2], 1):
        tracemalloc.start(); t0=time.perf_counter()
        clone=Cls().cloneGraph(n1)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: clone.val={clone.val}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
