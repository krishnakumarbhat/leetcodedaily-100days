/*
 * =====================================================================
 * LeetCode 787 : Cheapest Flights Within K Stops                   (Medium)
 * https://leetcode.com/problems/cheapest-flights-within-k-stops/
 * Category   : Advanced Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   n cities, flights[i] = (from, to, price) — directed. Find the
 *   cheapest price from `src` to `dst` using at most `k` intermediate
 *   stops (i.e. a path of at most k+1 edges), or -1 if none exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   We want the cheapest path under a HOP BUDGET, not the globally
 *   cheapest path. Plain Dijkstra is the wrong tool: the cheapest
 *   route to a node can use many hops, while the budget forces us to
 *   trade price against hop count. Two tools handle this:
 *   (1) Bellman-Ford, whose rounds are EXACTLY hop-count rounds, and
 *   (2) Dijkstra with hop count carried as part of the state.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bellman-Ford with k+1 relaxations (BEST)
 *   dist[u] = best price from src using the hops relaxed so far.
 *   Repeat k+1 times: relax every flight from a SNAPSHOT copy of dist.
 *   Round i incorporates exactly the paths using at most i edges, so
 *   after round k+1 we have all paths with <= k stops.
 *   Time  Complexity : O(k·E)   — (k+1) rounds × E flights each.
 *   Space Complexity : O(V)     — one dist array (+ one snapshot).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Dijkstra with stop-count state
 *   Push (price, city, stops) triples on a min-heap ordered by price.
 *   Pop the cheapest; if it is `dst`, return immediately (heap order
 *   guarantees no cheaper feasible trip remains). Prune with
 *   bestStops[u]: if we already reached u with <= stops, skip —
 *   that arrival dominates (same or lower price, more budget left).
 *   Time  Complexity : O(E log V) typical — each edge may push once
 *                        per distinct stop count reaching its head.
 *   Space Complexity : O(V + E)   — graph + heap + prune array.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why k+1 relaxations, not k
 *   A trip with k intermediate stops uses k+1 flight legs. Bellman-
 *   Ford's i-th round computes optimal prices for paths of AT MOST i
 *   edges, because each round extends every previously known path by
 *   exactly one more edge. The SNAPSHOT copy is the subtle part: if
 *   we relaxed in-place, one round could chain two edges (u->v then
 *   v->w) and silently count two legs as one — exceeding the budget.
 *   So: k stops ⇔ k+1 edges ⇔ k+1 rounds. For the same reason, plain
 *   Dijkstra fails here: it settles each node once with the cheapest
 *   price, but that price may spend the whole hop budget, blocking a
 *   slightly pricier but fewer-hop route to the destination.
 * =====================================================================
 */

#include <vector>          // std::vector — graph / dist arrays
#include <queue>           // std::priority_queue — the min-heap
#include <utility>         // std::pair — nested heap entries
#include <functional>      // std::greater — MIN-heap ordering
#include <chrono>          // std::chrono::steady_clock — benchmark timing
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

namespace {
const int INF = 1e9;  // sentinel "unreachable" price
}

/* =====================================================================
 * APPROACH 1 : Bellman-Ford with k+1 relaxations
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the cheapest price from src to dst using at
     *           most k stops, or -1 when no such trip exists.
     * Inputs  : n       — number of cities (0..n-1).
     *           flights — list of [from, to, price] directed flights.
     *           src, dst, k — start, target, max intermediate stops.
     * Output  : int — cheapest price, or -1.
     */
    int findCheapestPrice(int n, const std::vector<std::vector<int>>& flights,
                          int src, int dst, int k) {
        std::vector<int> dist(n, INF);
        dist[src] = 0;

        // k stops ⇔ at most k+1 flight legs ⇔ k+1 relaxation rounds.
        for (int round = 0; round <= k; ++round) {
            // SNAPSHOT: round i may only extend round i-1 results.
            // Relaxing in-place could chain two legs in one round and
            // silently exceed the stop budget.
            std::vector<int> next = dist;
            for (const auto& f : flights) {
                const int u = f[0], v = f[1], w = f[2];
                // Extend an old path by one leg: u -> v.
                if (dist[u] != INF && dist[u] + w < next[v]) {
                    next[v] = dist[u] + w;
                }
            }
            dist.swap(next);
        }

        return dist[dst] == INF ? -1 : dist[dst];
    }
};

/* =====================================================================
 * APPROACH 2 : Dijkstra with stop count carried in the state
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Same answer via a Dijkstra whose heap entries carry
     *           (price, city, stops) and prune dominated arrivals.
     * Inputs  : n, flights, src, dst, k — as in approach 1.
     * Output  : int — cheapest price, or -1.
     */
    int findCheapestPrice(int n, const std::vector<std::vector<int>>& flights,
                          int src, int dst, int k) {
        // adjacency: g[u] = list of (v, price)
        std::vector<std::vector<std::pair<int, int>>> g(n);
        for (const auto& f : flights) {
            g[f[0]].emplace_back(f[1], f[2]);
        }

        // Min-heap of (price, city, stops); pair<price, pair<city, stops>>
        // orders by price first — exactly the Dijkstra invariant.
        std::priority_queue<std::pair<int, std::pair<int, int>>,
                            std::vector<std::pair<int, std::pair<int, int>>>,
                            std::greater<std::pair<int, std::pair<int, int>>>> pq;
        pq.emplace(0, std::make_pair(src, 0));

        // bestStops[u] = fewest stops with which u was ever reached.
        // A later arrival with >= stops is dominated and prunable.
        std::vector<int> bestStops(n, INF);

        while (!pq.empty()) {
            const auto top = pq.top();
            pq.pop();
            const int price = top.first;
            const int u = top.second.first;
            const int stops = top.second.second;

            // First time dst is popped = cheapest feasible trip found,
            // because the heap always pops the smallest price first.
            if (u == dst) return price;

            // Budget exhausted, or a dominating arrival already seen.
            if (stops > k) continue;
            if (bestStops[u] <= stops) continue;
            bestStops[u] = stops;

            // Take one more flight; hop budget shrinks by one.
            for (const auto& [v, w] : g[u]) {
                pq.emplace(price + w, std::make_pair(v, stops + 1));
            }
        }
        return -1;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example 1 — 0->1->2->3 chain vs 0->2 shortcut;
    // with 1 stop, 0->2->3 (600) beats 0->1->2->3 (900) and 0->2 is
    // only a 1-stop prefix of it. Cheapest: 0->1->2->3 = 300? No —
    // with k=1 the only 2-leg routes are 0->1->2 (200) and 0->2->3
    // (600); dst=3 needs 0->2->3 = 600. Expected: 600.
    const std::vector<std::vector<int>> f1 = {
        {0, 1, 100}, {1, 2, 100}, {2, 3, 100}, {0, 2, 500}
    };
    // Test 2: official example 2 — 0->1->2 = 200 with 1 stop.
    const std::vector<std::vector<int>> f2 = {
        {0, 1, 100}, {1, 2, 100}, {0, 2, 500}
    };
    // Test 3: same graph but zero stops allowed — only the direct
    // flight 0->2 (500) fits the budget.
    const std::vector<std::vector<int>> f3 = f2;

    struct { int n; const std::vector<std::vector<int>>& f; int src; int dst; int k; int want; } tests[] = {
        {4, f1, 0, 3, 1, 600},
        {3, f2, 0, 2, 1, 200},
        {3, f3, 0, 2, 0, 500}
    };

    bool allOk = true;
    for (std::size_t i = 0; i < 3; ++i) {
        const int n = tests[i].n;
        const auto& f = tests[i].f;
        const int src = tests[i].src, dst = tests[i].dst, k = tests[i].k;
        const int want = tests[i].want;

        // --- Approach 1: Bellman-Ford with k+1 rounds ---
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::steady_clock::now();
        int r1 = Solution_1().findCheapestPrice(n, f, src, dst, k);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;

        // --- Approach 2: Dijkstra with stop-count state ---
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::steady_clock::now();
        int r2 = Solution_2().findCheapestPrice(n, f, src, dst, k);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;

        bool ok1 = r1 == want;
        bool ok2 = r2 == want;
        allOk = allOk && ok1 && ok2;

        std::cout << "Test " << (i + 1) << " A1 (Bellman-Ford k+1): " << r1
                  << "  " << (ok1 ? "PASS" : "FAIL") << "  time = " << us1
                  << " us  mem = " << kb1 << " KB\n";
        std::cout << "Test " << (i + 1) << " A2 (Dijkstra + stops) : " << r2
                  << "  " << (ok2 ? "PASS" : "FAIL") << "  time = " << us2
                  << " us  mem = " << kb2 << " KB\n";
    }

    std::cout << (allOk ? "PASS : both approaches match the expected prices."
                        : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}