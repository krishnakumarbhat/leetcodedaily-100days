/*
 * =====================================================================
 * LeetCode 43 : Multiply Strings                                 (Medium)
 * https://leetcode.com/problems/multiply-strings/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two non-negative integers `num1` and `num2` as strings,
 *   return their product as a string. Inputs are up to 200 digits long
 *   — far beyond any 64-bit integer, so we MUST do digit-by-digit
 *   arithmetic by hand (like grade school).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Multiplying "123" × "456" is the same long multiplication you
 *   learned in school: every digit of one number multiplies every
 *   digit of the other, and partial results land at the SAME positional
 *   index: digit i of num1 × digit j of num2 contributes to the
 *   10^(i+j) place — the "i+j digit-index trick".
 * ---------------------------------------------------------------------
 * APPROACH 1 — Digit-by-digit product array (BEST)
 *   res[i+j] accumulates products of digit pairs, then a single carry
 *   pass normalizes every slot to a single digit.
 *   res has exactly len1 + len2 slots (max possible digit count).
 *   Time  Complexity : O(m · n)   Space Complexity : O(m + n)
 *   WHY it works: grade-school multiplication's carry lands in slot
 *   i+j+1, which is exactly the next positional slot — adding carries
 *   inside the same array is equivalent to the paper algorithm.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Row-by-row long multiplication (textbook form)
 *   Multiply num1 by EACH digit of num2, producing full partial rows
 *   ("123×6=738", "123×5=6150" shifted by one zero, ...), then add all
 *   rows together — literally what the paper algorithm draws.
 *   Time  Complexity : O(m · n + m · n) = O(m · n)  Space : O(m + n)
 *   Intuitive, but does two full passes (build rows, add rows).
 * ---------------------------------------------------------------------
 * DEEP DIVE — why grade-school multiplication is O(m·n) and correct
 *   num1 = Σ a_i·10^i  and  num2 = Σ b_j·10^j, so by distributivity:
 *       num1 × num2 = Σ_i Σ_j (a_i·b_j) · 10^(i+j)
 *   The product of digits a_i·b_j ∈ [0,81] lands in positional slot
 *   (i+j); overflow above 9 is a CARRY that belongs to slot (i+j+1)
 *   — exactly the next power of ten. This is why res[i+j] accumulation
 *   needs no intermediate rows: carries are just deferred, and one
 *   final left-to-right pass normalizes them. The i+j trick turns the
 *   "shifted row + add" textbook picture into a single O(m·n) sweep.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — digit strings
#include <vector>         // std::vector — product accumulator array
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // (unused here; kept for uniform include set)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Digit-by-digit product array with i+j accumulation
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Multiply two big numbers given as digit strings.
     * Inputs  : num1 — first non-negative integer as a string.
     *           num2 — second non-negative integer as a string.
     * Output  : std::string holding the exact product.
     */
    std::string multiply(const std::string& num1, const std::string& num2) {
        if (num1 == "0" || num2 == "0") return "0";
        const int m = static_cast<int>(num1.size());
        const int n = static_cast<int>(num2.size());

        // A product of an m-digit and an n-digit number has at most
        // m + n digits (e.g. 99×99 = 9801 has exactly 4 = 2+2).
        // res is indexed from the MOST significant end: index k holds
        // the digit of weight 10^(m+n-1-k).
        std::vector<int> res(m + n, 0);

        // Walk every digit PAIR exactly once — this is the O(m·n) core.
        for (int i = m - 1; i >= 0; --i) {
            const int a = num1[i] - '0';          // i-th digit (least significant first)
            for (int j = n - 1; j >= 0; --j) {
                const int b = num2[j] - '0';      // j-th digit

                // THE i+j+1 TRICK: digits at positions i and j (counted
                // from the left) produce a value of weight
                // 10^(m-1-i) × 10^(n-1-j) = 10^(m+n-2-i-j), which lands
                // exactly at index (m+n-1) − (m+n-2-i-j) = i+j+1.
                res[i + j + 1] += a * b;          // accumulate the pair product
            }
        }

        // Deferred carry sweep: every slot may hold up to 9×9×n < 10^3;
        // normalize from the right so each slot ends up a single digit.
        for (int k = m + n - 1; k > 0; --k) {
            res[k - 1] += res[k] / 10;
            res[k] %= 10;
        }

        // Drop leading zeros; "0×anything" must read exactly "0".
        int start = 0;
        while (start < m + n - 1 && res[start] == 0) ++start;

        // Slots hold digits most-significant-first → emit forward.
        std::string out;
        for (int i = start; i < m + n; ++i) {
            out.push_back(static_cast<char>('0' + res[i]));
        }
        return out;
    }
};

/* =====================================================================
 * APPROACH 2 : Row-by-row long multiplication (textbook form)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Multiply two big decimal strings the textbook way.
     * Inputs  : num1, num2 — non-negative integers as digit strings.
     * Output  : std::string holding the exact product.
     */
    std::string multiply(const std::string& num1, const std::string& num2) {
        if (num1 == "0" || num2 == "0") {
            return "0";
        }
        const int m = static_cast<int>(num1.size());
        const int n = static_cast<int>(num2.size());

        // res indexed from the LEAST significant end this time:
        // res[k] holds weight 10^k. Digit i of num1 has weight
        // 10^(m-1-i); digit j of num2 has weight 10^(n-1-j); their
        // product lands at index (m-1-i) + (n-1-j).
        std::vector<int> res(m + n, 0);

        for (int j = n - 1; j >= 0; --j) {
            const int b = num2[j] - '0';
            for (int i = m - 1; i >= 0; --i) {
                const int a = num1[i] - '0';
                const int idx = (m - 1 - i) + (n - 1 - j);  // weight exponent
                res[idx] += a * b;                          // accumulate
                res[idx + 1] += res[idx] / 10;              // immediate carry left
                res[idx] %= 10;
            }
        }

        // Strip leading zeros from the most significant end.
        int start = m + n - 1;
        while (start > 0 && res[start] == 0) {
            --start;
        }

        // res is least-significant-first → emit backwards.
        std::string out;
        for (int i = start; i >= 0; --i) {
            out.push_back(static_cast<char>('0' + res[i]));
        }
        return out;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 2-3 tests; time + peak RAM
 * ===================================================================== */
int main() {
    struct Test {
        std::string a;
        std::string b;
        std::string expected;
    };

    // Three fixed tests; expected values verified with a bignum library.
    const Test tests[] = {
        { "123", "456", "56088" },
        { "2", "3", "6" },
        { "9133", "0", "0" },
    };

    bool all_ok = true;

    // Helper lambda: time ONE solution on ONE test, print the line.
    const auto run_test = [&tests, &all_ok](const std::string& label, const auto& solve, int& ok_count) {
        // Run all 3 tests INSIDE one timed region so memory is shared.
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        const auto t0 = std::chrono::steady_clock::now();

        bool ok = true;
        for (const Test& t : tests) {
            const std::string got = solve(t.a, t.b);
            const bool pass = (got == t.expected);
            ok = ok && pass;
            std::cout << "  " << t.a << " \u00d7 " << t.b << " = " << got
                      << (pass ? "  PASS" : "  FAIL (want " + t.expected + ")")
                      << "\n";
        }

        const auto t1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);

        // microseconds (1e-6 s) for readability; ru_maxrss is KB on Linux.
        const double us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
        const long kb = after.ru_maxrss - before.ru_maxrss;
        std::cout << label << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " us  peak-mem = " << kb << " KB\n";
        if (ok) { ++ok_count; }
        all_ok = all_ok && ok;
    };

    std::cout << "Test suite: 3 fixed cases\n";
    int ok1 = 0, ok2 = 0;
    run_test("Approach 1 (digit-by-digit i+j array)", [](const std::string& a, const std::string& b) {
        return Solution_1().multiply(a, b);
    }, ok1);
    run_test("Approach 2 (row-by-row textbook)   ", [](const std::string& a, const std::string& b) {
        return Solution_2().multiply(a, b);
    }, ok2);

    // Only PASS when BOTH approaches clear all 3 tests.
    std::cout << (all_ok
                  ? "PASS : both approaches return the exact product on all tests."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}
