/*
 * =====================================================================
 * LeetCode 395 : Longest Substring with At Least K Repeating Chars  (Medium)
 * https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/
 * Category   : Backtracking / divide and conquer
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Longest substring where EVERY character appears at least k times.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A character appearing fewer than k times in a window can NEVER be
 *   part of a valid substring — it splits the string into independent
 *   sub-problems. Recurse on the pieces between such "blocker" chars.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Divide & conquer on blockers (best)
 *   Count chars in s. If every count ≥ k → whole string is valid.
 *   Else split at every char with count < k and recurse each piece.
 * APPROACH 2 · Sliding window per distinct-count (classic two-pointer)
 *   For c in 1..26: longest window containing ≤ c distinct chars with
 *   all counts ≥ k. O(26·n).
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why blockers split the problem cleanly
 *   Suppose 'x' occurs 3 times in s with count 2 < k. Any valid
 *   substring can't include x; hence it lies fully inside one of the
 *   gaps between x's. The gaps are independent — recursion on each is
 *   correct and the answer is the max. Termination: every level cuts
 *   at least one character out, so depth ≤ 26·level. A1 is elegant
 *   but worst-case O(n²); A2 (26 sliding-window passes) is O(26n) and
 *   is the interview-safe alternative.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : A1 O(n²) worst; A2 O(26·n) = O(n).
 * MEMORY COMPLEXITY: O(n) recursion / window counters.
 * =====================================================================
 */
#include <iostream>
#include <string>
#include <array>
#include <algorithm>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::string* s_;
    int k_;
    int solve(int l, int r) {
        if (r - l + 1 < k_) return 0;
        std::array<int, 26> cnt{};
        for (int i = l; i <= r; ++i) ++cnt[(*s_)[i] - 'a'];
        bool valid = true;
        for (int c : cnt) if (c && c < k_) valid = false;
        if (valid) return r - l + 1;
        int best = 0, start = l;
        for (int i = l; i <= r; ++i) {
            if (cnt[(*s_)[i] - 'a'] < k_) {          // blocker char
                best = std::max(best, solve(start, i - 1));
                start = i + 1;
            }
        }
        return std::max(best, solve(start, r));
    }
public:
    int longestSubstring(std::string s, int k) {
        s_ = &s;
        k_ = k;
        return solve(0, static_cast<int>(s.size()) - 1);
    }
};

class Solution_2 {
public:
    int longestSubstring(std::string s, int k) {
        int n = static_cast<int>(s.size()), best = 0;
        for (int distinct = 1; distinct <= 26; ++distinct) {
            std::array<int, 26> cnt{};
            int uniq = 0, okCnt = 0;                  // unique & all≥k chars
            for (int l = 0, r = 0; r < n; ++r) {
                if (cnt[s[r] - 'a']++ == 0) ++uniq;
                if (cnt[s[r] - 'a'] == k) ++okCnt;
                while (uniq > distinct) {             // too many letters
                    int c = s[l++] - 'a';
                    if (cnt[c]-- == k) --okCnt;
                    if (cnt[c] == 0) --uniq;
                }
                if (uniq == okCnt) best = std::max(best, r - l + 1);
            }
        }
        return best;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::string s; int k; int want; };
    const Case cases[] = {
        {"aaabb", 3, 3},      // "aaa"
        {"ababbc", 2, 5},     // "ababb"
        {"ababacb", 3, 0},
        {"a", 1, 1}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = Solution_1().longestSubstring(c.s, c.k);
        int r2 = Solution_2().longestSubstring(c.s, c.k);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "\"" << c.s << "\" k=" << c.k << " → A1=" << r1 << " A2=" << r2
                  << " (want " << c.want << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
