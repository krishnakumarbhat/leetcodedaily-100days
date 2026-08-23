/*
 * =====================================================================
 * LeetCode 125 : Valid Palindrome                                     (Easy)
 * https://leetcode.com/problems/valid-palindrome/
 * Category   : Two Pointers
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string s, return true if s is a PALINDROME after
 *   normalizing it: keep only alphanumeric characters and convert
 *   letters to lowercase. An empty string after normalization is a
 *   palindrome.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A palindrome reads identically from both ends. That symmetry is
 *   exactly what two pointers exploit: compare the leftmost relevant
 *   character against the rightmost relevant character, and if every
 *   such pair matches, the string is a palindrome. The O(n) scan is
 *   unavoidable because every character must be inspected at least
 *   once (any one of them could break the palindrome).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Two pointers with in-place normalization (BEST, O(1) space)
 *   l walks from the left, r from the right. Skip any non-alphanumeric
 *   character (punctuation, spaces) on either side, then compare
 *   tolower(s[l]) vs tolower(s[r]). Any mismatch → false; pointers
 *   meet at the center → true.
 *   Time  Complexity : O(n)  — each character visited once total.
 *   Space Complexity : O(1)  — no extra buffer; indices only.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Filter + reverse compare
 *   Build a cleaned string (keep alnum, lowercase), then check it
 *   against its reverse. Conceptually simplest — a palindrome equals
 *   its own reverse — but allocates a second copy of the string.
 *   Time  Complexity : O(n)  — one filter pass + one reverse pass.
 *   Space Complexity : O(n)  — the filtered copy (+ its reverse).
 * ---------------------------------------------------------------------
 * DEEP DIVE — what "alphanumeric" really costs
 *   std::isalnum / Python isalnum are NOT cheap single instructions:
 *   for the ASCII digits 0-9 the check is trivial, but for letters
 *   they consult the current C locale's classification table (a small
 *   array indexed by character). In C++ this is a per-character table
 *   lookup — still O(1) per character, so the overall O(n) bound
 *   survives. Mirroring the check on both sides (instead of cleaning
 *   the whole string first) is what buys Approach 1 its O(1) space:
 *   the normalization happens lazily, one character at a time.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing PASS/FAIL + benchmarks
#include <string>        // std::string — the input text
#include <vector>        // std::vector — the test-case table
#include <cctype>        // std::isalnum / std::tolower — normalization
#include <algorithm>     // std::reverse — used by approach 2
#include <chrono>        // std::chrono — high-resolution timing
#include <sys/resource.h>// getrusage — peak RAM measurement

/* =====================================================================
 * APPROACH 1 : Two pointers, skip junk on the fly (BEST)
 * ===================================================================== */
class Solution_TwoPointers {
public:
    /*
     * Purpose : Decide whether s is a palindrome ignoring case/junk.
     * Inputs  : s — the raw string, possibly with spaces/punctuation.
     * Output  : bool — true if normalized s reads the same both ways.
     */
    bool isPalindrome(const std::string& s) {
        int l = 0;
        int r = static_cast<int>(s.size()) - 1;

        while (l < r) {
            // Advance l past any character that does not count:
            // punctuation and spaces are invisible to the palindrome.
            while (l < r && !std::isalnum(static_cast<unsigned char>(s[l]))) {
                ++l;
            }
            // Same for r, coming from the right.
            while (l < r && !std::isalnum(static_cast<unsigned char>(s[r]))) {
                --r;
            }
            // Both pointers now sit on real letters/digits; compare them
            // case-insensitively. tolower makes 'A' and 'a' equal.
            if (std::tolower(static_cast<unsigned char>(s[l]))
                != std::tolower(static_cast<unsigned char>(s[r]))) {
                return false;
            }
            ++l;
            --r;
        }
        return true;
    }
};

/* =====================================================================
 * APPROACH 2 : Filter + compare against the reverse
 * ===================================================================== */
class Solution_FilterReverse {
public:
    /*
     * Purpose : Decide whether s is a palindrome ignoring case/junk.
     * Inputs  : s — the raw string, possibly with spaces/punctuation.
     * Output  : bool — true if normalized s reads the same both ways.
     */
    bool isPalindrome(const std::string& s) {
        // Build the normalized string: alnum only, lowercased.
        // Cost: O(n) work + O(n) memory for the copy.
        std::string clean;
        clean.reserve(s.size());
        for (char c : s) {
            if (std::isalnum(static_cast<unsigned char>(c))) {
                clean.push_back(static_cast<char>(std::tolower(static_cast<unsigned char>(c))));
            }
        }
        // A palindrome is a string equal to its own reverse — compare.
        std::string rev(clean.rbegin(), clean.rend());
        return clean == rev;
    }
};

/* =====================================================================
 * BENCHMARK — verify both solutions on real test cases + time/RAM
 * ===================================================================== */
int main() {
    // Case 1: official example — spaces/punct/case all ignored → true.
    // Case 2: near-palindrome; first comparison at the ends already fails.
    // Case 3: digits count as alphanumeric → true.
    struct TestCase { std::string s; bool expected; };
    std::vector<TestCase> tests = {
        {"A man, a plan, a canal: Panama", true},
        {"race a car", false},
        {"0P0", true}
    };

    // Aggregate time + peak-RAM across all cases, per approach.
    long time_us[2] = {0, 0};
    long peak_kb[2] = {0, 0};
    bool allPass = true;

    for (size_t t = 0; t < tests.size(); ++t) {
        struct rusage before, after;
        bool r1, r2;

        // --- Approach 1: time + peak memory (ru_maxrss is KB on Linux) ---
        getrusage(RUSAGE_SELF, &before);
        auto s1 = std::chrono::steady_clock::now();
        r1 = Solution_TwoPointers().isPalindrome(tests[t].s);
        auto e1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        time_us[0] += std::chrono::duration_cast<std::chrono::nanoseconds>(e1 - s1).count() / 1000;
        peak_kb[0] = std::max(peak_kb[0], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        // --- Approach 2: same instrumentation ---
        getrusage(RUSAGE_SELF, &before);
        auto s2 = std::chrono::steady_clock::now();
        r2 = Solution_FilterReverse().isPalindrome(tests[t].s);
        auto e2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after);
        time_us[1] += std::chrono::duration_cast<std::chrono::nanoseconds>(e2 - s2).count() / 1000;
        peak_kb[1] = std::max(peak_kb[1], static_cast<long>(after.ru_maxrss - before.ru_maxrss));

        bool ok = (r1 == tests[t].expected) && (r2 == tests[t].expected);
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << ": twoPtr=" << (r1 ? "true" : "false")
                  << " filter=" << (r2 ? "true" : "false")
                  << " expected=" << (tests[t].expected ? "true" : "false")
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "---\n"
              << "Approach 1 (two pointers)     : " << time_us[0] << " µs total, peak " << peak_kb[0] << " KB\n"
              << "Approach 2 (filter + reverse) : " << time_us[1] << " µs total, peak " << peak_kb[1] << " KB\n"
              << (allPass ? "PASS : all cases" : "FAIL : at least one case") << "\n";
    return allPass ? 0 : 1;
}
