/*
 * =====================================================================
 * LeetCode 743 : Network Delay Time                                (Medium)
 * https://leetcode.com/problems/network-delay-time/
 * Category   : Advanced Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   n network nodes labelled 1..n. `times[i] = (u, v, w)` means a
 *   signal travels from u to v in w ms. A signal starts at node k and
 *   fans out along all edges simultaneously. Return the time it takes
 *   for ALL n nodes to receive the signal, or -1 if some node is
 *   unreachable from k.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Fans out along all edges" = each node receives the signal as soon
 *   as the SHORTEST path from k reaches it. So the answer is the
 *   maximum over all nodes of the shortest-path distance from k —
 *   a classic SINGLE-SOURCE SHORTEST PATHS (SSSP) problem. All edge
 *   weights are positive, which is exactly the setting Dijkstra was
 *   built for.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Dijkstra with a min-heap (BEST)
 *   dist[u] = best-known distance from k. Repeat: extract the node
 *   with the smallest dist (the min-heap gives that in O(log V)),
 *   "settle" it (its distance is now final), and relax each outgoing
 *   edge (u -> v, w): if dist[u] + w < dist[v], improve dist[v] and
 *   push it into the heap. Answer = max(dist[1..n]).
 *   Time  Complexity : O(E log V) — every edge relaxed once, each
 *                        heap op costs O(log V).
 *   Space Complexity : O(V + E)   — dist array + adjacency + heap.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Bellman-Ford (no heap, relax all edges V-1 times)
 *   Repeat V-1 rounds: scan every edge (u, v, w) and relax
 *   dist[v] = min(dist[v], dist[u] + w). After round i every node's
 *   dist is correct for all paths using at most i edges; V-1 rounds
 *   cover every simple path. Early-exit when a round changes nothing.
 *   Time  Complexity : O(V·E) — V-1 rounds × E edges each.
 *   Space Complexity : O(V)   — just the dist array.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why Dijkstra is correct, and what breaks it
 *   PROOF SKETCH (heap version): invariant — when a node u is popped,
 *   dist[u] is its TRUE shortest distance. Induction on pop order:
 *   u is the un-settled node with smallest dist; any alternative path
 *   k → ... → x → u must pass through some un-settled node x first
 *   (all settled nodes were already relaxed), and dist[x] >= dist[u],
 *   so that path costs >= dist[u] + (positive edges) > dist[u].
 *   Therefore no future relaxation can beat the current dist[u].
 *   NEGATIVE EDGES BREAK IT: with a negative edge, a later path
 *   k → ... → x → (negative edge) → u can cost LESS than dist[u]
 *   even when dist[x] > dist[u] — the settled-node argument collapses.
 *   Bellman-Ford handles negatives: relaxing every edge once per round
 *   propagates improvements one edge at a time, no settled-set needed.
 * =====================================================================
 */

#include <vector>          // std::vector — dist array / adjacency lists
#include <queue>           // std::priority_queue — the min-heap
#include <utility>         // std::pair — (distance, node) heap entries
#include <functional>      // std::greater — makes priority_queue a MIN-heap
#include <algorithm>       // std::max — tracking the answer
#include <chrono>          // std::chrono::steady_clock — benchmark timing
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

namespace {
const int INF = 1e9;  // sentinel "unreachable" distance (weights < 1000)
}

/* =====================================================================
 * APPROACH 1 : Dijkstra with a min-heap
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the time until the LAST node receives the
     *           signal (= max shortest distance from k), or -1 if
     *           some node is unreachable.
     * Inputs  : times — list of [u, v, w] directed edges.
     *           n     — number of nodes (labelled 1..n).
     *           k     — source node where the signal starts.
     * Output  : int — max shortest-path distance, or -1.
     */
    int networkDelayTime(const std::vector<std::vector<int>>& times, int n, int k) {
        // adjacency: g[u] = list of (v, w)
        std::vector<std::vector<std::pair<int, int>>> g(n + 1);
        for (const auto& t : times) {
            g[t[0]].emplace_back(t[1], t[2]);
        }

        // dist[u] = best-known shortest distance from k; INF = unseen.
        std::vector<int> dist(n + 1, INF);
        dist[k] = 0;

        // Min-heap of (distance, node): greater<> flips the default
        // max-heap so the SMALLEST distance sits on top.
        std::priority_queue<std::pair<int, int>,
                            std::vector<std::pair<int, int>>,
                            std::greater<std::pair<int, int>>> pq;
        pq.emplace(0, k);

        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();

            // Stale heap entry (u was improved after this push) — skip.
            // This lazy deletion keeps the heap simple and correct.
            if (d > dist[u]) continue;

            // u is now SETTLED: dist[u] is final (see proof in header).
            for (const auto& [v, w] : g[u]) {
                // Relaxation: is the detour through u cheaper than
                // what v already knows about itself?
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.emplace(dist[v], v);   // v may be improved again
                }
            }
        }

        // The last node to receive the signal = max over all nodes.
        int ans = 0;
        for (int i = 1; i <= n; ++i) {
            if (dist[i] == INF) return -1;    // unreachable node
            ans = std::max(ans, dist[i]);
        }
        return ans;
    }
};

/* =====================================================================
 * APPROACH 2 : Bellman-Ford (V-1 relaxation rounds)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Same result without any heap — relax every edge in
     *           V-1 rounds; each round extends paths by one edge.
     * Inputs  : times — list of [u, v, w] directed edges.
     *           n     — number of nodes (labelled 1..n).
     *           k     — source node where the signal starts.
     * Output  : int — max shortest-path distance, or -1.
     */
    int networkDelayTime(const std::vector<std::vector<int>>& times, int n, int k) {
        std::vector<int> dist(n + 1, INF);
        dist[k] = 0;

        // A simple path has at most n-1 edges → n-1 rounds suffice.
        for (int round = 1; round <= n - 1; ++round) {
            bool changed = false;
            for (const auto& t : times) {
                int u = t[0], v = t[1], w = t[2];
                // Relax every edge; only improve from reachable nodes.
                if (dist[u] != INF && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    changed = true;
                }
            }
            // No improvement → distances already final; stop early.
            if (!changed) break;
        }

        int ans = 0;
        for (int i = 1; i <= n; ++i) {
            if (dist[i] == INF) return -1;
            ans = std::max(ans, dist[i]);
        }
        return ans;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example 1 — 2 -> 3 -> 4 chain, answer 2.
    const std::vector<std::vector<int>> t1 = {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}};
    // Test 2: single edge, source reaches node 2 directly.
    const std::vector<std::vector<int>> t2 = {{1, 2, 1}};
    // Test 3: same edge but node 2 is NOT the source -> unreachable.
    const std::vector<std::vector<int>> t3 = {{1, 2, 1}};

    struct { const std::vector<std::vector<int>>& times; int n; int k; int want; } tests[] = {
        {t1, 4, 2, 2},
        {t2, 2, 1, 1},
        {t3, 2, 2, -1}
    };

    bool allOk = true;
    for (std::size_t i = 0; i < 3; ++i) {
        const auto& times = tests[i].times;
        int n = tests[i].n, k = tests[i].k, want = tests[i].want;

        // --- Approach 1: Dijkstra, timed + peak-RAM delta ---
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::steady_clock::now();
        int r1 = Solution_1().networkDelayTime(times, n, k);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;   // ru_maxrss is KB on Linux

        // --- Approach 2: Bellman-Ford ---
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::steady_clock::now();
        int r2 = Solution_2().networkDelayTime(times, n, k);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;

        bool ok1 = r1 == want;
        bool ok2 = r2 == want;
        allOk = allOk && ok1 && ok2;

        std::cout << "Test " << (i + 1) << " A1 (Dijkstra)   : " << r1
                  << "  " << (ok1 ? "PASS" : "FAIL") << "  time = " << us1
                  << " us  mem = " << kb1 << " KB\n";
        std::cout << "Test " << (i + 1) << " A2 (Bellman-Ford): " << r2
                  << "  " << (ok2 ? "PASS" : "FAIL") << "  time = " << us2
                  << " us  mem = " << kb2 << " KB\n";
    }

    std::cout << (allOk ? "PASS : both approaches match the expected delays."
                        : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}