/*
 * =====================================================================
 * LeetCode 22 : Generate Parentheses                               (Medium)
 * https://leetcode.com/problems/generate-parentheses/
 * Category   : Stack / Backtracking
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an integer n, generate ALL well-formed combinations of n
 *   pairs of parentheses — every '(' must be closed by a later ')',
 *   and the count of ')' may never exceed the count of '(' while the
 *   string is being built left to right.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A partial string stays valid iff it never contains more ')' than
 *   '(' — i.e. open_count >= close_count ALWAYS. At every position we
 *   have at most two legal moves:
 *     • append '(' if open_count < n       (more opens allowed)
 *     • append ')' if close_count < open_count (it closes an open)
 *   Enumerating all legal move sequences is a DFS; the recursion depth
 *   is exactly 2n, and the call stack is a stack of partial strings.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Backtracking DFS (BEST)
 *   Recursively grow a string, only taking the two legal moves above,
 *   and record the string when it reaches length 2n. Every generated
 *   string is valid by construction — no filtering needed.
 *   Time  Complexity : O(4ⁿ/√n) — the n-th Catalan number of leaves,
 *                        each of length 2n (≈ 4ⁿ/√(π n³) strings).
 *   Space Complexity : O(n)  — recursion depth 2n + the answer list.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative BFS (explicit queue, no recursion)
 *   The same expansion, level by level: a queue of (string, opens,
 *   closes) grows every frontier simultaneously until length 2n.
 *   Identical complexity, but the frontier holds MANY strings at once.
 *   Time  Complexity : O(4ⁿ/√n)  Space Complexity : O(4ⁿ/√n).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — what is "stack" here?
 *   Approach 1's hidden stack is the CALL STACK (last-in-first-out of
 *   partial strings); approach 2 swaps it for an explicit FIFO queue.
 *   Both are "branch-and-bound over a frontier" — the DFS variant
 *   (stack) is standard because it keeps only O(n) partial strings in
 *   memory, while BFS holds a full level of the Catalan tree.
 *   The guard close < open is the invariant that makes every branch
 *   valid without ever backtracking on mistakes.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <string>       // std::string — building bracket strings
#include <vector>       // std::vector — the result list
#include <queue>        // std::queue — the BFS frontier in approach 2
#include <stack>        // std::stack — (documented) DFS call stack
#include <tuple>        // std::tuple — (string, open, close) triples
#include <functional>   // std::function — typed recursion helper
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Backtracking DFS
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Generate every well-formed combination of n pairs.
     * Inputs  : n — number of '(' ')' pairs to generate (n >= 1).
     * Output  : vector of all valid strings, each of length 2n.
     */
    std::vector<std::string> generateParenthesis(int n) {
        std::vector<std::string> result;

        // Helper recurse: 'cur' is the string so far (always valid).
        // open / close count the parentheses already placed.
        std::function<void(std::string, int, int)> dfs =
            [&](std::string cur, int open, int close) {

            // Length 2n → every pair used → this branch is complete.
            if (static_cast<int>(cur.size()) == 2 * n) {
                result.push_back(cur);
                return;          // no more moves possible from a full string
            }

            // Legal move 1: open a new pair while budget remains.
            if (open < n) {
                dfs(cur + '(', open + 1, close);
            }

            // Legal move 2: close an open pair — only if one is open.
            // This guard is the entire correctness argument.
            if (close < open) {
                dfs(cur + ')', open, close + 1);
            }
        };

        dfs("", 0, 0);
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative BFS (explicit queue)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Generate every well-formed combination of n pairs.
     * Inputs  : n — number of '(' ')' pairs to generate (n >= 1).
     * Output  : vector of all valid strings, each of length 2n.
     */
    std::vector<std::string> generateParenthesis(int n) {
        std::vector<std::string> result;

        // Frontier entry: (partial string, opens used, closes used).
        std::queue<std::tuple<std::string, int, int>> frontier;
        frontier.push({"", 0, 0});

        // Level-by-level expansion — identical rules to the DFS.
        while (!frontier.empty()) {
            auto [cur, open, close] = frontier.front();
            frontier.pop();

            // Full string → this leaf is a final answer.
            if (static_cast<int>(cur.size()) == 2 * n) {
                result.push_back(cur);
                continue;        // leaf: nothing else to expand
            }

            // Same two legal moves as approach 1.
            if (open < n) {
                frontier.push({cur + '(', open + 1, close});
            }
            if (close < open) {
                frontier.push({cur + ')', open, close + 1});
            }
        }

        return result;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness tests: n = 1, 2, 3 (counts must match Catalan) ---
    int ns[] = {1, 2, 3};
    int expect[] = {1, 2, 5};   // Catalan numbers C_1..C_3
    bool all_ok = true;

    for (int i = 0; i < 3; ++i) {
        std::vector<std::string> r1 = Solution_1().generateParenthesis(ns[i]);
        std::vector<std::string> r2 = Solution_2().generateParenthesis(ns[i]);
        bool ok = static_cast<int>(r1.size()) == expect[i] &&
                  static_cast<int>(r2.size()) == expect[i];
        if (!ok) all_ok = false;
        std::cout << (ok ? "PASS" : "FAIL")
                  << " : n=" << ns[i] << "  dfs-count=" << r1.size()
                  << "  bfs-count=" << r2.size()
                  << "  expect=" << expect[i] << "\n";
    }

    // --- Benchmark on n = 12 (≈ 20 million strings, noticeable time) ---
    const int N = 12;

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    std::vector<std::string> r1 = Solution_1().generateParenthesis(N);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    std::vector<std::string> r2 = Solution_2().generateParenthesis(N);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (backtracking DFS)  : " << r1.size()
              << " strings  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (iterative BFS)     : " << r2.size()
              << " strings  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
