/*
 * =====================================================================
 * LeetCode 20 : Valid Parentheses                                   (Easy)
 * https://leetcode.com/problems/valid-parentheses/
 * Category   : Stack
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string `s` made only of '(' ')' '{' '}' '[' ']', return
 *   true if the brackets are correctly nested: every opener must be
 *   closed by the SAME bracket type, and the most recently opened
 *   bracket must be the first to close.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Most recent opener closes first" is the LIFO contract — that is
 *   exactly what a STACK implements. Push every opener; when a closer
 *   arrives, the stack top must be its matching opener, and we pop it.
 *   A hash map turns "which opener matches this closer?" into an O(1)
 *   lookup instead of a chain of if/else comparisons.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Stack + hash map (BEST)
 *   Single left-to-right pass. Closers are looked up in the map and
 *   compared against the stack top; any mismatch (or a closer with an
 *   empty stack) is an immediate false. A valid string leaves the
 *   stack EMPTY — every opener was matched.
 *   Time  Complexity : O(n)  — each char pushed/popped at most once,
 *                        every map op is O(1) average.
 *   Space Complexity : O(n)  — the stack holds at most n openers.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Repeated pair erasure (no stack, no map)
 *   Keep deleting the substrings "()", "{}", "[]" from a working copy
 *   until the string stops shrinking; valid ⇔ the result is empty.
 *   Intuitive, but each full pass only removes the innermost pairs,
 *   so worst case needs n/2 passes over an O(n) string.
 *   Time  Complexity : O(n²)  Space Complexity : O(n) (working copy).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — std::stack and the matching map
 *   std::stack<T> is an adapter over std::deque<T>: push/pop/top are
 *   O(1), and the deque grows in blocks so we never re-copy elements.
 *   The closer→opener map is std::unordered_map — separate chaining
 *   (bucket + linked list of colliding keys), O(1) average per op.
 *   Python's dict solves the same job with open addressing + linear
 *   probing:  h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
 *   With only 3 keys both are overkill — but the map reads clearly
 *   and scales if the problem ever grew more bracket types.
 * =====================================================================
 */

#include <iostream>     // std::cout — printing test + benchmark output
#include <string>       // std::string — the input bracket string
#include <stack>        // std::stack — the LIFO core of approach 1
#include <unordered_map>// std::unordered_map — closer→opener matching
#include <chrono>       // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Stack + hash map
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether the bracket string is correctly nested.
     * Inputs  : s — string of '(' ')' '{' '}' '[' ']' characters only.
     * Output  : true if every opener is closed in LIFO order by the
     *           same bracket type, false otherwise.
     */
    bool isValid(const std::string& s) {
        // match : closer -> the opener it must close (O(1) lookup).
        std::unordered_map<char, char> match = {
            {')', '('}, {'}', '{'}, {']', '['}
        };

        // st : every not-yet-closed opener, most recent on top.
        std::stack<char> st;

        // One linear pass — this is the entire O(n) walk.
        for (char c : s) {

            // If this character IS a closer, look up its partner...
            auto it = match.find(c);
            if (it != match.end()) {

                // ...and demand the stack top IS that partner.
                // Empty stack means the closer has nothing to close.
                if (st.empty() || st.top() != it->second) {
                    return false;   // wrong type or unmatched — fail fast
                }
                st.pop();           // pair matched → remove the opener
            } else {
                // Not a closer → it must be an opener → push it.
                st.push(c);
            }
        }

        // Every opener must have been matched → stack must be empty.
        return st.empty();
    }
};

/* =====================================================================
 * APPROACH 2 : Repeated pair erasure (no stack, no hash map)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether the bracket string is correctly nested.
     * Inputs  : s — string of '(' ')' '{' '}' '[' ']' characters only.
     * Output  : true if erasing "()" "{}" "[]" pairs iteratively
     *           reduces the string to empty, false otherwise.
     */
    bool isValid(const std::string& s) {
        // Work on a mutable copy — the input must stay untouched.
        std::string work = s;

        // Loop until a full pass removes nothing (string is stable).
        while (true) {
            bool changed = false;

            // Try every pair type; each removal deletes two characters.
            // std::string::erase + find are O(n) — hence O(n²) overall.
            static const std::string pairs[] = {"()", "{}", "[]"};
            for (const std::string& p : pairs) {
                std::size_t pos = work.find(p);
                if (pos != std::string::npos) {
                    work.erase(pos, 2);
                    changed = true;  // did remove a pair this pass
                }
            }

            // Stable string: either fully balanced (empty) or invalid.
            if (!changed) break;
        }

        // Valid ⇔ all pairs were erased ⇔ nothing remains.
        return work.empty();
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches and compare time + peak RAM
 * ===================================================================== */
int main() {
    // --- Correctness tests (2-3 cases per solution) ---
    struct Test { std::string in; bool expect; };
    Test tests[] = {
        {"()[]{}", true},   // official example 1 — every pair type
        {"([)]",  false},   // interleaved wrong nesting (classic trap)
        {"{[]}",  true},    // nested pairs, LIFO order respected
        {"(]",    false},   // mismatched types
        {"(((",   false}    // unclosed openers
    };

    bool all_ok = true;
    for (const Test& t : tests) {
        bool r1 = Solution_1().isValid(t.in);
        bool r2 = Solution_2().isValid(t.in);
        if (r1 != t.expect || r2 != t.expect) all_ok = false;
        std::cout << (r1 == t.expect ? "PASS" : "FAIL")
                  << " : \"" << t.in << "\"  stack=" << r1
                  << "  erasure=" << r2 << "  expect=" << t.expect << "\n";
    }

    // --- Benchmark: worst-case-ish nesting "((((...))))" ---
    std::string big(200000, '(');
    big.append(200000, ')');

    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    bool r1 = Solution_1().isValid(big);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB delta

    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    bool r2 = Solution_2().isValid(big);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (stack + map)     : " << r1
              << "  time = " << us_1 << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Approach 2 (pair erasure)    : " << r2
              << "  time = " << us_2 << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    // Final verdict: both must pass every correctness test.
    std::cout << (all_ok ? "PASS : all tests" : "FAIL : a test was wrong")
              << "\n";
    return all_ok ? 0 : 1;
}
