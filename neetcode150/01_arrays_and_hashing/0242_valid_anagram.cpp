/*
 * =====================================================================
 * LeetCode 242 : Valid Anagram                                   (Easy)
 * https://leetcode.com/problems/valid-anagram/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two strings s and t, return true if t is an anagram of s
 *   (same letters, same counts, any order), false otherwise.
 * ---------------------------------------------------------------------
 * INTUITION
 *   An anagram is a multiset equality: letter→count must match for
 *   both strings. So count letters of s, subtract counts of t, and
 *   check that nothing goes negative / stays positive at the end.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Fixed-size frequency array (BEST)
 *   Only 26 lowercase letters exist → use int count[26] instead of a
 *   hash map. Index = letter - 'a'. Count up for s, down for t.
 *   Time  Complexity : O(n)   — single pass over both strings.
 *   Space Complexity : O(1)   — 26 ints regardless of n.
 *   WHY better than a hash map: fixed tiny key space → no hashing
 *   cost, no collisions, contiguous 26×4 bytes = perfect cache
 *   locality. A hash map would need O(1) memory too but with
 *   hashing + probing overhead.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sort both strings
 *   Sort s and t, then compare. Equal iff anagrams.
 *   Time  Complexity : O(n log n) — dominated by the sorts.
 *   Space Complexity : O(1)       — sorting in place.
 * =====================================================================
 */

#include <string>        // std::string — the input type
#include <algorithm>     // std::sort — used by approach 2
#include <chrono>        // timing for the benchmark
#include <iostream>      // std::cout — benchmark output
#include <sys/resource.h>// getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Frequency array of 26 counters
 * ===================================================================== */
class Solution_FreqArray {
public:
    /*
     * Purpose : Decide whether t is an anagram of s.
     * Inputs  : s, t — the two strings to compare.
     * Output  : true when both hold identical letter multiset.
     */
    bool isAnagram(const string& s, const string& t) {

        // Different lengths can never be anagrams — cheap early exit.
        if (s.size() != t.size()) {
            return false;
        }

        // count[0..25] : occurrences of 'a'..'z'. 26 ints → O(1) space.
        int count[26] = {0};

        // One pass: credit s's letters, debit t's letters.
        for (int i = 0; i < static_cast<int>(s.size()); ++i) {

            // letter 'a' maps to index 0, 'z' to 25 — no hash needed.
            ++count[s[i] - 'a'];
            --count[t[i] - 'a'];
        }

        // If every bucket is back to zero → the multiset matched.
        for (int i = 0; i < 26; ++i) {
            if (count[i] != 0) {
                return false;
            }
        }
        return true;
    }
};

/* =====================================================================
 * APPROACH 2 : Sort both strings and compare
 * ===================================================================== */
class Solution_SortCompare {
public:
    /*
     * Purpose : Decide whether t is an anagram of s.
     * Inputs  : s, t — the two strings to compare.
     * Output  : true when both hold identical letter multiset.
     */
    bool isAnagram(string s, string t) {

        // Sorting rearranges an anagram into the SAME canonical order.
        sort(s.begin(), s.end());
        sort(t.begin(), t.end());

        // Canonical forms equal ⟺ original strings were anagrams.
        return s == t;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // Classic anagram pair.
    string s = "anagram", t = "nagaram";

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    bool r1 = Solution_FreqArray().isAnagram(s, t);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 ---
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    bool r2 = Solution_SortCompare().isAnagram(s, t);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (freq array [26]) : " << (r1 ? "true" : "false")
         << "  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (sort + compare)  : " << (r2 ? "true" : "false")
         << "  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    cout << ((r1 == r2) ? "PASS : both approaches agree."
                        : "FAIL : approaches disagree.")
         << "\n";
    return 0;
}