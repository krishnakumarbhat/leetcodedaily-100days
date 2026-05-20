"""LeetCode 787: Cheapest Flights Within K Stops - Medium"""
import time, tracemalloc
import heapq
from typing import List

# Variation 1: Bellman-Ford (k+1 relaxations)
class Solution_v1:
    def findCheapestPrice(self, n, flights, src, dst, k) -> int:
        prices=[float("inf")]*n; prices[src]=0
        for _ in range(k+1):
            tmp=prices[:]
            for u,v,w in flights:
                if prices[u]+w<tmp[v]: tmp[v]=prices[u]+w
            prices=tmp
        return prices[dst] if prices[dst]!=float("inf") else -1

# Variation 2: Modified Dijkstra (stops as state)
class Solution_v2:
    def findCheapestPrice(self, n, flights, src, dst, k) -> int:
        from collections import defaultdict
        graph=defaultdict(list)
        for u,v,w in flights: graph[u].append((v,w))
        heap=[(0,src,0)]  # cost, node, stops
        visited={}
        while heap:
            cost,u,stops=heapq.heappop(heap)
            if u==dst: return cost
            if stops>k: continue
            if u in visited and visited[u]<=stops: continue
            visited[u]=stops
            for v,w in graph[u]: heapq.heappush(heap,(cost+w,v,stops+1))
        return -1

if __name__ == "__main__":
    flights=[[0,1,100],[1,2,100],[0,2,500]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().findCheapestPrice(3,flights,0,2,1)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: price={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
