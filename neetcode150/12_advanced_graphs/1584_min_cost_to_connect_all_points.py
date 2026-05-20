"""LeetCode 1584: Min Cost to Connect All Points - Medium"""
import time, tracemalloc
import heapq
from typing import List

# Variation 1: Prim's algorithm O(n^2 log n)
class Solution_v1:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n=len(points); visited=set(); total=0
        heap=[(0,0)]  # (cost, node)
        while len(visited)<n:
            cost,u=heapq.heappop(heap)
            if u in visited: continue
            visited.add(u); total+=cost
            for v in range(n):
                if v not in visited:
                    d=abs(points[u][0]-points[v][0])+abs(points[u][1]-points[v][1])
                    heapq.heappush(heap,(d,v))
        return total

# Variation 2: Kruskal's with Union Find
class Solution_v2:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n=len(points)
        edges=[]
        for i in range(n):
            for j in range(i+1,n):
                d=abs(points[i][0]-points[j][0])+abs(points[i][1]-points[j][1])
                edges.append((d,i,j))
        edges.sort(); parent=list(range(n)); total=0; used=0
        def find(x):
            while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
            return x
        for d,u,v in edges:
            pu,pv=find(u),find(v)
            if pu==pv: continue
            parent[pv]=pu; total+=d; used+=1
            if used==n-1: break
        return total

if __name__ == "__main__":
    pts=[[0,0],[2,2],[3,10],[5,2],[7,0]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().minCostConnectPoints(pts)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: cost={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
