/*
 * =====================================================================
 * LeetCode 201 : Bitwise AND of Numbers Range                       (Medium)
 * https://leetcode.com/problems/bitwise-and-of-numbers-range/
 * Category   : Math / bit manipulation
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Bitwise AND of EVERY integer in [left, right] inclusive.
 * ---------------------------------------------------------------------
 * INTUITION
 *   For a bit position to be 1 in the result, ALL numbers in the
 *   range must share that bit — i.e. the common PREFIX of left and
 *   right. Everything past the first differing bit flips in between,
 *   killing it. So: right &= right-1 repeatedly until right ≤ left,
 *   or equivalently shift both until equal, then shift back.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Clear trailing bits (best)
 *   while left < right: right &= right - 1  → right is now the common
 *   prefix of the two endpoints.
 * APPROACH 2 · Shift-and-compare
 *   shift = 0; while left != right: left >>= 1, right >>= 1, shift++.
 *   Answer = left << shift.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why the common prefix is the answer
 *   left and right agree on the leading bits; at the first bit where
 *   they differ, the range contains a number with a 0 there (the
 *   "carry boundary"), and below that bit the range covers every
 *   combination — so those lower bits are all 0 in the AND. The
 *   prefix bits are constant across the range, hence survive.
 *   right & (right-1) clears exactly the lowest set bit — repeating
 *   it converges to the largest prefix ≤ right that is a prefix of
 *   left... the loop stops when right ≤ left, and with right ≥ left
 *   (invariant) it lands on the prefix itself.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(1) — ≤ 31 iterations.
 * MEMORY COMPLEXITY: O(1).
 * =====================================================================
 */
#include <iostream>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    int rangeBitwiseAnd(int left, int right) {
        while (left < right) right &= right - 1;   // clear lowest set bit
        return right;                              // = common prefix
    }
};

class Solution_2 {
public:
    int rangeBitwiseAnd(int left, int right) {
        int shift = 0;
        while (left != right) {                    // find common prefix
            left >>= 1;
            right >>= 1;
            ++shift;
        }
        return left << shift;                      // shift the prefix back
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { int l, r, want; };
    const Case cases[] = {
        {5, 7, 4},
        {0, 0, 0},
        {1, 2147483647, 0},
        {1073741824, 2147483646, 1073741824}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = Solution_1().rangeBitwiseAnd(c.l, c.r);
        int r2 = Solution_2().rangeBitwiseAnd(c.l, c.r);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "[" << c.l << "," << c.r << "] → A1=" << r1 << " A2=" << r2
                  << " (want " << c.want << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
