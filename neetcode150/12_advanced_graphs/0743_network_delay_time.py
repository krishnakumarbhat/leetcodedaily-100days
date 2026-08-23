"""
=====================================================================
LeetCode 743 : Network Delay Time                                (Medium)
https://leetcode.com/problems/network-delay-time/
Category   : Advanced Graphs
---------------------------------------------------------------------
PROBLEM
    n network nodes labelled 1..n. times[i] = (u, v, w) means a signal
    travels from u to v in w ms. A signal starts at node k and fans
    out along all edges simultaneously. Return the time it takes for
    ALL n nodes to receive the signal, or -1 if some node is
    unreachable from k.
---------------------------------------------------------------------
INTUITION
    "Fans out along all edges" = each node receives the signal as soon
    as the SHORTEST path from k reaches it. Answer = maximum over all
    nodes of the shortest-path distance from k — a single-source
    shortest paths problem. All weights are positive → Dijkstra.
---------------------------------------------------------------------
APPROACH 1 — Dijkstra with a min-heap (BEST)
    dist[u] = best-known distance from k. Repeat: extract the node
    with the smallest dist (min-heap, O(log V)), settle it, and relax
    each outgoing edge (u -> v, w): if dist[u] + w < dist[v], improve
    dist[v] and push it back. Answer = max(dist[1..n]).
    Time  Complexity : O(E log V) — each edge relaxed once, heap ops
                         O(log V).
    Space Complexity : O(V + E)   — dist + adjacency + heap.
---------------------------------------------------------------------
APPROACH 2 — Bellman-Ford (no heap, V-1 relaxation rounds)
    Repeat V-1 rounds: scan every edge and relax dist[v] = min(...).
    After round i every node's dist is correct for paths using at most
    i edges; V-1 rounds cover every simple path. Early-exit when a
    round changes nothing.
    Time  Complexity : O(V·E)   Space Complexity : O(V)
---------------------------------------------------------------------
DEEP DIVE — Dijkstra proof sketch, and what breaks it
    Invariant: when a node u is POPPED, dist[u] is its true shortest
    distance. Induction on pop order: u is the un-settled node with
    the smallest dist; any alternative path k → … → x → u must pass
    through an un-settled x with dist[x] ≥ dist[u], and all remaining
    edge weights are POSITIVE, so that path costs ≥ dist[x] + w
    > dist[u]. No later relaxation can beat it. NEGATIVE EDGES BREAK
    THIS: a path k → … → x → (negative edge) → u can cost LESS than
    dist[u] even when dist[x] > dist[u] — the settled-set argument
    collapses. Bellman-Ford survives negatives by relaxing everything
    once per round, one edge at a time.
---------------------------------------------------------------------
REAL LIFE
    • OSPF / IS-IS internet routing — every router runs Dijkstra on
      link-state advertisements to build its forwarding table.
    • CDN / cloud latency maps — "how long until my edge node sees it".
    • GPS navigation — shortest path in a road graph (positive weights).
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
import heapq
from typing import List


# =====================================================================
# APPROACH 1 : Dijkstra with a min-heap
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the time until the LAST node receives the signal
              (= max shortest distance from k), or -1 if unreachable.
    Inputs  : times — list of [u, v, w] directed edges.
              n     — number of nodes (labelled 1..n).
              k     — source node where the signal starts.
    Output  : int — max shortest-path distance, or -1.
    """

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # adjacency: g[u] = list of (v, w)
        g: dict[int, List[tuple[int, int]]] = {}
        for u, v, w in times:
            g.setdefault(u, []).append((v, w))

        INF = 10**9
        dist = [INF] * (n + 1)   # dist[u] = best-known distance from k
        dist[k] = 0

        # Min-heap of (distance, node); heapq is a genuine binary heap.
        pq: List[tuple[int, int]] = [(0, k)]

        while pq:
            d, u = heapq.heappop(pq)
            # Stale heap entry (u was improved after this push) — skip.
            if d > dist[u]:
                continue
            # u is now SETTLED: dist[u] is final (see header proof).
            for v, w in g.get(u, []):
                # Relaxation: detour through u cheaper than known?
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))

        # The last node to receive the signal = max over all nodes.
        ans = 0
        for i in range(1, n + 1):
            if dist[i] == INF:
                return -1      # unreachable node
            ans = max(ans, dist[i])
        return ans


# =====================================================================
# APPROACH 2 : Bellman-Ford (V-1 relaxation rounds)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Same result without any heap — relax every edge in V-1
              rounds; each round extends paths by one edge.
    Inputs  : times — list of [u, v, w] directed edges.
              n     — number of nodes (labelled 1..n).
              k     — source node where the signal starts.
    Output  : int — max shortest-path distance, or -1.
    """

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        INF = 10**9
        dist = [INF] * (n + 1)
        dist[k] = 0

        # A simple path has at most n-1 edges → n-1 rounds suffice.
        for _ in range(n - 1):
            changed = False
            for u, v, w in times:
                # Relax every edge; only improve from reachable nodes.
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    changed = True
            # No improvement → distances already final; stop early.
            if not changed:
                break

        ans = 0
        for i in range(1, n + 1):
            if dist[i] == INF:
                return -1
            ans = max(ans, dist[i])
        return ans


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example 1 — 2 -> 3 -> 4 chain, answer 2.
    t1 = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    # Test 2: single edge, source reaches node 2 directly.
    t2 = [[1, 2, 1]]
    # Test 3: same edge but node 2 is NOT the source → unreachable.
    t3 = [[1, 2, 1]]
    cases = [(t1, 4, 2, 2), (t2, 2, 1, 1), (t3, 2, 2, -1)]

    all_ok = True
    for idx, (times, n, k, want) in enumerate(cases):
        # --- Approach 1: Dijkstra, time + peak memory ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().networkDelayTime(times, n, k)
        t1_ = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: Bellman-Ford ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().networkDelayTime(times, n, k)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok1 = r1 == want
        ok2 = r2 == want
        all_ok = all_ok and ok1 and ok2

        print(f"Test {idx+1} A1 (Dijkstra)    : {r1}  {('PASS' if ok1 else 'FAIL')}  "
              f"time = {(t1_-t0)*1e6:.2f} us  peak = {peak1/1024:.1f} KB")
        print(f"Test {idx+1} A2 (Bellman-Ford): {r2}  {('PASS' if ok2 else 'FAIL')}  "
              f"time = {(t1b-t0b)*1e6:.2f} us  peak = {peak2/1024:.1f} KB")

    print("PASS : both approaches match the expected delays."
          if all_ok else "FAIL : at least one answer is wrong.")