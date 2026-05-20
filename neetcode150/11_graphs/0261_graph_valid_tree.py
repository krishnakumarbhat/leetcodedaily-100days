"""LeetCode 261: Graph Valid Tree - Medium"""
import time, tracemalloc
from collections import defaultdict

# Variation 1: Union Find (valid tree = n-1 edges, no cycle)
class Solution_v1:
    def validTree(self, n: int, edges) -> bool:
        if len(edges)!=n-1: return False
        parent=list(range(n))
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        for a,b in edges:
            pa,pb=find(a),find(b)
            if pa==pb: return False
            parent[pb]=pa
        return True

# Variation 2: DFS cycle detection
class Solution_v2:
    def validTree(self, n: int, edges) -> bool:
        if len(edges)!=n-1: return False
        graph=defaultdict(list)
        for a,b in edges: graph[a].append(b); graph[b].append(a)
        visited=set()
        def dfs(node, parent):
            if node in visited: return False
            visited.add(node)
            for nb in graph[node]:
                if nb==parent: continue
                if not dfs(nb,node): return False
            return True
        return dfs(0,-1) and len(visited)==n

if __name__ == "__main__":
    edges=[[0,1],[0,2],[0,3],[1,4]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().validTree(5,edges)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: valid_tree={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
