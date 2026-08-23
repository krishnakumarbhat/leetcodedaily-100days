/*
 * =====================================================================
 * LeetCode 1584 : Min Cost to Connect All Points                   (Medium)
 * https://leetcode.com/problems/min-cost-to-connect-all-points/
 * Category   : Advanced Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given n points on a plane, connect ALL points with a network of
 *   edges (a spanning tree) so that every point can reach every other.
 *   Edge cost between two points = Manhattan distance |x1-x2|+|y1-y2|.
 *   Return the MINIMUM total cost — i.e. the Minimum Spanning Tree
 *   (MST) weight of the complete graph on the points.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Connect every node, cheapest total" is the textbook definition
 *   of an MST. The graph is COMPLETE (any two points can connect), so
 *   we have n·(n-1)/2 edges available but only n-1 are needed. Two
 *   classical algorithms: grow one tree outward (Prim) or merge trees
 *   by cheapest edge (Kruskal).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Prim's algorithm with a heap (BEST for dense graphs)
 *   minCost[v] = cheapest edge from the tree-so-far to point v.
 *   Start with point 0 in the tree (minCost[0] = 0). Repeat n times:
 *   extract the unvisited point with the smallest minCost (heap), add
 *   its cost to the total, mark it visited, and refresh minCost for
 *   every unvisited neighbour. Each point is extracted exactly once.
 *   Time  Complexity : O(n² log n) — complete graph: n extractions,
 *                        each relaxes n-1 neighbours at O(log n) each.
 *   Space Complexity : O(n)        — minCost + heap + visited flags.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Kruskal's algorithm + union-find
 *   Generate ALL n(n-1)/2 edges with their costs, sort by cost, then
 *   walk the sorted list: take an edge only if its endpoints are in
 *   DIFFERENT components (union-find decides in ~O(α(n))); stop after
 *   n-1 edges (a spanning tree is complete).
 *   Time  Complexity : O(n² log n) — dominated by sorting E = n² edges.
 *   Space Complexity : O(n²)       — the edge list itself.
 * ---------------------------------------------------------------------
 * DEEP DIVE — Prim vs Kruskal, and why each is safe
 *   PRIM (cut property): take any cut separating the growing tree from
 *   the rest; the CHEAPEST edge across that cut is in some MST, so
 *   greedily adding the cheapest crossing edge can never go wrong.
 *   The heap makes "cheapest crossing edge" an O(log n) pop.
 *   KRUSKAL (cycle property): the cheapest edge not creating a cycle
 *   is always safe to keep; union-find detects "would create a cycle"
 *   by checking whether the endpoints already share a root. Both are
 *   correct because every edge crossing a cut is a candidate — the
 *   complete graph simply makes n² candidates explicit.
 *   When to use which: Prim shines on DENSE graphs (like this one,
 *   E ≈ n²) since it only scans edges of the frontier; Kruskal shines
 *   on SPARSE graphs (E ≈ n) and when edges are given explicitly.
 * =====================================================================
 */

#include <vector>          // std::vector — points / edges / DSU internals
#include <queue>           // std::priority_queue — the min-heap
#include <utility>         // std::pair — (cost, node) heap entries
#include <functional>      // std::greater — MIN-heap ordering
#include <algorithm>       // std::sort — Kruskal's edge ordering
#include <tuple>           // std::tuple — (cost, u, v) edge records
#include <chrono>          // std::chrono::steady_clock — benchmark timing
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

namespace {
const int INF = 1e9;  // sentinel "no edge known yet" cost

// Manhattan distance between two points — the edge weight.
int manhattan(const std::vector<int>& a, const std::vector<int>& b) {
    return std::abs(a[0] - b[0]) + std::abs(a[1] - b[1]);
}
}

/* =====================================================================
 * APPROACH 1 : Prim's algorithm with a min-heap
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the minimum total cost of a spanning tree over
     *           the given points (Manhattan weights, complete graph).
     * Inputs  : points — list of [x, y] coordinates.
     * Output  : int — MST total cost.
     */
    int minCostConnectPoints(const std::vector<std::vector<int>>& points) {
        const int n = static_cast<int>(points.size());

        std::vector<bool> inMST(n, false);   // visited / settled set
        std::vector<int> minCost(n, INF);    // cheapest edge to tree
        minCost[0] = 0;                      // seed the tree at point 0

        // Min-heap of (cost, point); point 0 enters with cost 0.
        std::priority_queue<std::pair<int, int>,
                            std::vector<std::pair<int, int>>,
                            std::greater<std::pair<int, int>>> pq;
        pq.emplace(0, 0);

        int total = 0;
        while (!pq.empty()) {
            const auto [cost, u] = pq.top();
            pq.pop();

            // u already joined the tree via a cheaper edge — skip.
            if (inMST[u]) continue;

            inMST[u] = true;      // settle u: its cheapest cut edge is
            total += cost;        // final (cut property — see header).

            // Refresh every unvisited neighbour's cheapest tree edge.
            for (int v = 0; v < n; ++v) {
                if (inMST[v]) continue;
                const int d = manhattan(points[u], points[v]);
                if (d < minCost[v]) {
                    minCost[v] = d;
                    pq.emplace(d, v);   // v's best edge just improved
                }
            }
        }
        return total;
    }
};

/* =====================================================================
 * APPROACH 2 : Kruskal's algorithm + union-find
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Same MST cost, generated from a sorted edge list and
     *           merged components via union-find.
     * Inputs  : points — list of [x, y] coordinates.
     * Output  : int — MST total cost.
     */
    int minCostConnectPoints(const std::vector<std::vector<int>>& points) {
        const int n = static_cast<int>(points.size());

        // Materialize ALL n(n-1)/2 edges of the complete graph.
        std::vector<std::tuple<int, int, int>> edges;
        edges.reserve(n * (n - 1) / 2);
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                edges.emplace_back(manhattan(points[i], points[j]), i, j);
            }
        }
        // Sort ascending by cost — the greedy order (cycle property).
        std::sort(edges.begin(), edges.end());

        DSU dsu(n);
        int total = 0;
        int used = 0;
        for (const auto& [w, u, v] : edges) {
            // Adding u-v is safe only if u and v are not yet connected.
            if (dsu.unite(u, v)) {
                total += w;
                if (++used == n - 1) break;   // spanning tree complete
            }
        }
        return total;
    }

private:
    /* Disjoint-set union with path compression + union by rank. */
    class DSU {
    public:
        explicit DSU(int size) : parent_(size), rank_(size, 0) {
            for (int i = 0; i < size; ++i) parent_[i] = i;
        }
        // Find root, flattening the path on the way up.
        int find(int x) {
            if (parent_[x] != x) parent_[x] = find(parent_[x]);
            return parent_[x];
        }
        // Merge two components; false if they were already one.
        bool unite(int a, int b) {
            const int ra = find(a);
            const int rb = find(b);
            if (ra == rb) return false;
            if (rank_[ra] < rank_[rb]) {
                parent_[ra] = rb;
            } else {
                parent_[rb] = ra;
                if (rank_[ra] == rank_[rb]) ++rank_[ra];
            }
            return true;
        }
    private:
        std::vector<int> parent_;
        std::vector<int> rank_;
    };
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example 1 — answer 20.
    const std::vector<std::vector<int>> p1 = {{0, 0}, {2, 2}, {3, 10}, {5, 2}, {7, 0}};
    // Test 2: official example 2 — answer 18.
    const std::vector<std::vector<int>> p2 = {{3, 12}, {-2, 5}, {-4, 1}};
    // Test 3: square — three unit edges, answer 4.
    const std::vector<std::vector<int>> p3 = {{0, 0}, {1, 1}, {1, 0}, {-1, 1}};

    struct { const std::vector<std::vector<int>>& p; int want; } tests[] = {
        {p1, 20}, {p2, 18}, {p3, 4}
    };

    bool allOk = true;
    for (std::size_t i = 0; i < 3; ++i) {
        const auto& points = tests[i].p;
        const int want = tests[i].want;

        // --- Approach 1: Prim + heap ---
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::steady_clock::now();
        int r1 = Solution_1().minCostConnectPoints(points);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;

        // --- Approach 2: Kruskal + union-find ---
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::steady_clock::now();
        int r2 = Solution_2().minCostConnectPoints(points);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;

        bool ok1 = r1 == want;
        bool ok2 = r2 == want;
        allOk = allOk && ok1 && ok2;

        std::cout << "Test " << (i + 1) << " A1 (Prim + heap)   : " << r1
                  << "  " << (ok1 ? "PASS" : "FAIL") << "  time = " << us1
                  << " us  mem = " << kb1 << " KB\n";
        std::cout << "Test " << (i + 1) << " A2 (Kruskal + DSU) : " << r2
                  << "  " << (ok2 ? "PASS" : "FAIL") << "  time = " << us2
                  << " us  mem = " << kb2 << " KB\n";
    }

    std::cout << (allOk ? "PASS : both approaches match the expected MST costs."
                        : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}