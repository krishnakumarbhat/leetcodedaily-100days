"""
=====================================================================
LeetCode 332 : Reconstruct Itinerary                              (Hard)
https://leetcode.com/problems/reconstruct-itinerary/
Category   : Advanced Graphs
---------------------------------------------------------------------
PROBLEM
    Given a list of airline tickets [from, to], rebuild the itinerary
    in order. The trip MUST start at "JFK" and use EVERY ticket
    exactly once. When several itineraries exist, return the one that
    is lexicographically smallest. Input guarantees a valid itinerary.
---------------------------------------------------------------------
INTUITION
    Every airport is a vertex, every ticket is a directed edge, and we
    must traverse EVERY edge exactly once — an EULERIAN PATH. The
    guarantee makes the graph Eulerian, so the problem reduces to:
    walk all edges exactly once, always taking the lexicographically
    smallest next airport (Hierholzer's algorithm).
---------------------------------------------------------------------
APPROACH 1 — Hierholzer, recursive DFS (BEST)
    Build adjacency: airport -> destinations, sorted DESCENDING so
    that pop() hands back the SMALLEST remaining destination. DFS:
    keep following smallest unused tickets; append the airport to the
    route only AFTER all its edges are consumed (post-order). Reverse
    at the end.
    Time  Complexity : O(E log E) — sorting each adjacency list
                         dominates (E = tickets).
    Space Complexity : O(E)       — adjacency + route.
---------------------------------------------------------------------
APPROACH 2 — Hierholzer, iterative (no recursion)
    Identical walk with an explicit stack, so deep graphs cannot
    overflow Python's recursion limit. Dead ends are closed out by
    appending to the route and popping the stack.
    Time  Complexity : O(E log E)   Space Complexity : O(E)
---------------------------------------------------------------------
DEEP DIVE — Hierholzer and the reversal trick
    Naive DFS walks into a dead end only when every remaining edge is
    inside cycles; those cycles get appended to the route exactly when
    the dead end is reached. Reversing the post-order list plugs every
    cycle back into the walk at the vertex where it was entered — each
    edge is traversed exactly once, total O(E). Python detail: the
    graph is a defaultdict (open addressing dict, linear probing
    h(k, i) = (hash(k) + i) mod m) — O(1) lookups per airport.
---------------------------------------------------------------------
REAL LIFE
    • Airline crew / aircraft rotation planning — fly every leg once.
    • DNA fragment assembly (de Bruijn graphs) — Eulerian path over
      k-mers reconstructs the genome.
    • Street-sweeping / snow-plough routing — cover every road once.
=====================================================================
"""

from __future__ import annotations
import time
import tracemalloc
from typing import List, Optional
from collections import defaultdict


# =====================================================================
# APPROACH 1 : Hierholzer's algorithm, recursive DFS
# =====================================================================
class SolutionOne:
    """
    Purpose : Return the lexicographically smallest Eulerian path that
              starts at "JFK" and uses every ticket exactly once.
    Inputs  : tickets — list of [from, to] airport-code pairs.
    Output  : List[str] — the ordered itinerary.
    """

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        # graph : airport -> destinations sorted DESCENDING so that
        #         pop() returns the SMALLEST remaining destination.
        graph: dict[str, list[str]] = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)

        route: List[str] = []

        def dfs(airport: str) -> None:
            # Keep following the smallest unused ticket. The loop ends
            # only when this airport's edges are exhausted.
            while graph[airport]:
                # pop() = smallest destination (list sorted descending).
                dfs(graph[airport].pop())
            # All outgoing edges used → close the airport out (post-order).
            route.append(airport)

        dfs("JFK")

        # The post-order walk is the itinerary read backwards.
        return route[::-1]


# =====================================================================
# APPROACH 2 : Hierholzer's algorithm, iterative (explicit stack)
# =====================================================================
class SolutionTwo:
    """
    Purpose : Same Eulerian path without recursion — an explicit stack
              replaces the call stack, safe for deep graphs.
    Inputs  : tickets — list of [from, to] airport-code pairs.
    Output  : List[str] — the ordered itinerary.
    """

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph: dict[str, list[str]] = defaultdict(list)
        for src, dst in sorted(tickets, reverse=True):
            graph[src].append(dst)

        stack: List[str] = ["JFK"]
        route: List[str] = []

        while stack:
            top = stack[-1]
            # Top airport still has unused tickets → descend into its
            # smallest destination (same rule as the recursive DFS).
            if graph[top]:
                stack.append(graph[top].pop())
            else:
                # Dead end reached: all edges of `top` are used.
                route.append(top)
                stack.pop()

        return route[::-1]


# =====================================================================
# BENCHMARK — run both approaches and compare time + peak memory
# =====================================================================
if __name__ == "__main__":
    # Test 1: official example 1 — linear chain, answer JFK→MUC→LHR→SFO→SJC.
    t1 = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    # Test 2: official example 2 — cycle around ATL/JFK/SFO.
    t2 = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    expected = [
        ["JFK", "MUC", "LHR", "SFO", "SJC"],
        ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"],
    ]

    def valid(route: Optional[List[str]], tickets: List[List[str]]) -> bool:
        # A correct itinerary: starts at JFK, uses every ticket once.
        if route is None or len(route) != len(tickets) + 1 or route[0] != "JFK":
            return False
        pool = [(a, b) for a, b in tickets]
        for i in range(1, len(route)):
            edge = (route[i - 1], route[i])
            if edge not in pool:
                return False
            pool.remove(edge)
        return True

    all_ok = True
    for idx, tickets in enumerate([t1, t2]):
        want = expected[idx]

        # --- Approach 1: recursive Hierholzer, time + peak memory ---
        tracemalloc.start()
        t0 = time.perf_counter()
        r1 = SolutionOne().findItinerary(tickets)
        t1_ = time.perf_counter()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # --- Approach 2: iterative Hierholzer ---
        tracemalloc.start()
        t0b = time.perf_counter()
        r2 = SolutionTwo().findItinerary(tickets)
        t1b = time.perf_counter()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        ok1 = valid(r1, tickets) and r1 == want
        ok2 = valid(r2, tickets) and r2 == want
        all_ok = all_ok and ok1 and ok2

        print(f"Test {idx+1} A1 (recursive): {r1}  {('PASS' if ok1 else 'FAIL')}  "
              f"time = {(t1_-t0)*1e6:.2f} us  peak = {peak1/1024:.1f} KB")
        print(f"Test {idx+1} A2 (iterative): {r2}  {('PASS' if ok2 else 'FAIL')}  "
              f"time = {(t1b-t0b)*1e6:.2f} us  peak = {peak2/1024:.1f} KB")

    print("PASS : both approaches reconstruct valid lexicographically-smallest itineraries."
          if all_ok else "FAIL : at least one answer is wrong.")