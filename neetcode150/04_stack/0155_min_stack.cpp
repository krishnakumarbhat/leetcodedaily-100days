/*
 * =====================================================================
 * LeetCode 155 : Min Stack                                         (Medium)
 * https://leetcode.com/problems/min-stack/
 * Category   : Stack (design)
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a stack supporting push, pop, top AND getMin — all in
 *   O(1) time. getMin returns the smallest value currently in the
 *   stack. The catch: O(1) getMin, not an O(n) scan on demand.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A plain stack cannot answer "what is the min?" in O(1) — the min
 *   can change arbitrarily when we pop. BUT the min at stack depth d
 *   only depends on values pushed at depth ≤ d. So keep a PARALLEL
 *   stack: at depth d it stores min of everything pushed so far.
 *   When the main stack pops, the parallel stack pops with it — the
 *   min is always in sync because both stacks are the SAME depth.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Two parallel stacks (BEST)
 *   Main stack holds values; min stack holds the running minimum.
 *   push(v):  main.push(v); min.push(min(min.top(), v)).
 *   pop():    pop BOTH stacks together (they are lockstep by design).
 *   getMin(): peek the min stack's top.
 *   Time  Complexity : O(1) for EVERY operation — nothing is scanned.
 *   Space Complexity : O(n) — two stacks, n entries each.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Single stack of (value, runningMin) pairs
 *   One stack; every element is a tuple (v, currentMin). Same logic,
 *   one physical stack, but each entry carries a second word.
 *   Time  Complexity : O(1) for every operation.
 *   Space Complexity : O(n) — one stack of 2-word entries.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — the parallel-minimum invariant
 *   Invariant: after any sequence of ops, min_stack.top() equals
 *   min(main_stack). Values in min_stack are NON-INCREASING from
 *   bottom to top (each push may only lower or keep the min). Because
 *   a pop removes the SAME depth from both stacks, the invariant
 *   survives every operation — this is why O(1) getMin is possible:
 *   the answer is precomputed per depth, not computed on demand.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <stack>        // std::stack — the two LIFO structures
#include <utility>      // std::pair — (value, min) entries in approach 2
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Two parallel stacks
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Stack with O(1) getMin via a parallel min stack.
     * Inputs  : push(v) inserts v; pop() removes the top; top() reads
     *           the top value; getMin() reads the current minimum.
     * Output  : methods mutate the stacks / return the asked value.
     */
    Solution_1() {}

    // Push v, and push the new running minimum alongside.
    void push(int val) {
        main_stack.push(val);

        // Running min = min(previous min, this value). Empty min stack
        // → this value is trivially the min so far.
        int new_min = min_stack.empty() ? val : std::min(min_stack.top(), val);
        min_stack.push(new_min);
    }

    // Pop BOTH stacks — the depth must stay identical so the min
    // entry at the top always describes the main stack's top depth.
    void pop() {
        main_stack.pop();
        min_stack.pop();
    }

    // Peek the top value — main stack only.
    int top() const {
        return main_stack.top();
    }

    // The precomputed min at this depth — O(1), no scanning.
    int getMin() const {
        return min_stack.top();
    }

private:
    std::stack<int> main_stack;  // the real stack of values
    std::stack<int> min_stack;   // running minimum at each depth
};

/* =====================================================================
 * APPROACH 2 : Single stack of (value, runningMin) pairs
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Stack with O(1) getMin using one tuple stack.
     * Inputs  : push(v) inserts v; pop() removes the top; top() reads
     *           the top value; getMin() reads the current minimum.
     * Output  : methods mutate the stack / return the asked value.
     */
    Solution_2() {}

    // Push a (value, running-minimum) pair in one operation.
    void push(int val) {
        // The pair's second field mirrors approach 1's min stack.
        int new_min = data.empty() ? val : std::min(data.top().second, val);
        data.push({val, new_min});
    }

    // Single stack → single pop; min sync is inside the pair.
    void pop() {
        data.pop();
    }

    // First field of the top pair is the actual value.
    int top() const {
        return data.top().first;
    }

    // Second field of the top pair is the min at this depth.
    int getMin() const {
        return data.top().second;
    }

private:
    std::stack<std::pair<int, int>> data;  // (value, minAtThisDepth)
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness: replay the official example 1 script ---
    // ops: push -2, push 0, push -3, getMin→-3, pop, top→0, getMin→-2
    Solution_1 s1;
    Solution_2 s2;

    s1.push(-2); s2.push(-2);
    s1.push(0);  s2.push(0);
    s1.push(-3); s2.push(-3);

    bool ok1 = s1.getMin() == -3 && s2.getMin() == -3;
    s1.pop(); s2.pop();
    bool ok2 = s1.top() == 0 && s2.top() == 0;
    bool ok3 = s1.getMin() == -2 && s2.getMin() == -2;

    // Extra stress: interleaved pops re-expose older minimums.
    s1.push(-5); s2.push(-5);
    bool ok4 = s1.getMin() == -5 && s2.getMin() == -5;
    s1.pop(); s2.pop();
    bool ok5 = s1.getMin() == -2 && s2.getMin() == -2;

    bool all_ok = ok1 && ok2 && ok3 && ok4 && ok5;
    std::cout << (ok1 ? "PASS" : "FAIL") << " : getMin after push(-3) == -3\n";
    std::cout << (ok2 ? "PASS" : "FAIL") << " : top() after pop == 0\n";
    std::cout << (ok3 ? "PASS" : "FAIL") << " : getMin after pop == -2\n";
    std::cout << (ok4 ? "PASS" : "FAIL") << " : getMin after push(-5) == -5\n";
    std::cout << (ok5 ? "PASS" : "FAIL") << " : getMin after popping -5 == -2\n";

    // --- Benchmark: 200k random pushes/pops through both ---
    const int N = 200000;

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    Solution_1 b1;
    for (int i = 0; i < N; ++i) {
        b1.push((i * 7919) % 1000000 - (i % 3 == 0 ? 1 : 0));
        if (i % 4 == 0 && i > 0) b1.pop();   // never pop below empty at i=0
        if (i % 16 == 0) b1.getMin();
    }
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    Solution_2 b2;
    for (int i = 0; i < N; ++i) {
        b2.push((i * 7919) % 1000000 - (i % 3 == 0 ? 1 : 0));
        if (i % 4 == 0 && i > 0) b2.pop();   // never pop below empty at i=0
        if (i % 16 == 0) b2.getMin();
    }
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (two stacks)      : 200k ops  time = "
              << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (tuple stack)     : 200k ops  time = "
              << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
