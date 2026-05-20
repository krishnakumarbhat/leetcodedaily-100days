"""LeetCode 684: Redundant Connection - Medium"""
import time, tracemalloc
from typing import List

# Variation 1: Union Find - first edge that creates cycle
class Solution_v1:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        parent=list(range(len(edges)+1)); rank=[0]*(len(edges)+1)
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        for a,b in edges:
            pa,pb=find(a),find(b)
            if pa==pb: return [a,b]
            if rank[pa]<rank[pb]: pa,pb=pb,pa
            parent[pb]=pa
            if rank[pa]==rank[pb]: rank[pa]+=1
        return []

# Variation 2: DFS - check if path exists before adding edge
class Solution_v2:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        from collections import defaultdict
        graph=defaultdict(set)
        def dfs(src, dst, visited):
            if src==dst: return True
            visited.add(src)
            for nb in graph[src]:
                if nb not in visited and dfs(nb,dst,visited): return True
            return False
        for a,b in edges:
            if dfs(a,b,set()): return [a,b]
            graph[a].add(b); graph[b].add(a)
        return []

if __name__ == "__main__":
    edges=[[1,2],[1,3],[2,3]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().findRedundantConnection(edges)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: redundant={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
