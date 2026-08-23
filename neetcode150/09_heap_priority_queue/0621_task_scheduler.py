"""
=====================================================================
LeetCode 621 : Task Scheduler                                    (Medium)
https://leetcode.com/problems/task-scheduler/
Category   : Heap / greedy
---------------------------------------------------------------------
PROBLEM
    Tasks labelled 'A'..'Z' must run on one CPU; the SAME task cannot
    run twice within n steps. Return the minimum number of time units
    (idle allowed) to finish all tasks.
---------------------------------------------------------------------
INTUITION
    The most frequent task dictates the skeleton of the schedule; idle
    slots appear only to satisfy its cooldown. Two views: a closed
    formula (O(1)) and a heap simulation (fidelity for complex cases).
---------------------------------------------------------------------
APPROACH 1 · Math formula (best)
    m = max frequency, c = count of tasks with frequency m.
    answer = max((m - 1) * (n + 1) + c, len(tasks)).
APPROACH 2 · Heap simulation
    Max-heap of remaining counts + FIFO cooldown queue; every second
    run the most frequent available task, park it for n seconds.
---------------------------------------------------------------------
DEEP DIVE · Why the formula is exact
    The busiest task T appears m times; between consecutive copies we
    need n other/ idle slots — that core costs (m-1)(n+1) units, and
    the LAST row fits all c tasks that tie with T. Filling the core
    gaps with the remaining tasks is always possible greedily, so the
    lower bound is tight. If tasks alone already fill every slot
    (len(tasks) larger), no idle is needed. O(1) beats O(26 log 26).
---------------------------------------------------------------------
TIME COMPLEXITY : O(1)  — one pass over 26 counters.
MEMORY COMPLEXITY: O(1).
=====================================================================
"""
import heapq, collections, time, tracemalloc


class Solution_1:
    """Closed-form formula."""

    def leastInterval(self, tasks, n):
        cnt = collections.Counter(tasks)
        m = max(cnt.values())
        c = sum(1 for v in cnt.values() if v == m)
        return max((m - 1) * (n + 1) + c, len(tasks))


class Solution_2:
    """Heap + cooldown-queue simulation."""

    def leastInterval(self, tasks, n):
        cnt = collections.Counter(tasks)
        heap = [-v for v in cnt.values()]
        heapq.heapify(heap)
        cooldown = collections.deque()     # (remaining, readyAt)
        t = 0
        while heap or cooldown:
            t += 1
            if heap:
                rem = -heapq.heappop(heap) - 1
                if rem > 0:
                    cooldown.append((rem, t + n))
            if cooldown and cooldown[0][1] == t:
                heapq.heappush(heap, -cooldown.popleft()[0])
        return t


if __name__ == "__main__":
    cases = [(["A", "A", "A", "B", "B", "B"], 2, 8),
             (["A", "A", "A", "B", "B", "B"], 0, 6),
             (["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2, 16),
             (["A", "B", "C", "D"], 3, 4)]
    tracemalloc.start()
    t0 = time.perf_counter()
    ok = True
    for tasks, n, want in cases:
        r1 = Solution_1().leastInterval(tasks[:], n)
        r2 = Solution_2().leastInterval(tasks[:], n)
        ok &= r1 == want and r2 == want
        print(f"n={n} -> A1={r1} A2={r2} (want {want}) {'PASS' if r1 == want and r2 == want else 'FAIL'}")
    dt = time.perf_counter() - t0
    mem = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"{'PASS : all cases' if ok else 'FAIL'} | time: {dt * 1e6:.0f} us | mem: {mem:.0f} KB")
