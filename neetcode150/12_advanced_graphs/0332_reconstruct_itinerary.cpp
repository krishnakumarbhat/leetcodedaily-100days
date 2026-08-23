/*
 * =====================================================================
 * LeetCode 332 : Reconstruct Itinerary                              (Hard)
 * https://leetcode.com/problems/reconstruct-itinerary/
 * Category   : Advanced Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a list of airline tickets [from, to], rebuild the itinerary
 *   in order. The trip MUST start at "JFK" and use EVERY ticket
 *   exactly once. When several itineraries exist, return the one that
 *   is lexicographically smallest as a list of airport codes.
 *   (The input is guaranteed to form at least one valid itinerary.)
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every airport is a vertex, every ticket is a directed edge, and we
 *   must traverse EVERY edge exactly once — that is an EULERIAN PATH.
 *   The guarantee "every ticket used once" means the graph is already
 *   Eulerian, so the problem reduces to: walk all edges exactly once,
 *   and break ties by always taking the lexicographically smallest
 *   next airport. Hierholzer's algorithm does exactly that.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Hierholzer's algorithm, recursive DFS (BEST)
 *   Build adjacency: map airport -> sorted destinations. To always pick
 *   the SMALLEST unused destination, store destinations descending and
 *   pop from the back. DFS: while the current airport still has unused
 *   tickets, follow one (smallest), recurse, and only AFTER all edges
 *   of the current node are consumed append the node to `route`.
 *   Finally REVERSE `route` — the post-order trick that turns the
 *   walk into the correct itinerary.
 *   Time  Complexity : O(E log E) — E tickets; sorting each adjacency
 *                        list dominates (E = number of tickets).
 *   Space Complexity : O(E)       — adjacency lists + route storage.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Hierholzer's algorithm, iterative (no recursion)
 *   Same idea with an explicit stack, so deep graphs cannot overflow
 *   the call stack. When the top airport has unused tickets we descend
 *   (push next); otherwise we close it out (append to route, pop).
 *   The reversal at the end is identical.
 *   Time  Complexity : O(E log E)   Space Complexity : O(E)
 * ---------------------------------------------------------------------
 * DEEP DIVE — Hierholzer's algorithm and why reversal works
 *   An Eulerian path exists iff every vertex with edges has balanced
 *   in/out degree except possibly one start (out = in + 1) and one end
 *   (in = out + 1). The problem guarantees this, so naive DFS "walks
 *   into a dead end" only when the remaining edges form cycles; those
 *   cycles are appended to the route at the moment the dead end is
 *   reached. Reversing the post-order list interleaves every cycle
 *   back into the walk at exactly the vertex where it was entered —
 *   this is the "edge-splitting" proof: each vertex's cycle is a
 *   sub-tour that plugs into the vertex's slot. Every edge is traversed
 *   exactly once, total O(E).
 *   C++ note: std::map keeps airports sorted (red-black tree, O(log V)
 *   per op) — that gives us lexicographic adjacency for free.
 * =====================================================================
 */

#include <vector>          // std::vector — ticket list / route storage
#include <string>          // std::string — airport codes
#include <map>             // std::map — sorted adjacency (lexicographic)
#include <algorithm>       // std::sort / std::reverse — sort dsts, flip route
#include <chrono>          // std::chrono::steady_clock — benchmark timing
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Hierholzer's algorithm, recursive DFS
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the lexicographically smallest Eulerian path
     *           that starts at "JFK" and uses every ticket once.
     * Inputs  : tickets — list of [from, to] airport-code pairs.
     * Output  : vector<string> — the ordered itinerary.
     */
    std::vector<std::string> findItinerary(const std::vector<std::vector<std::string>>& tickets) {
        // adj : airport -> destinations sorted DESCENDING so that the
        //       lexicographically smallest is at the back() we pop.
        adj_.clear();
        route_.clear();
        for (const auto& t : tickets) {
            adj_[t[0]].push_back(t[1]);
        }
        for (auto& kv : adj_) {
            std::sort(kv.second.rbegin(), kv.second.rend());
        }

        // Post-order DFS: only when ALL edges of an airport are used do
        // we append the airport to the route.
        dfs("JFK");

        // The post-order walk is the itinerary read backwards.
        std::reverse(route_.begin(), route_.end());
        return route_;
    }

private:
    // adjacency: airport -> remaining destinations (descending order)
    std::map<std::string, std::vector<std::string>> adj_;
    // route: built in post-order, reversed by the caller
    std::vector<std::string> route_;

    /*
     * Purpose : Hierholzer DFS — consume every outgoing edge of
     *           `airport`, then append the airport (post-order).
     * Inputs  : airport — current vertex being drained.
     * Output  : none (fills route_).
     */
    void dfs(const std::string& airport) {
        // Keep following the smallest unused ticket. The loop only ends
        // when this airport's edges are exhausted (or it has none).
        while (!adj_[airport].empty()) {
            // back() holds the lexicographically smallest destination
            // because the list was sorted descending.
            std::string next = adj_[airport].back();
            adj_[airport].pop_back();   // ticket consumed — never reused
            dfs(next);
        }
        // All outgoing edges of `airport` are used → close it out.
        route_.push_back(airport);
    }
};

/* =====================================================================
 * APPROACH 2 : Hierholzer's algorithm, iterative (explicit stack)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Same Eulerian path, no recursion — an explicit stack
     *           replaces the call stack so deep graphs are safe.
     * Inputs  : tickets — list of [from, to] airport-code pairs.
     * Output  : vector<string> — the ordered itinerary.
     */
    std::vector<std::string> findItinerary(const std::vector<std::vector<std::string>>& tickets) {
        // Same descending adjacency as approach 1.
        std::map<std::string, std::vector<std::string>> adj;
        for (const auto& t : tickets) {
            adj[t[0]].push_back(t[1]);
        }
        for (auto& kv : adj) {
            std::sort(kv.second.rbegin(), kv.second.rend());
        }

        // stack simulates the DFS recursion; route is the post-order list.
        std::vector<std::string> stack;
        std::vector<std::string> route;
        stack.push_back("JFK");

        while (!stack.empty()) {
            const std::string top = stack.back();
            // If the top airport still has unused tickets, descend into
            // its smallest destination (same rule as the recursive DFS).
            auto it = adj.find(top);
            if (it != adj.end() && !it->second.empty()) {
                std::string next = it->second.back();
                it->second.pop_back();
                stack.push_back(next);
            } else {
                // Dead end reached: all edges of `top` are used.
                route.push_back(top);
                stack.pop_back();
            }
        }

        std::reverse(route.begin(), route.end());
        return route;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — a long linear chain of 4 tickets.
    const std::vector<std::vector<std::string>> t1 = {
        {"MUC", "LHR"}, {"JFK", "MUC"}, {"SFO", "SJC"}, {"LHR", "SFO"}
    };
    // Test 2: official example 2 — a cycle wrapped around ATL/JFK/SFO.
    const std::vector<std::vector<std::string>> t2 = {
        {"JFK", "SFO"}, {"JFK", "ATL"}, {"SFO", "ATL"},
        {"ATL", "JFK"}, {"ATL", "SFO"}
    };
    const std::vector<std::vector<std::vector<std::string>>> tests = {t1, t2};
    // Expected answers, used by the PASS/FAIL checker.
    const std::vector<std::vector<std::string>> expected = {
        {"JFK", "MUC", "LHR", "SFO", "SJC"},
        {"JFK", "ATL", "JFK", "SFO", "ATL", "SFO"}
    };

    bool allOk = true;
    for (std::size_t ti = 0; ti < tests.size(); ++ti) {
        const auto& tickets = tests[ti];
        const auto& want = expected[ti];

        // --- Approach 1: recursive Hierholzer, timed + mem delta ---
        struct rusage b1, a1;
        getrusage(RUSAGE_SELF, &b1);
        auto s1 = std::chrono::steady_clock::now();
        std::vector<std::string> r1 = Solution_1().findItinerary(tickets);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a1);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000.0;
        long kb1 = a1.ru_maxrss - b1.ru_maxrss;   // ru_maxrss is KB on Linux

        // --- Approach 2: iterative Hierholzer ---
        struct rusage b2, a2;
        getrusage(RUSAGE_SELF, &b2);
        auto s2 = std::chrono::steady_clock::now();
        std::vector<std::string> r2 = Solution_2().findItinerary(tickets);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &a2);
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000.0;
        long kb2 = a2.ru_maxrss - b2.ru_maxrss;

        // --- Verify: correct length, starts at JFK, uses each ticket ---
        auto valid = [&](const std::vector<std::string>& r) {
            if (r.size() != tickets.size() + 1 || r.empty() || r[0] != "JFK") return false;
            std::multimap<std::string, std::string> pool;
            for (const auto& t : tickets) pool.insert({t[0], t[1]});
            for (std::size_t i = 1; i < r.size(); ++i) {
                auto it = pool.find(r[i - 1]);
                bool found = false;
                for (; it != pool.end() && it->first == r[i - 1]; ++it) {
                    if (it->second == r[i]) { pool.erase(it); found = true; break; }
                }
                if (!found) return false;
            }
            return true;
        };
        bool ok1 = valid(r1) && r1 == want;
        bool ok2 = valid(r2) && r2 == want;
        allOk = allOk && ok1 && ok2;

        std::cout << "Test " << (ti + 1) << " A1 (recursive): [";
        for (std::size_t i = 0; i < r1.size(); ++i) std::cout << (i ? ",\"" : "\"") << r1[i] << "\"";
        std::cout << "]  " << (ok1 ? "PASS" : "FAIL") << "  time = " << us1 << " us  mem = " << kb1 << " KB\n";
        std::cout << "Test " << (ti + 1) << " A2 (iterative): [";
        for (std::size_t i = 0; i < r2.size(); ++i) std::cout << (i ? ",\"" : "\"") << r2[i] << "\"";
        std::cout << "]  " << (ok2 ? "PASS" : "FAIL") << "  time = " << us2 << " us  mem = " << kb2 << " KB\n";
    }

    std::cout << (allOk ? "PASS : both approaches reconstruct valid lexicographically-smallest itineraries."
                        : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}