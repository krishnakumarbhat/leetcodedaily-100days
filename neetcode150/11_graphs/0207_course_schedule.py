"""LeetCode 207: Course Schedule - Medium"""
import time, tracemalloc
from collections import defaultdict, deque

# Variation 1: DFS cycle detection
class Solution_v1:
    def canFinish(self, numCourses: int, prerequisites) -> bool:
        graph = defaultdict(list)
        for c,p in prerequisites: graph[c].append(p)
        # 0=unvisited, 1=in-stack, 2=done
        state = [0]*numCourses
        def dfs(c):
            if state[c]==1: return False  # cycle
            if state[c]==2: return True
            state[c]=1
            for nb in graph[c]:
                if not dfs(nb): return False
            state[c]=2; return True
        return all(dfs(c) for c in range(numCourses))

# Variation 2: Topological sort (Kahn BFS)
class Solution_v2:
    def canFinish(self, numCourses: int, prerequisites) -> bool:
        graph = defaultdict(list); indeg = [0]*numCourses
        for c,p in prerequisites: graph[p].append(c); indeg[c]+=1
        q = deque([i for i in range(numCourses) if indeg[i]==0])
        done = 0
        while q:
            c = q.popleft(); done+=1
            for nb in graph[c]:
                indeg[nb]-=1
                if indeg[nb]==0: q.append(nb)
        return done==numCourses

if __name__ == "__main__":
    prereqs=[[1,0],[2,0],[3,1],[3,2]]
    for Vi,Cls in enumerate([Solution_v1,Solution_v2],1):
        tracemalloc.start(); t0=time.perf_counter()
        r=Cls().canFinish(4, prereqs)
        t1=time.perf_counter(); mem=tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: can_finish={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
