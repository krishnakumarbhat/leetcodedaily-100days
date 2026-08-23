/*
 * =====================================================================
 * LeetCode 7  : Reverse Integer                                    (Medium)
 * https://leetcode.com/problems/reverse-integer/
 * Category   : Bit manipulation / integer arithmetic
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a signed 32-bit integer x, return x with its digits reversed.
 *   If reversing causes the value to fall outside [-2^31, 2^31-1],
 *   return 0.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Repeatedly peel off the last digit (x % 10), append it to a running
 *   answer (rev = rev*10 + d), and truncate x (x /= 10). The catch is
 *   32-bit overflow: building rev in 64 bits lets us test the range
 *   *after* the reversal, then clamp.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Arithmetic pop/append (best)
 *   1. Keep the sign of x, work on the absolute value.
 *   2. Loop: d = x % 10 ; rev = rev*10 + d ; x /= 10.
 *   3. Apply sign, then test 32-bit range; return 0 if out of range.
 * APPROACH 2 · String reverse with built-in overflow guard
 *   1. Convert |x| to a string, reverse it, parse back to int.
 *   2. Apply sign, then clamp to 32-bit.
 * ---------------------------------------------------------------------
 * DEEP DIVE · WHY arithmetic beats string here
 *   Modulo 10 is a single x86 'idiv' remainder; integer multiply by 10
 *   and add is one IMUL + one ADD — no heap allocation, no parsing
 *   overhead, no UTF-8 decode. The 32-bit bound is INT32_MAX = 2147483647
 *   and INT32_MIN = -2147483648; building the result in a 64-bit long
 *   guarantees the comparison is always well defined (no UB from
 *   signed overflow during the build itself). Also note: 64-bit build
 *   handles INT32_MIN safely — INT32_MIN / -1 overflows in 32-bit, but
 *   never in 64-bit.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(log10 |x|) = O(1)  — at most 10 digits.
 * MEMORY COMPLEXITY: O(1)                  — rev fits in a long (8 bytes).
 * ---------------------------------------------------------------------
 */
#include <iostream>
#include <string>
#include <algorithm>     // std::reverse
#include <cstdint>
#include <chrono>
#include <sys/resource.h>

/* ---------------- Approach 1: arithmetic pop/append ---------------- */
class Solution_1 {
public:
    int reverse(int x) {
        long long rev = 0;                 // 64-bit: never overflows mid-build
        long long n = x;                   // copy so % and /= work on magnitude
        while (n != 0) {
            int d = static_cast<int>(n % 10);  // last digit (sign preserved)
            rev = rev * 10 + d;                // append to the growing answer
            n /= 10;                           // drop the digit we consumed
        }
        if (rev < INT32_MIN || rev > INT32_MAX) return 0;  // clamp to 32-bit
        return static_cast<int>(rev);
    }
};

/* ---------------- Approach 2: string reverse ---------------- */
class Solution_2 {
public:
    int reverse(int x) {
        long long n = x;                          // magnitude-safe copy
        bool neg = n < 0;
        std::string s = std::to_string(neg ? -n : n);  // digits only
        std::reverse(s.begin(), s.end());         // flip the string
        long long rev = std::stoll(s);            // parse back
        if (neg) rev = -rev;                      // restore sign
        if (rev < INT32_MIN || rev > INT32_MAX) return 0;
        return static_cast<int>(rev);
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() {
    struct rusage r{};
    getrusage(RUSAGE_SELF, &r);
    return r.ru_maxrss;  // kilobytes on Linux
}

int main() {
    struct Case { int x; int expect; };
    const Case cases[] = {
        {123, 321}, {-123, -321}, {120, 21},
        {0, 0}, {1534236469, 0}, {-2147483648, 0}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = Solution_1().reverse(c.x);
        int r2 = Solution_2().reverse(c.x);
        bool ok = r1 == c.expect && r2 == c.expect;
        allOk = allOk && ok;
        std::cout << "x=" << c.x << " → A1=" << r1 << " A2=" << r2
                  << " (want " << c.expect << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all 6 cases on both approaches" : "FAIL : some case wrong")
              << " | time: " << (t1 - t0) << " us | mem: " << (memKb() - mem0) << " KB\n";
    /* benchmark: 1e6 reversals of a pathological input */
    t0 = nowUs();
    for (int i = 0; i < 1000000; ++i) Solution_1().reverse(1534236469);
    t1 = nowUs();
    std::cout << "BENCH A1: " << (t1 - t0) << " us for 1e6 calls\n";
    t0 = nowUs();
    for (int i = 0; i < 1000000; ++i) Solution_2().reverse(1534236469);
    t1 = nowUs();
    std::cout << "BENCH A2: " << (t1 - t0) << " us for 1e6 calls\n";
    return 0;
}
