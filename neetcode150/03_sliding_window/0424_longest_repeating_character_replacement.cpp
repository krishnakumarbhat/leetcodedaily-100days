/*
 * =====================================================================
 * LeetCode 424 : Longest Repeating Character Replacement      (Medium)
 * https://leetcode.com/problems/longest-repeating-character-replacement/
 * Category   : Sliding Window
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string `s` of UPPERCASE letters and an integer `k`, you
 *   may change AT MOST k characters anywhere in the string. Return
 *   the length of the longest substring that can be made to contain
 *   ONLY ONE distinct character after those ≤ k changes.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A window [l, r] can be made uniform in ≤ k changes iff
 *       (window length) − (most frequent char count) ≤ k
 *   The left side counts "mismatched" characters — the ones that
 *   must be rewritten. The most frequent character is the one we
 *   KEEP; everything else gets converted into it.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sliding window + running max frequency (BEST)
 *   count[26] tracks letter frequencies inside [l, r]. maxFreq is
 *   the max over ALL history — it never decreases, which is legal
 *   because the answer window only ever grows in our favour when a
 *   future char matches the historical max. When the invariant
 *   (len − maxFreq > k) breaks, shrink l. maxLen = max window seen.
 *   Time  Complexity : O(n)  — each char enters & leaves once
 *   Space Complexity : O(26) = O(1) — fixed count array
 * ---------------------------------------------------------------------
 * APPROACH 2 — Brute force (every start, expand while valid)
 *   For each start index i, expand j while the ≤ k condition holds
 *   using a fresh per-window count. Correct, but restarts all state
 *   for every i.
 *   Time  Complexity : O(n²) — worst case when k is large
 *   Space Complexity : O(26) = O(1)
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — count[26] vs dict, and the maxFreq trick
 *   The alphabet is exactly 26 uppercase letters → int count[26]
 *   indexed by (c − 'A') beats any hash map: no hashing, one
 *   contiguous 104-byte array, perfect cache locality. A Python dict
 *   (open addressing, linear probing: h(k, i) = (hash(k)+i) mod m)
 *   would be correct but slower for a fixed 26-key universe.
 *   WHY maxFreq never shrinks: maxLen = r − l + 1 is monotone, and
 *   if maxFreq is stale-high, the check (len − maxFreq > k) only
 *   becomes HARDER to pass — we shrink earlier, which is safe; it
 *   can never cause us to overstate maxLen because any window that
 *   passed with a stale-high maxFreq also passes with the true one.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — the input text
#include <vector>         // std::vector — test-case storage
#include <algorithm>      // std::max — running maximum updates
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement (KB)

/* =====================================================================
 * APPROACH 1 : Sliding window + running max frequency (O(n))
 * ===================================================================== */
class Solution_SlidingWindow {
public:
    /*
     * Purpose : Return the longest substring of `s` that can become
     *           uniform after changing at most `k` characters.
     * Inputs  : s — uppercase-letter string to scan.
     *           k — maximum allowed character replacements.
     * Output  : int — length of the longest fixable substring.
     */
    int characterReplacement(const std::string& s, int k) {
        // count : letter frequencies inside the current window.
        int count[26] = {0};
        int l = 0;       // left edge of the window
        int maxFreq = 0; // largest frequency EVER seen in any window
        int maxLen = 0;  // best answer so far

        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
            // Expand: this char's frequency grows by one.
            const int idx = s[r] - 'A';   // 'A'→0 … 'Z'→25
            ++count[idx];
            // maxFreq only ever grows — see the deep dive above for
            // why re-using the historical max is sound.
            maxFreq = std::max(maxFreq, count[idx]);

            // Invariant: window can be uniform in ≤ k changes.
            // If violated, shrink l until it holds again.
            while (r - l + 1 - maxFreq > k) {
                const int out = s[l] - 'A';
                --count[out];   // evicted char leaves the window
                ++l;
            }
            // Window is valid again → candidate for the answer.
            maxLen = std::max(maxLen, r - l + 1);
        }
        return maxLen;
    }
};

/* =====================================================================
 * APPROACH 2 : Brute force — every start index, expand while valid
 * ===================================================================== */
class Solution_BruteForce {
public:
    /*
     * Purpose : Return the longest substring of `s` that can become
     *           uniform after changing at most `k` characters.
     * Inputs  : s — uppercase-letter string to scan.
     *           k — maximum allowed character replacements.
     * Output  : int — length of the longest fixable substring.
     */
    int characterReplacement(const std::string& s, int k) {
        int maxLen = 0;

        // Start index i fixes the window's left edge.
        for (int i = 0; i < static_cast<int>(s.size()); ++i) {
            int count[26] = {0};  // fresh counters per start
            int maxFreq = 0;
            // Expand j while the ≤ k invariant still holds.
            for (int j = i; j < static_cast<int>(s.size()); ++j) {
                const int idx = s[j] - 'A';
                ++count[idx];
                maxFreq = std::max(maxFreq, count[idx]);
                // j−i+1 − maxFreq = chars we would have to rewrite.
                if (j - i + 1 - maxFreq <= k) {
                    maxLen = std::max(maxLen, j - i + 1);
                } else {
                    break;  // shrinking j would only repeat shorter
                }
            }
        }
        return maxLen;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests + a longer string,
 * compare time and peak RAM, print PASS/FAIL per case.
 * ===================================================================== */
int main() {
    const std::vector<std::tuple<std::string, int, int>> tests = {
        {"ABAB", 2, 4},       // official: whole string → "AAAA"
        {"AABABBA", 1, 4},    // official: answer is "AABAB"→"AABBB"… best 4
        {"AAAB", 0, 3}        // k=0 → longest run of identical chars
    };

    bool allPass = true;
    for (const auto& t : tests) {
        const int r1 = Solution_SlidingWindow().characterReplacement(std::get<0>(t), std::get<1>(t));
        const int r2 = Solution_BruteForce().characterReplacement(std::get<0>(t), std::get<1>(t));
        const bool ok = r1 == std::get<2>(t) && r2 == std::get<2>(t);
        allPass = allPass && ok;
        std::cout << (ok ? "PASS " : "FAIL ")
                  << "s=\"" << std::get<0>(t) << "\" k=" << std::get<1>(t)
                  << " expected=" << std::get<2>(t)
                  << "  window=" << r1 << "  brute=" << r2 << "\n";
    }

    // Longer string mixing long A-runs with filler, k=5.
    std::string bench;
    for (int i = 0; i < 500; ++i) {
        bench.append("AAAA");      // fat A-run
        bench.append("BCDEF");     // mismatches to be replaced
    }

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    const int b1 = Solution_SlidingWindow().characterReplacement(bench, 5);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    const double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    const long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss; // KB on Linux

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    const int b2 = Solution_BruteForce().characterReplacement(bench, 5);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    const double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    const long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (sliding window) : result=" << b1
              << "  time=" << us_1 << " µs  peak-ram-delta=" << mem_1 << " KB\n";
    std::cout << "Approach 2 (brute force)    : result=" << b2
              << "  time=" << us_2 << " µs  peak-ram-delta=" << mem_2 << " KB\n";

    // Brute force is the ground truth; the O(n) pass must match it.
    allPass = allPass && (b1 == b2);
    std::cout << (allPass ? "PASS : all test cases and benchmark agree."
                          : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}