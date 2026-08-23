/*
 * =====================================================================
 * LeetCode 567 : Permutation in String                          (Medium)
 * https://leetcode.com/problems/permutation-in-string/
 * Category   : Sliding Window
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given strings `s1` and `s2`, return true if s2 contains ANY
 *   permutation of s1 as a contiguous substring.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A permutation is a re-ORDERING — so "s2 contains a permutation
 *   of s1" ⇔ "some length-|s1| window of s2 has the same character
 *   MULTISET as s1". Counting kills ordering. A window of exactly
 *   len(s1) slides over s2; each slide drops one char and adds one
 *   char. The naive "compare 26 counters per slide" costs O(26n);
 *   tracking a `matches` counter makes each slide O(1).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Fixed window + 26-array counters + matches (BEST)
 *   Count s1 into c1[26] and the first |s1| chars of s2 into c2[26].
 *   matches = #slots where c1[i] == c2[i]. Sliding: adding s2[i]
 *   and removing s2[i−|s1|] can each only flip ONE slot's equality,
 *   so matches is updated in O(1) per slide. matches == 26 ⇔ true.
 *   Time  Complexity : O(n)  — n = |s2|; O(1) work per slide
 *   Space Complexity : O(1)  — two fixed 26-slot arrays
 * ---------------------------------------------------------------------
 * APPROACH 2 — Fixed window + hash-map counter comparison
 *   Same window, but counters live in an unordered_map<char,int>.
 *   Compare maps with operator== each slide — O(σ) per slide where
 *   σ = distinct chars. Simpler to write, slower in theory.
 *   Time  Complexity : O(n·σ) — σ ≤ min(26, |s1|)
 *   Space Complexity : O(σ)
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — count[26] vs unordered_map
 *   Fixed 26-letter lowercase alphabet (LeetCode constraint) →
 *   int c1[26], c2[26] win: index = c − 'a', O(1) worst case, zero
 *   hashing, one contiguous cache line. unordered_map (C++ separate
 *   chaining) / dict (Python open addressing, linear probing
 *   h(k,i) = (hash(k)+i) mod m) are correct but pay hash + resize
 *   costs for a universe of 26 keys. If the alphabet were Unicode,
 *   maps would be the right call — the 26-array is a lowercase-only
 *   optimization. The REAL lesson is the `matches` counter: turning
 *   a per-slide full comparison into O(1) incremental bookkeeping
 *   is the difference between O(26n) and O(n).
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <string>         // std::string — the two inputs
#include <vector>         // std::vector — test-case storage
#include <unordered_map>  // std::unordered_map — approach 2 counters
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RAM measurement (KB)

/* =====================================================================
 * APPROACH 1 : Fixed window + 26 arrays + incremental matches count
 * ===================================================================== */
class Solution_MatchesCounter {
public:
    /*
     * Purpose : Return true if some contiguous window of `s2` is a
     *           permutation of `s1`.
     * Inputs  : s1 — the needle (its multiset must be matched).
     *           s2 — the haystack to slide the window over.
     * Output  : bool — true iff a permutation of s1 appears in s2.
     */
    bool checkInclusion(const std::string& s1, const std::string& s2) {
        if (s1.size() > s2.size()) {
            return false;  // window longer than the haystack → impossible
        }

        int c1[26] = {0};   // s1's letter multiset (fixed target)
        int c2[26] = {0};   // current window's letter multiset

        // Seed: count s1 fully and the first |s1| chars of s2.
        for (int i = 0; i < static_cast<int>(s1.size()); ++i) {
            ++c1[s1[i] - 'a'];
            ++c2[s2[i] - 'a'];
        }

        // matches : number of slots (0..25) where c1[i] == c2[i].
        // 26 matches ⇔ identical multisets ⇔ window is a permutation.
        int matches = 0;
        for (int i = 0; i < 26; ++i) {
            if (c1[i] == c2[i]) {
                ++matches;
            }
        }

        // Slide: the window is [i − |s1| + 1 .. i].
        for (int i = static_cast<int>(s1.size()); i < static_cast<int>(s2.size()); ++i) {
            if (matches == 26) {
                return true;  // short-circuit BEFORE the next slide
            }
            // Add the incoming char s2[i] to the window.
            const int add = s2[i] - 'a';
            ++c2[add];
            // The incoming char can only flip ITS slot's equality:
            // it now matches exactly when it previously was one short.
            if (c2[add] == c1[add]) {
                ++matches;
            } else if (c2[add] == c1[add] + 1) {
                --matches;  // overshot by one → lost its equality
            }
            // Remove the outgoing char s2[i − |s1|] from the window.
            const int del = s2[i - s1.size()] - 'a';
            --c2[del];
            // Mirror logic for the outgoing char.
            if (c2[del] == c1[del]) {
                ++matches;
            } else if (c2[del] == c1[del] - 1) {
                --matches;
            }
        }
        // Final window is [|s2| − |s1| .. |s2|−1] — check it too.
        return matches == 26;
    }
};

/* =====================================================================
 * APPROACH 2 : Fixed window + hash-map counter comparison (simpler)
 * ===================================================================== */
class Solution_CounterCompare {
public:
    /*
     * Purpose : Return true if some contiguous window of `s2` is a
     *           permutation of `s1`.
     * Inputs  : s1 — the needle (its multiset must be matched).
     *           s2 — the haystack to slide the window over.
     * Output  : bool — true iff a permutation of s1 appears in s2.
     */
    bool checkInclusion(const std::string& s1, const std::string& s2) {
        if (s1.size() > s2.size()) {
            return false;
        }

        // target : s1's full letter multiset.
        std::unordered_map<char, int> target;
        for (char c : s1) {
            ++target[c];
        }
        // windowCount : the current length-|s1| window's multiset.
        std::unordered_map<char, int> windowCount;

        // Seed the first |s1| chars of s2 into the window.
        for (int i = 0; i < static_cast<int>(s1.size()); ++i) {
            ++windowCount[s2[i]];
        }
        // Sliding is a full map comparison per position: readable,
        // correct, but O(σ) per slide instead of O(1).
        for (int i = static_cast<int>(s1.size()); i <= static_cast<int>(s2.size()); ++i) {
            if (windowCount == target) {
                return true;  // multisets equal → a permutation found
            }
            if (i == static_cast<int>(s2.size())) {
                break;  // no next slide to perform
            }
            ++windowCount[s2[i]];                        // add new char
            const char out = s2[i - s1.size()];          // remove old char
            if (--windowCount[out] == 0) {
                windowCount.erase(out);  // keep the map sparse: 0-count
            }                            // entries would still match
        }
        return false;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests + a longer pair,
 * compare time and peak RAM, print PASS/FAIL per case.
 * ===================================================================== */
int main() {
    const std::vector<std::tuple<std::string, std::string, bool>> tests = {
        {"ab", "eidbaooo", true},   // "ba" at index 3 — official
        {"ab", "eidboaoo", false},  // 'a' and 'b' never adjacent — official
        {"adc", "dcda", true}       // "dcd"… actually "dca" — "cda" fits
    };

    bool allPass = true;
    for (const auto& t : tests) {
        const bool r1 = Solution_MatchesCounter().checkInclusion(std::get<0>(t), std::get<1>(t));
        const bool r2 = Solution_CounterCompare().checkInclusion(std::get<0>(t), std::get<1>(t));
        const bool ok = r1 == std::get<2>(t) && r2 == std::get<2>(t);
        allPass = allPass && ok;
        std::cout << (ok ? "PASS " : "FAIL ")
                  << "s1=\"" << std::get<0>(t) << "\" s2=\"" << std::get<1>(t)
                  << "\" expected=" << (std::get<2>(t) ? "true" : "false")
                  << "  matches=" << (r1 ? "true" : "false")
                  << "  compare=" << (r2 ? "true" : "false") << "\n";
    }

    // Longer adversarial pair: the needle appears only at the very end.
    std::string benchS1 = "abcdefghijklmnopqrstuvwxyz";
    std::string benchS2;
    for (int i = 0; i < 40; ++i) {
        benchS2.append("mnopqrstuvwxyzabcdefghijkl");
    }
    benchS2.append("abcdefghijklmnopqrstuvwxyz");

    // --- Approach 1 timing ---
    struct rusage before_1, after_1;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::high_resolution_clock::now();
    const bool b1 = Solution_MatchesCounter().checkInclusion(benchS1, benchS2);
    auto end_1 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    const double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    const long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss; // KB on Linux

    // --- Approach 2 timing ---
    struct rusage before_2, after_2;
    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::high_resolution_clock::now();
    const bool b2 = Solution_CounterCompare().checkInclusion(benchS1, benchS2);
    auto end_2 = std::chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    const double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;
    const long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;

    std::cout << "Approach 1 (matches counter) : result=" << (b1 ? "true" : "false")
              << "  time=" << us_1 << " µs  peak-ram-delta=" << mem_1 << " KB\n";
    std::cout << "Approach 2 (counter compare) : result=" << (b2 ? "true" : "false")
              << "  time=" << us_2 << " µs  peak-ram-delta=" << mem_2 << " KB\n";

    allPass = allPass && (b1 == b2);
    std::cout << (allPass ? "PASS : all test cases and benchmark agree."
                          : "FAIL : at least one answer is wrong.") << "\n";
    return 0;
}