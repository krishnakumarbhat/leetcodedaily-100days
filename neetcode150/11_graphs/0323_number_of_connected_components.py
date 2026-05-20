"""LeetCode 323: Number of Connected Components - Medium"""
import time, tracemalloc
from collections import defaultdict

# Variation 1: Union Find
class Solution_v1:
    def countComponents(self, n: int, edges) -> int:
        parent=list(range(n)); rank=[0]*n
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        count=n
        for a,b in edges:
            pa,pb=find(a),find(b)
            if pa==pb: continue
            if rank[pa]<rank[pb]: pa,pb=pb,pa
            parent[pb]=pa
            if rank[pa]==rank[pb]: rank[pa]+=1
            count-=1
        return count

# Variation 2: DFS
class Solution_v2:
    def countComponents(self, n: int, edges) -> int:
        graph=defaultdict(list)
        for a,b in edges: graph[a].append(b); graph[b].append(a)
        visited=set(); count=0
        def dfs(node):
            visited.add(node)
            for nb in graph[node]:
                if nb not in visited: dfs(nb)
        for i in range(n):
            if i not in visited: count+=1; dfs(i)
        return count

if __name__ == "__main__":
    edges=[[0,1],[1,2],[3,4]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().countComponents(5,edges)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: components={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
