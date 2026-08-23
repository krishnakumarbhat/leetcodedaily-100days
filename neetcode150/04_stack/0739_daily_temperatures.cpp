/*
 * =====================================================================
 * LeetCode 739 : Daily Temperatures                                (Medium)
 * https://leetcode.com/problems/daily-temperatures/
 * Category   : Stack (monotonic)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of daily temperatures, return an answer array where
 *   answer[i] = the number of days you must wait for a WARMER day, or
 *   0 if no warmer day ever follows.
 * ---------------------------------------------------------------------
 * INTUITION
 *   For every day i we ask "when does the next strictly-greater value
 *   appear?" Walking left→right, while temperatures only cool down we
 *   cannot answer any day yet — their answers are still pending. The
 *   moment a warmer day arrives, ALL cooler days behind it get their
 *   answers resolved at once. Pending days form a stack; the first
 *   pending day is the most recent cooler one — LIFO again.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Monotonic decreasing stack (BEST)
 *   Invariant: stack holds indices whose temperatures are STRICTLY
 *   DECREASING from bottom to top. For each day i: while the stack is
 *   non-empty and temperatures[i] > temperatures[stack.top()], the
 *   top index has found its first warmer day → answer = i − top.
 *   Then push i. Every index is pushed and popped exactly once.
 *   Time  Complexity : O(n)  — amortized O(1) per index.
 *   Space Complexity : O(n)  — the stack (≤ n entries).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Brute force (contrast)
 *   For each day scan forward until a warmer day is found.
 *   Time  Complexity : O(n²)  Space Complexity : O(1).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — the monotonic stack invariant
 *   This is the "next greater element" family (0084 uses the mirrored
 *   "previous smaller", 0853 the same ordering trick on times). The
 *   invariant "stack holds indices in decreasing temperature order"
 *   is re-established before every push: pop WHILE the top is cooler,
 *   resolve its answer, then push. Because each index lives on the
 *   stack for a single contiguous period, total pops = total pushes
 *   = n → the sweep is linear. Same pattern, three problems.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <vector>       // std::vector — temperatures and the answer
#include <stack>        // std::stack — the monotonic stack of indices
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Monotonic decreasing stack
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Days until the next warmer day, per input day.
     * Inputs  : temperatures — daily temperatures in order.
     * Output  : vector where out[i] is the wait (0 = never warmer).
     */
    std::vector<int> dailyTemperatures(const std::vector<int>& temperatures) {
        int n = static_cast<int>(temperatures.size());

        // answer : one slot per day, default 0 (never warmer).
        std::vector<int> answer(n, 0);

        // st : indices of days whose warmer day is still pending;
        // temperatures strictly DECREASING from bottom to top.
        std::stack<int> st;

        // Single left→right pass — the whole O(n) work.
        for (int i = 0; i < n; ++i) {

            // Day i is warmer than the pending top → the top's wait is
            // over: its next warmer day is EXACTLY day i.
            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {

                // Day count between the pending day and day i.
                answer[st.top()] = i - st.top();
                st.pop();   // resolved — remove from the pending stack
            }

            // Day i itself is now pending (nothing warmer seen yet).
            st.push(i);
        }

        return answer;
    }
};

/* =====================================================================
 * APPROACH 2 : Brute force (contrast)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Days until the next warmer day, per input day.
     * Inputs  : temperatures — daily temperatures in order.
     * Output  : vector where out[i] is the wait (0 = never warmer).
     */
    std::vector<int> dailyTemperatures(const std::vector<int>& temperatures) {
        int n = static_cast<int>(temperatures.size());
        std::vector<int> answer(n, 0);

        // For every day, scan forward until a strictly warmer day.
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {

                // First warmer day found → distance is the wait.
                if (temperatures[j] > temperatures[i]) {
                    answer[i] = j - i;
                    break;   // stop scanning this i
                }
            }
            // No warmer day found → answer[i] stays 0.
        }

        return answer;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness tests (2-3 cases per solution) ---
    struct Test { std::vector<int> t; std::vector<int> expect; };
    Test tests[] = {
        // Official example 1.
        {{73, 74, 75, 71, 69, 72, 76, 73}, {1, 1, 4, 2, 1, 1, 0, 0}},
        // Always warmer → every wait is exactly 1 except the last day.
        {{30, 40, 50, 60}, {1, 1, 1, 0}},
        // Monotone cooling → only the final day answers.
        {{90, 80, 70, 60}, {0, 0, 0, 0}}
    };

    bool all_ok = true;
    for (const Test& t : tests) {
        std::vector<int> r1 = Solution_1().dailyTemperatures(t.t);
        std::vector<int> r2 = Solution_2().dailyTemperatures(t.t);
        bool ok = r1 == t.expect && r2 == t.expect;
        if (!ok) all_ok = false;
        std::cout << (ok ? "PASS" : "FAIL")
                  << " : " << t.t.size() << " days  monotonic=[";
        for (int x : r1) std::cout << x << ",";
        std::cout << "]  brute=[";
        for (int x : r2) std::cout << x << ",";
        std::cout << "]\n";
    }

    // --- Benchmark: descending ramp — worst case for brute force ---
    std::vector<int> big;
    for (int i = 50000; i > 0; --i) big.push_back(i);

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    std::vector<int> r1 = Solution_1().dailyTemperatures(big);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    std::vector<int> r2 = Solution_2().dailyTemperatures(big);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (monotonic stack) : " << r1[0] << "…"
              << "  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (brute force)     : " << r2[0] << "…"
              << "  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
