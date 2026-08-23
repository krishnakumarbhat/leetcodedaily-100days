/*
 * =====================================================================
 * LeetCode 207 : Course Schedule                                    (Medium)
 * https://leetcode.com/problems/course-schedule/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   You must take `numCourses` courses labelled 0..numCourses-1.
 *   Prerequisites are pairs [a, b] meaning "to take course a you
 *   must first finish b". Decide whether ALL courses can be finished
 *   — i.e. whether a valid ordering exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Courses are nodes; an edge a → b means "a depends on b". A valid
 *   schedule exists ⇔ the directed graph has NO CYCLE. (A cycle
 *   a→b→c→a is a set of mutually dependent courses that can never be
 *   ordered.) So the problem reduces to CYCLE DETECTION on a directed
 *   graph — two classic algorithms: Kahn's algorithm (BFS on in-
 *   degrees) and DFS with 3-colour marking.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Kahn's algorithm (BEST, iterative)
 *   Count in-degrees (number of prerequisites per course). Repeatedly
 *   remove a course with in-degree 0 — those are "ready now". If we
 *   manage to remove ALL n courses, the graph is acyclic.
 *   Time  Complexity : O(V + E)  — every edge scanned once.
 *   Space Complexity : O(V + E)  — adjacency list + in-degree array.
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS with colours (0=unvisited, 1=in-stack, 2=done)
 *   Walk every edge of the DFS tree. Hitting a node that is still
 *   ON the current stack (colour 1) = back edge = cycle.
 *   Time  Complexity : O(V + E)   Space Complexity : O(V + E).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — cycle detection via colours
 *   Colour 1 ("in progress") distinguishes a BACK EDGE from a cross
 *   edge: a node can be visited but fully finished (colour 2) and
 *   safely skipped — only nodes in the CURRENT recursion stack imply
 *   a cycle. A plain boolean visited array is NOT enough for directed
 *   graphs — the third state is the whole trick. Kahn's is iterative
 *   (no recursion risk) and produces the order too (see 210).
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — adjacency lists
#include <string>           // std::string — result printing helpers
#include <queue>            // std::queue — Kahn's ready queue
#include <unordered_map>    // std::unordered_map — hash table (chaining)
#include <unordered_set>    // std::unordered_set — visited set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Kahn's algorithm — peel in-degree-0 nodes
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether all courses can be finished.
     * Inputs  : numCourses — number of courses.
     *           prerequisites — [a, b] pairs: a needs b first.
     * Output  : bool — true iff no cycle exists.
     */
    bool canFinish(int numCourses, const std::vector<std::vector<int>>& prerequisites) {
        // adjacency : course -> its prerequisites (edges a → b).
        std::vector<std::vector<int>> adj(numCourses);
        std::vector<int> indegree(numCourses, 0);
        for (const auto& p : prerequisites) {
            adj[p[0]].push_back(p[1]);  // a depends on b
            ++indegree[p[1]];           // b has one more dependent
        }

        // Ready queue: every course with NO remaining prerequisites.
        std::queue<int> q;
        for (int i = 0; i < numCourses; ++i) {
            if (indegree[i] == 0) q.push(i);
        }

        int processed = 0;  // how many courses were fully scheduled
        while (!q.empty()) {
            int course = q.front();
            q.pop();
            ++processed;
            // Finishing `course` unblocks every course that listed it
            // as a prerequisite.
            for (int dep : adj[course]) {
                if (--indegree[dep] == 0) q.push(dep);
            }
        }
        // A cycle leaves some course forever with in-degree > 0 →
        // fewer than numCourses get processed.
        return processed == numCourses;
    }
};

/* =====================================================================
 * APPROACH 2 : DFS with 3 colours — detect a back edge
 * ===================================================================== */
class Solution_2 {
private:
    std::vector<std::vector<int>> adj_;
    std::vector<int> colour_;   // 0 = unvisited, 1 = on stack, 2 = done

    /*
     * Purpose : DFS-walk from course v, report cycles in its subtree.
     * Inputs  : v — course to explore.
     * Output  : bool — false iff a cycle was found.
     */
    bool dfs(int v) {
        if (colour_[v] == 1) return false;  // back edge → cycle!
        if (colour_[v] == 2) return true;   // finished before → safe
        colour_[v] = 1;                     // enter: mark "on stack"
        for (int nb : adj_[v]) {
            if (!dfs(nb)) return false;
        }
        colour_[v] = 2;                     // exit: fully explored
        return true;
    }

public:
    /*
     * Purpose : Decide whether all courses can be finished.
     * Inputs  : numCourses — number of courses.
     *           prerequisites — [a, b] pairs: a needs b first.
     * Output  : bool — true iff no cycle exists.
     */
    bool canFinish(int numCourses, const std::vector<std::vector<int>>& prerequisites) {
        adj_.assign(numCourses, {});
        for (const auto& p : prerequisites) adj_[p[0]].push_back(p[1]);
        colour_.assign(numCourses, 0);

        // Every node seeds a DFS — the graph may be disconnected.
        for (int v = 0; v < numCourses; ++v) {
            if (colour_[v] == 0 && !dfs(v)) return false;
        }
        return true;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 official-style tests
 * ===================================================================== */
int main() {
    // Test 1 (official): 2, [[1,0]] → true (0 before 1).
    // Test 2 (official): 2, [[1,0],[0,1]] → false (mutual cycle).
    // Test 3: 4 courses, chain 0→1→2→3 with extra edge → true.
    struct { int n; std::vector<std::vector<int>> pre; bool expected; } tests[] = {
        {2, {{1, 0}}, true},
        {2, {{1, 0}, {0, 1}}, false},
        {4, {{1, 0}, {2, 0}, {3, 1}, {3, 2}}, true}
    };

    bool allPass = true;
    for (int t = 0; t < 3; ++t) {
        // --- Approach 1 timing + memory ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto s1 = std::chrono::high_resolution_clock::now();
        bool r1 = Solution_1().canFinish(tests[t].n, tests[t].pre);
        auto e1_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);

        // --- Approach 2 timing + memory ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto s2 = std::chrono::high_resolution_clock::now();
        bool r2 = Solution_2().canFinish(tests[t].n, tests[t].pre);
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