/*
 * =====================================================================
 * LeetCode 150 : Evaluate Reverse Polish Notation                   (Medium)
 * https://leetcode.com/problems/evaluate-reverse-polish-notation/
 * Category   : Stack
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of strings `tokens` holding a valid Reverse Polish
 *   (postfix) arithmetic expression over + - * / with integer operands,
 *   evaluate it. Division truncates toward ZERO (C++ int division),
 *   and operands / results fit in 32-bit ints.
 * ---------------------------------------------------------------------
 * INTUITION
 *   In postfix notation an operator ALWAYS applies to the two most
 *   recently seen operands. "Most recent first" = LIFO = stack: push
 *   numbers as they arrive; on an operator, pop the two top operands,
 *   compute, push the result back. When the token stream ends, the
 *   single value left on the stack is the answer.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Stack + operator set (BEST)
 *   Operands are pushed; operators pop a and b (b popped SECOND is the
 *   left operand — order matters for - and /), then push the result.
 *   An unordered_set answers "is this token an operator?" in O(1).
 *   Time  Complexity : O(n)  — each token handled exactly once.
 *   Space Complexity : O(n)  — the stack holds ≤ n operands.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Stack + char switch (no hash set)
 *   Same algorithm, but operators are recognised by shape: every
 *   operator token is a SINGLE character and not a digit. That makes
 *   a 4-case switch possible and avoids allocating a set.
 *   Time  Complexity : O(n)  Space Complexity : O(n).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — what the stack buys, and the div trap
 *   Postfix is stack-native: no parentheses, no precedence rules, the
 *   stack IS the expression tree being evaluated bottom-up.
 *   C++ int division truncates TOWARD ZERO, which matches the problem.
 *   Python's `//` truncates toward −∞, so `-3 // 2 == -2` — the
 *   Python port must use int(a / b) to emulate C++ semantics. Same
 *   idea everywhere, one line changes the whole behaviour.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <vector>       // std::vector — the token list
#include <string>       // std::string — token strings
#include <stack>        // std::stack — the operand stack
#include <unordered_set>// std::unordered_set — operator membership test
#include <cctype>       // std::isdigit — operator-vs-operand test (A2)
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Stack + operator set
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Evaluate a valid RPN expression.
     * Inputs  : tokens — postfix tokens: int strings and + - * /.
     * Output  : the integer value of the expression.
     */
    int evalRPN(const std::vector<std::string>& tokens) {
        // ops : the four operators, for O(1) membership tests.
        std::unordered_set<std::string> ops = {"+", "-", "*", "/"};

        std::stack<int> st;

        for (const std::string& tok : tokens) {

            // Number token → push the parsed value onto the stack.
            if (ops.find(tok) == ops.end()) {
                st.push(std::stoi(tok));
                continue;
            }

            // Operator token → pop the two most recent operands.
            // b was pushed LATER → b is the LEFT operand for - and /.
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();

            // Apply, push the result — it may feed another operator.
            if (tok == "+")      st.push(a + b);
            else if (tok == "-") st.push(a - b);
            else if (tok == "*") st.push(a * b);
            else                 st.push(a / b);   // C++ int div: truncate toward 0
        }

        // Valid RPN leaves exactly one value on the stack.
        return st.top();
    }
};

/* =====================================================================
 * APPROACH 2 : Stack + char switch (no hash set)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Evaluate a valid RPN expression.
     * Inputs  : tokens — postfix tokens: int strings and + - * /.
     * Output  : the integer value of the expression.
     */
    int evalRPN(const std::vector<std::string>& tokens) {
        std::stack<int> st;

        for (const std::string& tok : tokens) {

            // Every operator token is exactly one non-digit character
            // (numbers may be multi-digit and signed → size > 1).
            bool is_op = tok.size() == 1 &&
                         !std::isdigit(static_cast<unsigned char>(tok[0]));
            if (!is_op) {
                st.push(std::stoi(tok));
                continue;
            }

            // Same pops as approach 1 — b is the left operand.
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();

            // 4-way switch: the token's single character IS the op.
            switch (tok[0]) {
                case '+': st.push(a + b); break;
                case '-': st.push(a - b); break;
                case '*': st.push(a * b); break;
                default:  st.push(a / b); break;   // '/' — truncate toward 0
            }
        }

        return st.top();
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness tests (2-3 cases per solution) ---
    struct Test { std::vector<std::string> t; int expect; };
    Test tests[] = {
        // ((2 + 1) * 3) = 9 — the official example 1.
        {{"2", "1", "+", "3", "*"}, 9},
        // 4 + (13 / 5) = 4 + 2 = 6 — 13/5 truncates toward zero.
        {{"4", "13", "5", "/", "+"}, 6},
        // The long official example 3 → 22.
        {{"10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"}, 22},
        // Negative result: (5 - 8) * 2 = -6.
        {{"5", "8", "-", "2", "*"}, -6}
    };

    bool all_ok = true;
    for (const Test& t : tests) {
        int r1 = Solution_1().evalRPN(t.t);
        int r2 = Solution_2().evalRPN(t.t);
        if (r1 != t.expect || r2 != t.expect) all_ok = false;
        std::cout << (r1 == t.expect && r2 == t.expect ? "PASS" : "FAIL")
                  << " : " << t.t.size() << " tokens  set=" << r1
                  << "  switch=" << r2 << "  expect=" << t.expect << "\n";
    }

    // --- Benchmark: long chain of mixed operations ---
    std::vector<std::string> big;
    for (int i = 0; i < 50000; ++i) {
        big.push_back(std::to_string(i));
        big.push_back(std::to_string(i + 1));
        big.push_back("+");
    }
    big.push_back("2");
    big.push_back("*");

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    int r1 = Solution_1().evalRPN(big);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    int r2 = Solution_2().evalRPN(big);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (stack + set)     : " << r1
              << "  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (stack + switch)  : " << r2
              << "  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
