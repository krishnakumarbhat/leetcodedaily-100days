/*
 * =====================================================================
 * LeetCode 70 : Climbing Stairs                                   (Easy)
 * https://leetcode.com/problems/climbing-stairs/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   You climb a staircase of `n` steps. Each move takes either 1 step
 *   or 2 steps. Count the DISTINCT ways to reach the top.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The only way to LAND on step i is from step i-1 (one 1-step) or
 *   from step i-2 (one 2-step). Every path to i extends a path to i-1
 *   or a path to i-2 → ways(i) = ways(i-1) + ways(i-2). That is the
 *   Fibonacci sequence: overlapping subproblems (ways(3) is needed by
 *   both ways(4) and ways(5)) → textbook dynamic programming.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up tabulation with rolling variables (BEST)
 *   dp[i] = distinct ways to reach step i.
 *   Recurrence : dp[i] = dp[i-1] + dp[i-2]     dp[0] = dp[1] = 1
 *   State space : i ∈ [0, n] → n+1 states, mapped onto array dp[n+1],
 *                filled left→right. Cell i reads only i-1 and i-2.
 *   Space optimization : only the last TWO values are ever needed →
 *                replace the table by two rolling variables → O(1).
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized recursion
 *   f(i) = f(i-1) + f(i-2), memo[i] caches every solved state so the
 *   naive exponential recursion collapses to O(n) work.
 *   Trade-off : easier to derive, but each call costs a stack frame +
 *               a memo lookup; very deep n risks stack overflow.
 *   Time  Complexity : O(n)   Space Complexity : O(n) (memo + stack)
 * ---------------------------------------------------------------------
 * DEEP DIVE — optimal substructure & the recurrence→array mapping
 *   Naive recursion for f(n) recomputes f(3) O(fib) times — exponential.
 *   The two DP strategies are the two ways to kill that overlap:
 *   tabulation solves states in dependency order (left→right, each once),
 *   memoization solves on demand but never twice. The recurrence maps
 *   1:1 onto the array: dp[i] looks BACKWARD only (i-1, i-2) — that
 *   one-directional dependency is exactly what makes rolling variables
 *   safe: when computing dp[i], dp[i-2] is no longer needed after the
 *   slide, so old cells can be forgotten instead of stored.
 *   Real life : the Fibonacci model (rabbit populations, 1202), branch
 *   counting in trees, grid path counting, tiling counts.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : bottom-up with two rolling variables
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Count distinct ways to climb `n` stairs (1 or 2 per move).
     * Inputs  : n — number of steps.
     * Output  : int — total number of distinct ways.
     */
    int climbStairs(int n) {
        // Rolling window: prev2 = dp[i-2], prev1 = dp[i-1].
        int prev2 = 1;  // dp[0] = 1 — one way to stand on step 0
        int prev1 = 1;  // dp[1] = 1 — one way to reach step 1
        for (int i = 2; i <= n; ++i) {
            const int cur = prev1 + prev2;  // dp[i] = dp[i-1] + dp[i-2]
            prev2 = prev1;                  // slide the window right
            prev1 = cur;
        }
        return prev1;  // dp[n]
    }
};

/* =====================================================================
 * APPROACH 2 : top-down memoized recursion
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Count distinct ways to climb `n` stairs via memoized DFS.
     * Inputs  : n — number of steps.
     * Output  : int — total number of distinct ways.
     */
    int climbStairs(int n) {
        // memo[i] = -1 means "state i not solved yet".
        memo.assign(n + 1, -1);
        return f(n);
    }

private:
    std::vector<int> memo;

    /*
     * Purpose : Recursive state solver with caching (top-down DP).
     * Inputs  : i — current step we want to reach.
     * Output  : int — ways to reach step i.
     */
    int f(int i) {
        if (i <= 1) {
            return 1;                    // base case: dp[0] = dp[1] = 1
        }
        if (memo[i] != -1) {
            return memo[i];              // overlapping subproblem → reuse
        }
        // The recurrence, cached before returning.
        return memo[i] = f(i - 1) + f(i - 2);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (n, expected ways). Both solutions must match.
    struct Test { int n; int expected; };
    const std::vector<Test> tests = {
        {2, 2},    // 1+1, 2
        {3, 3},    // 1+1+1, 1+2, 2+1
        {10, 89}   // Fibonacci: F(11) with F(1)=F(2)=1 → 89
    };

    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: steady_clock for time, getrusage for RAM ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const int r1 = Solution_1().climbStairs(t.n);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        // ru_maxrss delta = peak RAM of this run (KB on Linux).
        const double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        const long kb1 = after1.ru_maxrss - before1.ru_maxrss;
        total_us_1 += us1;
        total_kb_1 += kb1;

        // --- Approach 2 ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const int r2 = Solution_2().climbStairs(t.n);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        const bool ok = (r1 == t.expected) && (r2 == t.expected);
        allPass = allPass && ok;

        std::cout << "n=" << t.n << "  A1=" << r1 << "  A2=" << r2
                  << "  expected=" << t.expected
                  << (ok ? "  PASS" : "  FAIL")
                  << "  A1 " << us1 << "µs/" << kb1 << "KB  A2 " << us2
                  << "µs/" << kb2 << "KB\n";
    }

    std::cout << "Totals: A1 " << total_us_1 << "µs/" << total_kb_1
              << "KB | A2 " << total_us_2 << "µs/" << total_kb_2 << "KB\n";
    std::cout << (allPass
                  ? "PASS : both approaches match every expected output."
                  : "FAIL : at least one answer is wrong.")
              << "\n";
    return allPass ? 0 : 1;
}