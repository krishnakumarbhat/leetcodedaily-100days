/*
 * =====================================================================
 * LeetCode 76 : Minimum Window Substring                        (Hard)
 * https://leetcode.com/problems/minimum-window-substring/
 * Category   : Sliding Window
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given strings `s` and `t`, return the SHORTEST substring of `s`
 *   that contains EVERY character of `t` (including duplicates), or
 *   "" if no such window exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Contains all of t" is a COUNTING condition, not an order
 *   condition. Define required = number of DISTINCT chars in t and
 *   track formed  = how many of those chars the window currently
 *   satisfies. When formed == required the window is valid — then
 *   greedily shrink from the left while validity holds, because a
 *   shorter window can only come from shrinking a valid one.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Sliding window + two hash maps (formed/required)
 *   Grow r. When window count of s[r] reaches t's requirement,
 *   formed++. While formed == required: record candidate window,
 *   then shrink l (decrement count; if it drops below the
 *   requirement, formed--).
 *   Time  Complexity : O(n + m) — n = |s|, m = |t|, each char O(1)
 *   Space Complexity : O(m)     — maps hold ≤ |t| distinct chars
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sliding window + 128-slot count arrays (no hashing)
 *   Same logic, but need[128] / windowCount[128] indexed by char
 *   code. Indexing is O(1) with ZERO hash cost and O(1) space
 *   because the alphabet is bounded (ASCII). matched tracks how
 *   many chars meet their quota, mirroring formed/required.
 *   Time  Complexity : O(n + m) — same, with a smaller constant
 *   Space Complexity : O(1)     — fixed 128×2 ints, no allocation
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — count array vs hash map
 *   unordered_map<char,int> (C++): separate chaining, O(1) average,
 *   memory proportional to DISTINCT chars in t — good when |Σ| is
 *   huge/unknown (Unicode).
 *   int count[128] (or 256): O(1) worst case, contiguous memory,
 *   cache-perfect, zero hashing — strictly better for ASCII input,
 *   which is what LeetCode provides. Python dict is open addressing
 *   with linear probing: h(k, i) = (hash(k) + i) mod m — correct
 *   but wasteful when the alphabet is a known fixed size.
 *   The formed/required trick matters more than the container:
 *   it turns a full "does window ⊇ t?" scan (O(Σ) per step) into
 *   O(1) bookkeeping per character movement.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — the input texts
#include <vector>         // std::vector — test-case storage
#include <unordered_map>  // std::unordered_map — approach 1 counters
#include <climits>        // INT_MAX — "no window found yet" sentinel
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement (KB)

/* =====================================================================
 * APPROACH 1 : Sliding window + two hash maps (formed/required)
 * ===================================================================== */
class Solution_HashMaps {
public:
    /*
     * Purpose : Return the shortest substring of `s` containing every
     *           character of `t` (with multiplicities), or "" if none.
     * Inputs  : s — the haystack to search inside.
     *           t — the needle whose character counts must be matched.
     * Output  : std::string — the minimum window, or empty string.
     */
    std::string minWindow(const std::string& s, const std::string& t) {
        if (s.empty() || t.empty()) {
            return "";  // nothing to match or nowhere to look
        }

        // need : t's character requirements (target counts).
        std::unordered_map<char, int> need;
        for (char c : t) {
            ++need[c];
        }
        // required = number of DISTINCT characters that must be satisfied.
        const int required = static_cast<int>(need.size());
        // windowCount : counts currently inside [l, r].
        std::unordered_map<char, int> windowCount;

        int formed = 0;               // how many chars have met their quota
        int ansLen = INT_MAX;         // best (smallest) window length so far
        int ansL = 0;                 // left edge of the best window
        int l = 0;                    // left edge of the CURRENT window

        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
            // Expand: s[r] enters the window.
            const char c = s[r];
            ++windowCount[c];

            // Did this expansion push exactly one char to its quota?
            auto it = need.find(c);
            if (it != need.end() && windowCount[c] == it->second) {
                ++formed;
            }

            // Window is valid → try to shrink for a smaller window.
            while (formed == required) {
                // Candidate: [l, r] is valid and as short as possible
                // AFTER the previous shrinks.
                const int len = r - l + 1;
                if (len < ansLen) {
                    ansLen = len;
                    ansL = l;
                }
                // Shrink: s[l] leaves the window.
                const char out = s[l];
                --windowCount[out];
                // If the outgoing char breaks its quota, validity ends.
                auto jt = need.find(out);
                if (jt != need.end() && windowCount[out] < jt->second) {
                    --formed;
                }
                ++l;
            }
        }
        // ansLen == INT_MAX ⇔ no valid window ever existed.
        return ansLen == INT_MAX ? "" : s.substr(ansL, ansLen);
    }
};

/* =====================================================================
 * APPROACH 2 : Sliding window + 128-slot count arrays (no hashing)
 * ===================================================================== */
class Solution_CountArrays {
public:
    /*
     * Purpose : Return the shortest substring of `s` containing every
     *           character of `t` (with multiplicities), or "" if none.
     * Inputs  : s — the haystack to search inside.
     *           t — the needle whose character counts must be matched.
     * Output  : std::string — the minimum window, or empty string.
     */
    std::string minWindow(const std::string& s, const std::string& t) {
        if (s.empty() || t.empty()) {
            return "";
        }

        // need : required count per ASCII char; slot = (int)char.
        int need[128] = {0};
        for (char c : t) {
            ++need[static_cast<unsigned char>(c)];
        }
        // required = distinct chars in t (slots whose need > 0).
        int required = 0;
        for (int i = 0; i < 128; ++i) {
            if (need[i] > 0) {
                ++required;
            }
        }

        int windowCount[128] = {0};   // counts inside [l, r]
        int matched = 0;              // chars currently meeting their quota
        int ansLen = INT_MAX;
        int ansL = 0;
        int l = 0;

        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
            const unsigned char c = static_cast<unsigned char>(s[r]);
            // Expand: increment this char's window count, then check
            // whether it just crossed its quota (need[c] > 0 guard).
            ++windowCount[c];
            if (need[c] > 0 && windowCount[c] == need[c]) {
                ++matched;
            }

            while (matched == required) {
                const int len = r - l + 1;
                if (len < ansLen) {
                    ansLen = len;
                    ansL = l;
                }
                const unsigned char out = static_cast<unsigned char>(s[l]);
                --windowCount[out];
                // Outgoing char dropped below quota → window invalid.
                if (need[out] > 0 && windowCount[out] < need[out]) {
                    --matched;
                }
                ++l;
            }
        }
        return ansLen == INT_MAX ? "" : s.substr(ansL, ansLen);
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests + a longer string,
 * compare time and peak RAM, print PASS/FAIL per case.
 * ===================================================================== */
int main() {
    const std::vector<std::tuple<std::string, std::string, std::string>> tests = {
        {"ADOBECODEBANC", "ABC", "BANC"},  // classic official example
        {"a", "a", "a"},                  // single char matches
        {"a", "aa", ""}                   // t has more copies than s
    };

    bool allPass = true;
    for (const auto& t : tests) {
        const std::string r1 = Solution_HashMaps().minWindow(std::get<0>(t), std::get<1>(t));
        const std::string r2 = Solution_CountArrays().minWindow(std::get<0>(t), std::get<1>(t));
        const bool ok = r1 == std::get<2>(t) && r2 == std::get<2>(t);
        allPass = allPass && ok;
        std::cout << (ok ? "PASS " : "FAIL ")
                  << "s=\"" << std::get<0>(t) << "\" t=\"" << std::get<1>(t)
                  << "\" expected=\"" << std::get<2>(t) << "\""
                  << "  maps=\"" << r1 << "\"  arrays=\"" << r2 << "\"\n";
    }

    // Longer adversarial-ish string: the minimum window is the suffix
    // "XYZ..." at the end, forcing the full shrink/slide cycle.
    const std::string benchS = "AAAAAAABBBBBBCCCCCDDDDDABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const std::string benchT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    const std::string b1 = Solution_HashMaps().minWindow(benchS, benchT);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    const double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    const long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss; // KB on Linux

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    const std::string b2 = Solution_CountArrays().minWindow(benchS, benchT);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    const double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    const long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (hash maps)     : result=\"" << b1
              << "\"  time=" << us_1 << " µs  peak-ram-delta=" << mem_1 << " KB\n";
    std::cout << "Approach 2 (count arrays)  : result=\"" << b2
              << "\"  time=" << us_2 << " µs  peak-ram-delta=" << mem_2 << " KB\n";

    allPass = allPass && (b1 == b2);
    std::cout << (allPass ? "PASS : all test cases and benchmark agree."
                          : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}
