/*
 * =====================================================================
 * LeetCode 210 : Course Schedule II                                (Medium)
 * https://leetcode.com/problems/course-schedule-ii/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Same setup as 207, but now RETURN one valid order of taking all
 *   `numCourses` courses, or an empty array if a cycle makes it
 *   impossible.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The order asked for is a TOPOLOGICAL ORDER: an ordering where
 *   every prerequisite edge a → b puts b before a. Kahn's algorithm
 *   produces it naturally — the order courses leave the ready queue.
 *   DFS produces the REVERSE of finish time — prepending each node
 *   when it is marked "done" yields a valid topological order.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Kahn's algorithm (BEST)
 *   In-degree array + queue of "ready" courses; dequeue order IS the
 *   answer. Fewer than n courses output ⇒ cycle ⇒ return {}.
 *   Time  Complexity : O(V + E)  — every edge scanned once.
 *   Space Complexity : O(V + E)  — adjacency + order.
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS (post-order prepending)
 *   Colour DFS; when a node finishes (colour 2) prepend it to the
 *   answer. Detecting a back edge aborts with an empty array.
 *   Time  Complexity : O(V + E)   Space Complexity : O(V + E).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — Kahn's vs DFS for topological sort
 *   Kahn's: BFS-like, iterative, naturally produces the order; the
 *   in-degree array is itself the "remaining dependencies" book.
 *   DFS: recursion; the trick is that finish-time REVERSE order is
 *   topological — children always finish before their parent, so
 *   prepending on exit keeps parents first. Both O(V+E); Kahn's has
 *   no recursion-depth risk and handles disconnected graphs in the
 *   same pass.
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — adjacency lists + order
#include <string>           // std::string — order formatting
#include <queue>            // std::queue — Kahn's ready queue
#include <unordered_map>    // std::unordered_map — hash table (chaining)
#include <unordered_set>    // std::unordered_set — visited set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement
#include <algorithm>        // std::reverse — DFS finish-time reversal

/* =====================================================================
 * APPROACH 1 : Kahn's algorithm — dequeue order IS the answer
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return one valid order to take all courses.
     * Inputs  : numCourses — number of courses.
     *           prerequisites — [a, b] pairs: a needs b first.
     * Output  : vector<int> — topological order, empty if cyclic.
     */
    std::vector<int> findOrder(int numCourses, const std::vector<std::vector<int>>& prerequisites) {
        std::vector<std::vector<int>> adj(numCourses);
        std::vector<int> indegree(numCourses, 0);
        for (const auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);  // edge b → a : finish b before a
            ++indegree[p[0]];           // a gains one unsatisfied prereq
        }

        // Ready queue: courses with no unsatisfied prerequisites.
        std::queue<int> q;
        for (int i = 0; i < numCourses; ++i) {
            if (indegree[i] == 0) q.push(i);
        }

        // The dequeue order is a valid topological order.
        std::vector<int> order;
        order.reserve(numCourses);
        while (!q.empty()) {
            int course = q.front();
            q.pop();
            order.push_back(course);
            // Unblock dependents whose prerequisites are all done.
            for (int dep : adj[course]) {
                if (--indegree[dep] == 0) q.push(dep);
            }
        }
        // Cycle → some course never became ready → order is short.
        return order.size() == static_cast<size_t>(numCourses) ? order : std::vector<int>{};
    }
};

/* =====================================================================
 * APPROACH 2 : DFS — prepend on finish (reverse of finish time)
 * ===================================================================== */
class Solution_2 {
private:
    std::vector<std::vector<int>> adj_;
    std::vector<int> colour_;   // 0 unvisited, 1 on stack, 2 done
    std::vector<int> order_;    // topological order, built backwards

    /*
     * Purpose : DFS-walk from v; on finish, prepend v to order_.
     * Inputs  : v — course to explore.
     * Output  : bool — false iff a cycle was found.
     */
    bool dfs(int v) {
        if (colour_[v] == 1) return false;  // back edge → cycle
        if (colour_[v] == 2) return true;   // already done
        colour_[v] = 1;
        for (int nb : adj_[v]) {
            if (!dfs(nb)) return false;
        }
        colour_[v] = 2;
        // Children finished BEFORE v → prepending keeps prerequisites
        // earlier in the final order (finish-time reverse order).
        order_.push_back(v);
        return true;
    }

public:
    /*
     * Purpose : Return one valid order to take all courses.
     * Inputs  : numCourses — number of courses.
     *           prerequisites — [a, b] pairs: a needs b first.
     * Output  : vector<int> — topological order, empty if cyclic.
     */
    std::vector<int> findOrder(int numCourses, const std::vector<std::vector<int>>& prerequisites) {
        adj_.assign(numCourses, {});
        for (const auto& p : prerequisites) adj_[p[1]].push_back(p[0]);  // b → a
        colour_.assign(numCourses, 0);
        order_.clear();

        for (int v = 0; v < numCourses; ++v) {
            if (colour_[v] == 0 && !dfs(v)) return {};
        }
        // `order_` was built by prepending on finish; reverse it so
        // prerequisites appear before their dependents.
        std::reverse(order_.begin(), order_.end());
        return order_;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 official-style tests
 * ===================================================================== */
int main() {
    // Test 1 (official): 2, [[1,0]] → [0,1].
    // Test 2 (official): 4, [[1,0],[2,0],[3,1],[3,2]] → one of the
    //   valid orders (both algorithms must agree with each other).
    // Test 3: 1, [] → [0].
    struct { int n; std::vector<std::vector<int>> pre; } tests[] = {
        {2, {{1, 0}}},
        {4, {{1, 0}, {2, 0}, {3, 1}, {3, 2}}},
        {1, {}}
    };

    bool allPass = true;
    for (int t = 0; t < 3; ++t) {
        // --- Approach 1 timing + memory ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto s1 = std::chrono::high_resolution_clock::now();
        std::vector<int> r1 = Solution_1().findOrder(tests[t].n, tests[t].pre);
        auto e1_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);

        // --- Approach 2 timing + memory ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto s2 = std::chrono::high_resolution_clock::now();
        std::vector<int> r2 = Solution_2().findOrder(tests[t].n, tests[t].pre);
        auto e2_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);

        long mem1 = (after1.ru_maxrss - before1.ru_maxrss);
        long mem2 = (after2.ru_maxrss - before2.ru_maxrss);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1_ - s1).count() / 1000.0;
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2_ - s2).count() / 1000.0;

        // Validity check: every prerequisite b must appear before a in
        // the output order (also verifies both orders are correct).
        auto validOrder = [&](const std::vector<int>& order) {
            if (order.size() != static_cast<size_t>(tests[t].n)) return false;
            std::vector<int> pos(tests[t].n, -1);
            for (size_t i = 0; i < order.size(); ++i) pos[order[i]] = static_cast<int>(i);
            for (const auto& p : tests[t].pre) {
                if (pos[p[1]] > pos[p[0]]) return false;
            }
            return true;
        };

        bool ok1 = validOrder(r1);
        bool ok2 = validOrder(r2);
        bool ok = ok1 && ok2;
        allPass = allPass && ok;

        std::cout << "Test " << (t + 1) << (ok ? " PASS" : " FAIL");
        std::cout << " | A1=[";
        for (size_t i = 0; i < r1.size(); ++i) std::cout << (i ? "," : "") << r1[i];
        std::cout << "]  time=" << us1 << " µs  mem=" << mem1 << " KB";
        std::cout << " | A2=[";
        for (size_t i = 0; i < r2.size(); ++i) std::cout << (i ? "," : "") << r2[i];
        std::cout << "]  time=" << us2 << " µs  mem=" << mem2 << " KB\n";
    }
    std::cout << (allPass ? "PASS : all tests green on both approaches.\n"
                          : "FAIL : at least one test/approach disagrees.\n");
    return 0;
}