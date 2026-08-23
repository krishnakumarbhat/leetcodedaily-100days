/*
 * =====================================================================
 * LeetCode 3 : Longest Substring Without Repeating Characters  (Medium)
 * https://leetcode.com/problems/longest-substring-without-repeating-characters/
 * Category   : Sliding Window
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string `s`, return the length of the LONGEST substring
 *   (contiguous slice) that contains NO repeating characters.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A window [l, r] is valid ⇔ all its characters are distinct.
 *   When s[r] duplicates a character already inside the window, the
 *   window cannot grow — so we shrink from the left until the
 *   duplicate is evicted. Both pointers move monotonically: r
 *   advances n times, l advances at most n times → O(n) amortized.
 *   This is THE canonical sliding-window pattern: expand right, fix
 *   the invariant by shrinking left, record the window size.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sliding window + hash set (shrink step-by-step)
 *   Keep a set of characters currently inside [l, r]. When s[r]
 *   collides with the set, evict s[l] and l++ until the duplicate
 *   is gone. Then insert s[r] and record maxLen = max(maxLen, r-l+1).
 *   Time  Complexity : O(n)   — every char enters AND leaves once
 *   Space Complexity : O(min(n, m)) — m = alphabet size (≤ 128 ASCII)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sliding window + last-seen index map (JUMP past dupe)
 *   Store each character's most recent index. On a duplicate at r,
 *   l can JUMP straight to lastSeen[s[r]] + 1 instead of evicting
 *   char-by-char. Handles repeated collisions in O(1) per step.
 *   Time  Complexity : O(n)   — single pass, O(1) map ops
 *   Space Complexity : O(min(n, m))
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — set/map vs fixed count array
 *   C++ std::unordered_map / unordered_set = separate chaining:
 *   each bucket is a linked list of colliding keys, O(1) average
 *   per op. std::map = red-black BST with O(log n) ops — only for
 *   ordered iteration / range queries, never needed here.
 *   Python dict/set = open addressing with LINEAR PROBING:
 *       h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...   (m = table size)
 *   When the alphabet is ASCII (≤ 128 characters) a fixed array
 *   (bool count[128] or int lastSeen[128]) is strictly faster:
 *   ZERO hashing, 128×4 contiguous bytes, perfect cache locality.
 *   For full Unicode, hash maps keyed on code points are required —
 *   a 128-slot array indexes only the FIRST byte of a multi-byte
 *   UTF-8 character and silently produces wrong answers.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — the input text
#include <vector>         // std::vector — test-case storage
#include <unordered_set>  // std::unordered_set — approach 1 window set
#include <unordered_map>  // std::unordered_map — approach 2 index map
#include <algorithm>      // std::max — updating the running maximum
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement (KB)

/* =====================================================================
 * APPROACH 1 : Sliding window + hash set (evict one char at a time)
 * ===================================================================== */
class Solution_SetEviction {
public:
    /*
     * Purpose : Return the length of the longest substring of `s`
     *           that contains no repeated characters.
     * Inputs  : s — the string to scan.
     * Output  : int — length of the longest valid substring.
     */
    int lengthOfLongestSubstring(const std::string& s) {
        // window : chars currently inside the [l, r] slice. Membership
        // tests are O(1) average — the whole trick of this approach.
        std::unordered_set<char> window;
        int l = 0;            // left edge of the window (shrinks)
        int maxLen = 0;       // best valid length seen so far

        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
            // s[r] breaks the "all distinct" invariant → shrink the
            // left edge until the duplicate char is evicted. Every
            // erased char is erased exactly once → O(n) total work.
            while (window.count(s[r]) != 0) {
                window.erase(s[l]);
                ++l;
            }
            // Invariant restored → s[r] may now join the window.
            window.insert(s[r]);
            // [l, r] is valid by construction → candidate for the best.
            maxLen = std::max(maxLen, r - l + 1);
        }
        return maxLen;
    }
};

/* =====================================================================
 * APPROACH 2 : Sliding window + last-seen index map (jump past dupe)
 * ===================================================================== */
class Solution_IndexJump {
public:
    /*
     * Purpose : Return the length of the longest substring of `s`
     *           that contains no repeated characters.
     * Inputs  : s — the string to scan.
     * Output  : int — length of the longest valid substring.
     */
    int lengthOfLongestSubstring(const std::string& s) {
        // lastSeen : char -> most recent index where it appeared.
        // Values < l are stale — the map entry may predate the window.
        std::unordered_map<char, int> lastSeen;
        int l = 0;            // left edge of the window
        int maxLen = 0;       // best valid length seen so far

        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
            // If s[r] was seen INSIDE the current window, every index
            // ≤ that sighting is now poisoned → l jumps over it in
            // one step instead of evicting char-by-char.
            auto it = lastSeen.find(s[r]);
            if (it != lastSeen.end() && it->second >= l) {
                l = it->second + 1;
            }
            // Record this sighting; later duplicates use it to jump.
            lastSeen[s[r]] = r;
            // [l, r] is valid by construction → candidate for the best.
            maxLen = std::max(maxLen, r - l + 1);
        }
        return maxLen;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests + a longer string,
 * compare time and peak RAM, print PASS/FAIL per case.
 * ===================================================================== */
int main() {
    // Fixed official examples — the real acceptance criteria.
    const std::vector<std::pair<std::string, int>> tests = {
        {"abcabcbb", 3},  // "abc"        — classic triple repeat
        {"bbbbb", 1},     // "b"          — all identical
        {"pwwkew", 3}     // "wke"        — answer is a middle window
    };

    bool allPass = true;
    for (const auto& t : tests) {
        const int r1 = Solution_SetEviction().lengthOfLongestSubstring(t.first);
        const int r2 = Solution_IndexJump().lengthOfLongestSubstring(t.first);
        const bool ok = r1 == t.second && r2 == t.second;
        allPass = allPass && ok;
        std::cout << (ok ? "PASS " : "FAIL ")
                  << "s=\"" << t.first << "\" expected=" << t.second
                  << "  set=" << r1 << "  jumpMap=" << r2 << "\n";
    }

    // Longer mixed-case string so the benchmark is not trivially fast
    // and both maps actually grow.
    const std::string bench = "abcabcbbdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                              "0123456789aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz";

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    const int b1 = Solution_SetEviction().lengthOfLongestSubstring(bench);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    // Convert nanoseconds to microseconds for human-friendly output.
    const double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    // ru_maxrss is cumulative peak → the DELTA is what this run consumed.
    const long mem_1 = (after_1.ru_maxrss - before_1.ru_maxrss); // already KB on Linux

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    const int b2 = Solution_IndexJump().lengthOfLongestSubstring(bench);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    const double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    const long mem_2 = (after_2.ru_maxrss - before_2.ru_maxrss);

    std::cout << "Approach 1 (set eviction)  : result=" << b1
              << "  time=" << us_1 << " µs  peak-ram-delta=" << mem_1 << " KB\n";
    std::cout << "Approach 2 (index jump)    : result=" << b2
              << "  time=" << us_2 << " µs  peak-ram-delta=" << mem_2 << " KB\n";

    // Both approaches must agree with each other on the big string too.
    allPass = allPass && (b1 == b2);
    std::cout << (allPass ? "PASS : all test cases and benchmark agree."
                          : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}
