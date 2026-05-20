"""LeetCode 621: Task Scheduler - Medium"""
import time, tracemalloc
import heapq
from collections import Counter, deque
from typing import List

# Variation 1: Math formula (greedy)
class Solution_v1:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counts = sorted(Counter(tasks).values(), reverse=True)
        max_count = counts[0]
        idle_slots = (max_count - 1) * n
        for c in counts[1:]: idle_slots -= min(c, max_count - 1)
        return len(tasks) + max(0, idle_slots)

# Variation 2: Max-heap simulation
class Solution_v2:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = Counter(tasks)
        heap = [-c for c in count.values()]
        heapq.heapify(heap)
        time_val = 0
        q = deque()  # (count, available_at)
        while heap or q:
            time_val += 1
            if heap:
                cnt = 1 + heapq.heappop(heap)  # decrement (negated)
                if cnt: q.append((cnt, time_val + n))
            if q and q[0][1] == time_val:
                heapq.heappush(heap, q.popleft()[0])
        return time_val

# Variation 3: Round-robin greedy simulation
class Solution_v3:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = Counter(tasks)
        max_count = max(count.values())
        max_count_tasks = sum(1 for v in count.values() if v == max_count)
        return max(len(tasks), (max_count - 1) * (n + 1) + max_count_tasks)

if __name__ == "__main__":
    tasks = ["A","A","A","B","B","B"]; n = 2
    for Vi, Cls in enumerate([Solution_v1, Solution_v2, Solution_v3], 1):
        tracemalloc.start(); t0 = time.perf_counter()
        r = Cls().leastInterval(tasks[:], n)
        t1 = time.perf_counter(); mem = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        print(f"var{Vi}: result={r}, mem={mem}bytes, time={(t1-t0)*1e6:.2f}us")
# var1 mem = {} and time = {}
# var2 mem = {} and time = {}
# var3 mem = {} and time = {}
