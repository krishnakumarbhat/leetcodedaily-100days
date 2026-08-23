/*
 * =====================================================================
 * LeetCode 49 : Group Anagrams                                   (Medium)
 * https://leetcode.com/problems/group-anagrams/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an array of strings, group the anagrams together. Any order
 *   of groups is accepted.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Two words are anagrams iff their "fingerprint" is identical.
 *   A fingerprint must be ORDER-INSENSITIVE: either the sorted word
 *   ("eat"→"aet") or the 26-letter count tuple. Hash the fingerprint
 *   → all anagrams land in the same bucket. Classic hash-key trick.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Count-tuple key (BEST for long words)
 *   Fingerprint = tuple of 26 letter counts (Python) / string of 26
 *   counts (C++). Computing it costs O(k) per word, k = word length.
 *   Time  Complexity : O(n·k)   — n words × k letters each.
 *   Space Complexity : O(n·k)   — the output groups + key storage.
 *   WHY tuple: Python tuples are HASHABLE (immutable) → valid dict
 *   keys; lists are not. C++ has no tuple hash → serialize counts
 *   into a fixed-length string "1,0,2,..." to get a comparable key.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Sorted-string key
 *   Fingerprint = sorted(word). Sorting costs O(k log k) per word.
 *   Time  Complexity : O(n·k log k)   Space Complexity : O(n·k).
 *   Simpler to write; slower for long words. Both are accepted.
 * =====================================================================
 */

#include <vector>          // std::vector — the input and output containers
#include <string>          // std::string — words
#include <unordered_map>   // std::unordered_map — fingerprint → group
#include <algorithm>       // std::sort — approach 2 fingerprint
#include <chrono>          // timing for the benchmark
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : 26-count fingerprint key
 * ===================================================================== */
class Solution_CountKey {
public:
    /*
     * Purpose : Group all anagrams of the input words together.
     * Inputs  : strs — list of words to group.
     * Output  : vector of groups; each group is a list of anagrams.
     */
    vector<vector<string>> groupAnagrams(const vector<string>& strs) {

        // key (26 counts serialized) → list of words sharing that key.
        unordered_map<string, vector<string>> groups;

        // Fingerprint every word exactly once.
        for (const string& w : strs) {

            // count[0..25] = how many 'a'..'z' this word contains.
            int count[26] = {0};
            for (char c : w) {
                ++count[c - 'a'];   // 'a'→0 … 'z'→25, no hash function needed
            }

            // Serialize counts with commas so "1,0" ≠ "10" (unambiguous).
            string key;
            for (int i = 0; i < 26; ++i) {
                key += to_string(count[i]) + ",";
            }

            // All words with the same 26-counts land in the same bucket.
            groups[key].push_back(w);
        }

        // Flatten the hash table into the required "list of groups".
        vector<vector<string>> result;
        for (auto& kv : groups) {
            result.push_back(kv.second);
        }
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : sorted-word fingerprint key
 * ===================================================================== */
class Solution_SortedKey {
public:
    /*
     * Purpose : Group all anagrams of the input words together.
     * Inputs  : strs — list of words to group.
     * Output  : vector of groups; each group is a list of anagrams.
     */
    vector<vector<string>> groupAnagrams(const vector<string>& strs) {

        // sorted word → group (canonical form as the dict key).
        unordered_map<string, vector<string>> groups;

        // Fingerprint every word once.
        for (const string& w : strs) {

            // Sorting erases order: "eat","tea","ate" all become "aet".
            string key = w;
            sort(key.begin(), key.end());

            // Same sorted form ⟹ same letter multiset ⟹ same group.
            groups[key].push_back(w);
        }

        // Flatten groups into the required output shape.
        vector<vector<string>> result;
        for (auto& kv : groups) {
            result.push_back(kv.second);
        }
        return result;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // The official example plus one long-word stress case.
    vector<string> strs = {"eat", "tea", "tan", "ate", "nat", "bat",
                           "listen", "silent", "enlist", "inlets"};

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    auto r1 = Solution_CountKey().groupAnagrams(strs);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 ---
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    auto r2 = Solution_SortedKey().groupAnagrams(strs);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (count-tuple key) : " << r1.size() << " groups"
         << "  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (sorted key)      : " << r2.size() << " groups"
         << "  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    // Both must produce the same number of groups for this input.
    cout << ((r1.size() == r2.size()) ? "PASS : both approaches agree."
                                      : "FAIL : approaches disagree.")
         << "\n";
    return 0;
}