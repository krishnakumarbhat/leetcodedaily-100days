"""LeetCode 743: Network Delay Time - Medium"""
import time, tracemalloc
import heapq
from collections import defaultdict
from typing import List

# Variation 1: Dijkstra with min-heap
class Solution_v1:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph=defaultdict(list)
        for u,v,w in times: graph[u].append((v,w))
        dist={i:float("inf") for i in range(1,n+1)}; dist[k]=0
        heap=[(0,k)]
        while heap:
            d,u=heapq.heappop(heap)
            if d>dist[u]: continue
            for v,w in graph[u]:
                if dist[u]+w<dist[v]: dist[v]=dist[u]+w; heapq.heappush(heap,(dist[v],v))
        mx=max(dist.values())
        return mx if mx<float("inf") else -1

# Variation 2: Bellman-Ford O(VE)
class Solution_v2:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        dist=[float("inf")]*(n+1); dist[k]=0
        for _ in range(n-1):
            for u,v,w in times:
                if dist[u]+w<dist[v]: dist[v]=dist[u]+w
        mx=max(dist[1:])
        return mx if mx<float("inf") else -1

if __name__ == "__main__":
    times=[[2,1,1],[2,3,1],[3,4,1]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().networkDelayTime(times,4,2)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: delay={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
