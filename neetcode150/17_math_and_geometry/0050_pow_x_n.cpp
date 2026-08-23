/*
 * =====================================================================
 * LeetCode 50 : Pow(x, n)                                        (Medium)
 * https://leetcode.com/problems/powx-n/
 * Category   : Math & Geometry
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Implement pow(x, n) — raise a floating point x to an integer
 *   power n (n can be negative, down to -2^31). No std::pow.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Multiplying x by itself n times is O(n) — too slow for n = 10^9.
 *   KEY OBSERVATION: x^8 = x^4 · x^4 = (x^2)^4 ... squaring halves
 *   the exponent each step. This is "exponentiation by squaring":
 *   x^n = (x^(n/2))² for even n, and x^n = x · (x^((n-1)/2))² for odd.
 *   Each step halves n → only O(log n) multiplications.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative exponentiation by squaring (BEST)
 *   Sweep the bits of n from least significant: keep a running
 *   base = x^(2^k); whenever bit k of n is set, multiply into result.
 *   Negative n is handled by inverting x at the start and negating n.
 *   Time  Complexity : O(log n)   Space Complexity : O(1)
 *   WHY it works: x^n = ∏ x^(2^k) over all set bits k of n — the
 *   binary expansion of n picks exactly which squares multiply.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive halving
 *   pow(x, n): if n is even → p = pow(x, n/2); return p·p.
 *              if n is odd  → return x · pow(x, n-1) (or (n/2)²·x).
 *   Same O(log n) multiplications, but the recursion depth is log n
 *   and the call stack costs O(log n) memory.
 *   Time  Complexity : O(log n)   Space Complexity : O(log n)
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the recurrence is correct
 *   The recurrence is:  pow(x, n) = pow(x, n/2)²          (n even)
 *                       pow(x, n) = x · pow(x, n/2)²      (n odd, integer div)
 *   because n = 2k ⇒ x^n = (x^k)², and n = 2k+1 ⇒ x^n = x·(x^k)².
 *   Subtlety: exponent n = -2^31 cannot be negated in a signed 32-bit
 *   int (overflow!). Safe pattern: if n < 0, return 1.0 / pow(x, -n)
 *   using a LONG (64-bit) negated exponent. Doubles need no overflow
 *   worries — multiplication and division are IEEE-754 exact enough.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — formatting result lines
#include <vector>         // std::vector — (unused; uniform include set)
#include <unordered_map>  // (unused here; kept for uniform include set)
#include <unordered_set>  // (unused here; kept for uniform include set)
#include <chrono>         // std::chrono — steady_clock timing
#include <sys/resource.h> // getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Iterative exponentiation by squaring (bit sweep)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Compute x raised to the integer power n.
     * Inputs  : x — base (double, may be any finite value).
     *           n — exponent (int, may be negative).
     * Output  : double approximation of x^n.
     */
    double myPow(double x, int n) {
        // Use a 64-bit exponent: -INT_MIN would overflow a 32-bit int,
        // but it fits perfectly in a long.
        long long exp = n;

        // Negative exponent = reciprocal of the positive-power result.
        // We invert x instead of negating exp at the end — cheaper and
        // avoids a second pass. (exp is made positive below.)
        if (exp < 0) {
            x = 1.0 / x;
            exp = -exp;
        }

        double result = 1.0;
        double base = x;   // base = x^(2^k) as k grows with each bit

        // Sweep every bit of |exp|, least significant first.
        while (exp > 0) {
            // If bit k of exp is set, x^(2^k) must be multiplied in.
            if (exp % 2 == 1) {
                result *= base;
            }
            base *= base;   // square: x^(2^k) → x^(2^(k+1))
            exp /= 2;       // move to the next bit (halve the exponent)
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive halving (same math, O(log n) stack)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Compute x^n via the halving recurrence.
     * Inputs  : x — base (double); n — exponent (int, may be negative).
     * Output  : double approximation of x^n.
     */
    double myPow(double x, int n) {
        if (n == 0) {
            return 1.0;                 // x^0 = 1 for any x
        }

        // Negative exponent → reciprocal, computed recursively with a
        // long so INT_MIN negates safely.
        if (n < 0) {
            return 1.0 / myPow(x, -static_cast<long long>(n));
        }

        // Halve: p = x^(n/2) (integer division floors odd n).
        const double p = myPow(x, n / 2);

        // n even → x^n = (x^(n/2))² ; n odd → multiply one extra x.
        return (n % 2 == 0) ? p * p : p * p * x;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests; time + peak RAM
 * ===================================================================== */
int main() {
    // (x, n, expected) — expected verified against std::pow upstream.
    const double tests[][3] = {
        { 2.0, 10, 1024.0 },
        { 2.1, 3, 9.261 },
        { 2.0, -2, 0.25 },
    };

    bool all_ok = true;

    const auto run_all = [&](const std::string& label, const auto& solve) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        const auto t0 = std::chrono::steady_clock::now();

        bool ok = true;
        for (const auto& t : tests) {
            const double got = solve(t[0], static_cast<int>(t[1]));
            // Relative tolerance: IEEE-754 squaring chains drift by ~1e-15.
            const double rel = (t[2] != 0.0) ? (got - t[2]) / t[2] : got;
            const bool pass = rel > -1e-9 && rel < 1e-9;
            ok = ok && pass;
            std::cout << "  " << t[0] << "^" << static_cast<long long>(t[1]) << " = "
                      << got << (pass ? "  PASS" : "  FAIL (want " + std::to_string(t[2]) + ")") << "\n";
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
    run_all("Approach 1 (iterative bit sweep)   ", [](double x, int n) {
        return Solution_1().myPow(x, n);
    });
    run_all("Approach 2 (recursive halving)     ", [](double x, int n) {
        return Solution_2().myPow(x, n);
    });

    std::cout << (all_ok
                  ? "PASS : both approaches match the expected powers on all tests."
                  : "FAIL : at least one test failed.") << "\n";
    return all_ok ? 0 : 1;
}
