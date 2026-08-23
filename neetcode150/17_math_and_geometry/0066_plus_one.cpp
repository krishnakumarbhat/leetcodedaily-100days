/*
 * =====================================================================
 * LeetCode 66 : Plus One                                           (Easy)
 * https://leetcode.com/problems/plus-one/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a big integer as an array of digits (most significant
 *   first, no leading zeros), add ONE to it and return the new digit
 *   array. E.g. [9,9] → [1,0,0]. The number may be arbitrarily long
 *   — converting to int and back can overflow; do digit arithmetic.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Adding 1 only touches digits from the right until a digit < 9
 *   absorbs the carry. If EVERY digit is 9 the number overflows to a
 *   NEW digit: [9,9] → [1,0,0]. Walk from the least significant
 *   digit, carrying 1 leftward, and stop early when no carry remains.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Backwards scan with carry (BEST)
 *   Start carry = 1 at the last digit. For each digit (right → left):
 *   add carry, if the digit becomes 10 set it to 0 and carry on,
 *   otherwise the carry is absorbed and we can return immediately.
 *   If the whole array was 9s, prepend a leading 1.
 *   Time  Complexity : O(n)   Space Complexity : O(1) extra
 *   (worst case: all-9 input forces the full walk; the O(n) new array
 *   is only allocated for the all-9 overflow case).
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sum with explicit digit math (contrast)
 *   Convert to integer, add 1, convert back to digits. Overflows
 *   silently for inputs longer than 19 digits (or raises in Python
 *   for truly huge ones). Shown as the "tempting but wrong" baseline.
 *   Time  Complexity : O(n)   Space Complexity : O(n)
 *   WHY it fails: C++ long long holds ~19 digits — the problem allows
 *   arbitrarily many; even Python big-ints work, but the digit walk
 *   is the portable, dependency-free answer.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the early exit makes it O(n) amortized cheap
 *   The carry propagates exactly until the first non-9 digit from the
 *   right. Average case: a uniformly random digit is 9 with
 *   probability 1/10, so the expected walk length is
 *       1 + 1/10 + 1/100 + … = 10/9  →  O(1) average!
 *   Only the worst case (all 9s) costs the full O(n) walk. Amortized
 *   over many increments, this is the same analysis as a binary
 *   counter's carry chain.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — formatting result lines
#include <vector>         // std::vector — the digit array
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // (unused here; kept for uniform include set)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Backwards scan with carry (best)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Add one to a big integer stored as a digit array.
     * Inputs  : digits — most-significant-first digit array.
     * Output  : vector<int> holding the incremented digits.
     */
    std::vector<int> plusOne(const std::vector<int>& digits) {
        std::vector<int> out = digits;   // work on a copy; return fresh

        // Walk from the LEAST significant digit, carrying 1 leftward.
        for (int i = static_cast<int>(out.size()) - 1; i >= 0; --i) {
            if (out[i] < 9) {
                out[i] += 1;             // carry absorbed right here
                return out;              // done — digits left unchanged
            }
            out[i] = 0;                  // 9+1 = 10 → 0, carry propagates
        }

        // Every digit was 9 → the number gained one new leading digit.
        out.insert(out.begin(), 1);      // [9,9,9] → [1,0,0,0]
        return out;
    }
};

/* =====================================================================
 * APPROACH 2 : Integer round-trip (contrast — overflow trap)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Add one by converting the digit array to an integer.
     * Inputs  : digits — most-significant-first digit array.
     * Output  : vector<int> holding the incremented digits.
     * NOTE    : only correct while the value fits a long long
     *           (~19 digits); longer inputs silently wrap — this is
     *           why Approach 1 exists.
     */
    std::vector<int> plusOne(const std::vector<int>& digits) {
        // Horner's rule: value = ((d0)*10 + d1)*10 + ... + dn.
        long long value = 0;
        for (const int d : digits) {
            value = value * 10 + d;
        }
        value += 1;

        // Emit the digits of value, most significant first.
        std::vector<int> out;
        if (value == 0) {
            out.push_back(0);
            return out;
        }
        while (value > 0) {
            out.push_back(static_cast<int>(value % 10));
            value /= 10;
        }
        // Collected least-significant-first → reverse by hand.
        int lo = 0;
        int hi = static_cast<int>(out.size()) - 1;
        while (lo < hi) {
            const int tmp = out[lo];
            out[lo] = out[hi];
            out[hi] = tmp;
            ++lo;
            --hi;
        }
        return out;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests; time + peak RAM
 * ===================================================================== */
int main() {
    const std::vector<int> tests[] = {
        { 1, 2, 3 },
        { 9, 9, 9 },
        { 4, 3, 2, 1 },
    };
    const std::vector<int> expected[] = {
        { 1, 2, 4 },
        { 1, 0, 0, 0 },
        { 4, 3, 2, 2 },
    };

    bool all_ok = true;

    const auto run_all = [&](const std::string& label, const auto& solve) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        const auto t0 = std::chrono::steady_clock::now();

        bool ok = true;
        for (size_t t = 0; t < 3; ++t) {
            const std::vector<int> got = solve(tests[t]);
            const bool pass = (got == expected[t]);
            ok = ok && pass;
            std::cout << "  test " << (t + 1) << ": [";
            for (size_t i = 0; i < got.size(); ++i) {
                if (i) { std::cout << ","; }
                std::cout << got[i];
            }
            std::cout << "]" << (pass ? "  PASS" : "  FAIL") << "\n";
        }

        const auto t1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        const double us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
        const long kb = after.ru_maxrss - before.ru_maxrss;
        std::cout << label << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " us  peak-mem = " << kb << " KB\n";
        all_ok = all_ok && ok;
    };

    std::cout << "Test suite: 3 fixed cases\n";
    run_all("Approach 1 (backwards carry scan)  ", [](const std::vector<int>& d) {
        return Solution_1().plusOne(d);
    });
    run_all("Approach 2 (int round-trip)        ", [](const std::vector<int>& d) {
        return Solution_2().plusOne(d);
    });

    std::cout << (all_ok
                  ? "PASS : both approaches return the incremented digits on all tests."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}