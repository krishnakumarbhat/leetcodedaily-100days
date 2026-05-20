"""LeetCode 210: Course Schedule II - Medium"""
import time, tracemalloc
from collections import defaultdict, deque

# Variation 1: Kahn topological sort (BFS)
class Solution_v1:
    def findOrder(self, numCourses, prerequisites):
        graph=defaultdict(list); indeg=[0]*numCourses
        for c,p in prerequisites: graph[p].append(c); indeg[c]+=1
        q=deque([i for i in range(numCourses) if indeg[i]==0]); order=[]
        while q:
            c=q.popleft(); order.append(c)
            for nb in graph[c]:
                indeg[nb]-=1
                if indeg[nb]==0: q.append(nb)
        return order if len(order)==numCourses else []

# Variation 2: DFS post-order topological sort
class Solution_v2:
    def findOrder(self, numCourses, prerequisites):
        graph=defaultdict(list)
        for c,p in prerequisites: graph[c].append(p)
        state=[0]*numCourses; order=[]
        def dfs(c):
            if state[c]==1: return False
            if state[c]==2: return True
            state[c]=1
            for nb in graph[c]:
                if not dfs(nb): return False
            state[c]=2; order.append(c); return True
        for c in range(numCourses):
            if not dfs(c): return []
        return order

if __name__ == "__main__":
    prereqs=[[1,0],[2,0],[3,1],[3,2]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().findOrder(4, prereqs)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: order={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
