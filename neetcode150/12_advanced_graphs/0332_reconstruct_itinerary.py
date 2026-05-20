"""LeetCode 332: Reconstruct Itinerary - Hard"""
import time, tracemalloc
from collections import defaultdict

# Variation 1: Hierholzer DFS (Eulerian path)
class Solution_v1:
    def findItinerary(self, tickets):
        graph = defaultdict(list)
        for src,dst in sorted(tickets, reverse=True): graph[src].append(dst)
        route = []
        def dfs(airport):
            while graph[airport]: dfs(graph[airport].pop())
            route.append(airport)
        dfs("JFK")
        return route[::-1]

# Variation 2: Iterative Hierholzer
class Solution_v2:
    def findItinerary(self, tickets):
        graph = defaultdict(list)
        for src,dst in sorted(tickets, reverse=True): graph[src].append(dst)
        stack, route = ["JFK"], []
        while stack:
            while graph[stack[-1]]: stack.append(graph[stack[-1]].pop())
            route.append(stack.pop())
        return route[::-1]

if __name__ == "__main__":
    tickets=[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().findItinerary(tickets)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: {r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
