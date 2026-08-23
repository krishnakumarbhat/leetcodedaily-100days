/*
 * =====================================================================
 * LeetCode 678 : Valid Parenthesis String                          (Medium)
 * https://leetcode.com/problems/valid-parenthesis-string/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string s of '(', ')' and '*' — where '*' may be '(', ')'
 *   or nothing — decide whether SOME assignment of the stars makes s
 *   a valid parentheses sequence.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The set of POSSIBLE balance values after scanning a prefix is
 *   always a CONTIGUOUS interval of integers [lo, hi]. We never need
 *   the full set — only its min and max. A ')' shrinks the interval,
 *   '(' grows it, '*' widens it (can be −1, 0, +1). If hi drops below
 *   0 no assignment survives; if lo goes negative the interval clamps
 *   at 0 (we may drop already-closed surplus opens). Valid ⟺ lo == 0
 *   at the end. Greedy: tracking two boundary counts is sufficient
 *   because the interval property is invariant — an exchange-style
 *   argument: any two feasible assignments can be "mixed" while
 *   staying feasible, so only extremes matter.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Two-pass counter sweep (BEST, intuitive)
 *   Left→right: '(' or '*' → +1, ')' → −1; if count < 0 → false
 *   (stars acted as '('; a ')' beyond them can never be balanced).
 *   Right→left: ')' or '*' → +1, '(' → −1; same rule mirrored.
 *   Both directions must hold — a sequence valid iff the greedy
 *   "treat * as '(' going left, as ')' going right" never goes
 *   negative. Time O(n)  Space O(1).
 *   WHY sufficient: the left pass guarantees every ')' gets a '(' or
 *   '*' before it (enough opens); the right pass guarantees every '('
 *   gets a ')' or '*' after it (enough closes). Together that is
 *   exactly the condition for a valid balanced string (each bracket
 *   can be greedily paired in both directions).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Min/max open-count interval (single pass)
 *     '(' → lo++, hi++;  ')' → lo--, hi--;  '*' → lo--, hi++
 *     if hi < 0 → false; if lo < 0 → lo = 0
 *     return lo == 0
 *   Time O(n)  Space O(1). The interval [lo,hi] of possible balances
 *   is the invariant; the two passes of approach 1 are just the two
 *   extremes of this single interval walked separately.
 * ---------------------------------------------------------------------
 * DEEP DIVE — when greedy bounds beat enumerating assignments
 *   Naive: 3^m assignments (m = #stars). Greedy insight: balances are
 *   a contiguous interval because the +1/−1/0 moves of a random walk
 *   fill every integer between min and max — no "holes" can appear.
 *   Hence tracking 2 numbers replaces tracking 3^m states: the
 *   compressed representation is exact. This is the same exchange
 *   argument that makes the two-pass greedy exact: if SOME
 *   assignment works, the extreme assignments (all-as-open /
 *   all-as-close greedies) survive every prefix.
 * =====================================================================
 */

#include <iostream>       // std::cout — benchmark output
#include <vector>         // std::vector — test batch container
#include <string>         // std::string — the input sequence
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RSS measurement

/* =====================================================================
 * APPROACH 1 : Two-pass counter sweep
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide if some assignment of '*' makes s valid.
     * Inputs  : s — string of '(', ')' and '*'.
     * Output  : bool — true if a valid assignment exists.
     */
    bool checkValidString(const std::string& s) {
        // LEFT pass: stars are '(' — verifies every ')' has a partner.
        int balance = 0;
        for (char c : s) {
            if (c == '(' || c == '*') ++balance; // star can open
            else --balance;                       // ')' consumes one open
            if (balance < 0) return false;        // unmatched ')' — dead
        }

        // RIGHT pass: stars are ')' — verifies every '(' has a partner.
        balance = 0;
        for (int i = static_cast<int>(s.size()) - 1; i >= 0; --i) {
            if (s[i] == ')' || s[i] == '*') ++balance; // star can close
            else --balance;                            // '(' consumes one
            if (balance < 0) return false;             // unmatched '('
        }
        return true; // both directions pair up — valid assignment exists
    }
};

/* =====================================================================
 * APPROACH 2 : Min/max open-count interval (single pass)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide if some assignment of '*' makes s valid.
     * Inputs  : s — string of '(', ')' and '*'.
     * Output  : bool — true if a valid assignment exists.
     */
    bool checkValidString(const std::string& s) {
        int lo = 0; // minimum possible open-count (stars as ')'/empty)
        int hi = 0; // maximum possible open-count (stars as '(')

        for (char c : s) {
            if (c == '(') { ++lo; ++hi; }        // both bounds grow
            else if (c == ')') { --lo; --hi; }   // both bounds shrink
            else { --lo; ++hi; }                 // '*' widens the interval
            if (hi < 0) return false;            // even the max died
            if (lo < 0) lo = 0;                  // clamp: surplus closed
        }
        return lo == 0; // some assignment ends perfectly balanced
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, time + peak RAM
 * ===================================================================== */
int main() {
    // Official examples + parity/edge cases (odd length = invalid).
    const std::vector<std::string> tests = {
        "()",            // → true
        "(*)",           // → true
        "(*))",          // → true  (* = '(')
        "((((",          // → false (no closes at all)
        "((()))",        // → true  (plain nesting)
        "((*))",         // → true  (* = empty → (()) )
        "())(()",        // → false (official example 3 variant)
        "*",             // → true  (star = empty)
        "***"            // → true  (all stars empty)
    };
    const std::vector<bool> expected = { true, true, true, false, true, true, false, true, true };

    auto run_all = [&](int which, bool (*solve)(const std::string&)) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto t0 = std::chrono::high_resolution_clock::now();

        bool ok = true;
        for (int t = 0; t < static_cast<int>(tests.size()); ++t) {
            if (solve(tests[t]) != expected[t]) ok = false;
        }

        auto t1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);
        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1000.0;
        long mem_kb = after.ru_maxrss - before.ru_maxrss; // delta, KB

        std::cout << "Approach " << which
                  << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " µs  peak-ram-delta = " << mem_kb << " KB\n";
        return ok;
    };

    bool a1 = run_all(1, [](const std::string& s) { return Solution_1().checkValidString(s); });
    bool a2 = run_all(2, [](const std::string& s) { return Solution_2().checkValidString(s); });
    std::cout << (a1 && a2 ? "PASS : both approaches agree on every test case."
                           : "FAIL : at least one approach is wrong.") << "\n";
    return 0;
}
