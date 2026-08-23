/*
 * =====================================================================
 * LeetCode 261 : Graph Valid Tree                                 (Medium)
 * https://leetcode.com/problems/graph-valid-tree/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given n nodes labelled 0..n-1 and an edge list, decide whether
 *   the edges form a VALID TREE: connected AND acyclic. (An undirected
 *   graph with n nodes is a tree ⇔ it is connected and has exactly
 *   n−1 edges with no cycle.)
 * ---------------------------------------------------------------------
 * INTUITION
 *   Two cheap structural facts decide everything:
 *     • A connected acyclic graph on n nodes has EXACTLY n−1 edges.
 *     • If a graph with n−1 edges is acyclic it is automatically
 *       connected (components would need extra edges); conversely if
 *       it is connected and has n−1 edges it is automatically acyclic.
 *   So "valid tree" ⇔ no cycle AND n−1 edges ⇔ no cycle + count
 *   check. Cycle detection in an UNDIRECTED graph: union-find (an
 *   edge joining two already-merged nodes closes a cycle) or DFS
 *   with a visited set + parent argument (skip the edge that goes
 *   back to the parent).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Union-Find with path compression (BEST)
 *   Merge endpoints of every edge. If an edge's endpoints are ALREADY
 *   in the same set → cycle → invalid. Finally require exactly one
 *   component (or equivalently edges == n−1 AND no cycle).
 *   Time  Complexity : O(n + E·α(n))  — α(n) inverse Ackermann,
 *                        effectively constant.
 *   Space Complexity : O(n)           — parent + rank arrays.
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS from node 0
 *   Walk the graph once with a visited array. If we revisit a node
 *   that is not the parent → cycle. Then check all nodes visited
 *   (connected).
 *   Time  Complexity : O(n + E)   Space Complexity : O(n + E).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — union-find: path compression + rank
 *   parent[x] chains x to its component root. find() compresses the
 *   path (each hop flattens toward the root); union() attaches the
 *   smaller-rank root under the larger so trees stay shallow. With
 *   both optimisations the amortised cost is the INVERSE ACKERMANN
 *   function α(n) — growth so slow it is ≤ 4 for any practical n.
 *   Python dict/set hashing (open addressing, linear probing
 *   h(k,i)=(hash(k)+i) mod m) is NOT needed here — node labels are
 *   0..n−1, so plain arrays index directly.
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — edge list, adjacency
#include <string>           // std::string — printing helpers
#include <queue>            // std::queue — BFS/DFS frontier
#include <unordered_map>    // std::unordered_map — hash table (chaining)
#include <unordered_set>    // std::unordered_set — visited set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement
#include <functional>       // std::function — recursion-free DFS? no:
                            // iterative stack used instead

/* =====================================================================
 * APPROACH 1 : Union-Find — any edge closing a cycle kills the tree
 * ===================================================================== */
class Solution_1 {
private:
    // find with PATH COMPRESSION: walk to root, then flatten the whole
    // chain in one backward pass.
    int find(std::vector<int>& parent, int x) {
        if (parent[x] != x) parent[x] = find(parent, x);
        return parent[x];
    }

    // union by rank: attach the shorter tree under the taller root so
    // find() stays near-O(1) amortised.
    bool unite(std::vector<int>& parent, std::vector<int>& rank, int a, int b) {
        int ra = find(parent, a);
        int rb = find(parent, b);
        if (ra == rb) return false;   // already same set → edge closes
                                       // a cycle → tree invalid
        if (rank[ra] < rank[rb]) parent[ra] = rb;
        else if (rank[ra] > rank[rb]) parent[rb] = ra;
        else {
            parent[rb] = ra;          // equal ranks: attach + bump one
            ++rank[ra];
        }
        return true;
    }

public:
    /*
     * Purpose : Decide whether the edges form a valid tree.
     * Inputs  : n — node count; edges — undirected edge list.
     * Output  : bool — true iff connected and acyclic.
     */
    bool validTree(int n, const std::vector<std::vector<int>>& edges) {
        // Tree on n nodes needs exactly n−1 edges — cheap early reject.
        if (static_cast<int>(edges.size()) != n - 1) return false;

        std::vector<int> parent(n);
        std::vector<int> rank(n, 0);
        for (int i = 0; i < n; ++i) parent[i] = i;  // every node is its
                                                    // own component

        int components = n;   // each successful merge lowers the count
        for (const auto& e : edges) {
            if (!unite(parent, rank, e[0], e[1])) return false;  // cycle
            --components;
        }
        // With n−1 successful merges all nodes share one component.
        return components == 1;
    }
};

/* =====================================================================
 * APPROACH 2 : DFS from node 0 — cycle + connectivity in one walk
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether the edges form a valid tree.
     * Inputs  : n — node count; edges — undirected edge list.
     * Output  : bool — true iff connected and acyclic.
     */
    bool validTree(int n, const std::vector<std::vector<int>>& edges) {
        if (static_cast<int>(edges.size()) != n - 1) return false;

        // Adjacency list of the undirected graph.
        std::vector<std::vector<int>> adj(n);
        for (const auto& e : edges) {
            adj[e[0]].push_back(e[1]);
            adj[e[1]].push_back(e[0]);
        }

        // Iterative DFS with (node, parent) stack. In an undirected
        // graph the ONLY way to revisit a node is (a) its parent via
        // the edge we came from — legal — or (b) a genuine cycle.
        std::vector<bool> visited(n, false);
        std::vector<std::pair<int, int>> stack;
        stack.push_back({0, -1});
        visited[0] = true;
        int seen = 1;

        while (!stack.empty()) {
            auto [node, parent] = stack.back();
            stack.pop_back();
            for (int nb : adj[node]) {
                if (nb == parent) continue;   // the edge we came on
                if (visited[nb]) return false; // back edge → cycle
                visited[nb] = true;
                ++seen;
                stack.push_back({nb, node});
            }
        }
        // Cycle-free AND every node reached → connected → valid tree.
        return seen == n;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 official-style tests
 * ===================================================================== */
int main() {
    // Test 1 (official): 5, [[0,1],[0,2],[0,3],[1,4]] → true.
    // Test 2 (official): 5, [[0,1],[1,2],[2,3],[1,3],[1,4]] → false
    //   (cycle 1-2-3-1).
    // Test 3: 4, [[0,1],[2,3]] → false (disconnected).
    struct { int n; std::vector<std::vector<int>> edges; bool expected; } tests[] = {
        {5, {{0, 1}, {0, 2}, {0, 3}, {1, 4}}, true},
        {5, {{0, 1}, {1, 2}, {2, 3}, {1, 3}, {1, 4}}, false},
        {4, {{0, 1}, {2, 3}}, false}
    };

    bool allPass = true;
    for (int t = 0; t < 3; ++t) {
        // --- Approach 1 timing + memory ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto s1 = std::chrono::high_resolution_clock::now();
        bool r1 = Solution_1().validTree(tests[t].n, tests[t].edges);
        auto e1_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);

        // --- Approach 2 timing + memory ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto s2 = std::chrono::high_resolution_clock::now();
        bool r2 = Solution_2().validTree(tests[t].n, tests[t].edges);
        auto e2_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);

        long mem1 = (after1.ru_maxrss - before1.ru_maxrss);
        long mem2 = (after2.ru_maxrss - before2.ru_maxrss);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1_ - s1).count() / 1000.0;
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2_ - s2).count() / 1000.0;

        bool ok = r1 == tests[t].expected && r2 == tests[t].expected && r1 == r2;
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << (ok ? " PASS" : " FAIL")
                  << " | A1=" << (r1 ? "true" : "false") << " (expect " << (tests[t].expected ? "true" : "false") << ")"
                  << "  time=" << us1 << " µs  mem=" << mem1 << " KB"
                  << " | A2=" << (r2 ? "true" : "false") << "  time=" << us2 << " µs  mem=" << mem2 << " KB\n";
    }
    std::cout << (allPass ? "PASS : all tests green on both approaches.\n"
                          : "FAIL : at least one test/approach disagrees.\n");
    return 0;
}