/*
 * =====================================================================
 * LeetCode 139 : Word Break                                     (Medium)
 * https://leetcode.com/problems/word-break/
 * Category   : 1D Dynamic Programming
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a string `s` and a word dictionary `wordDict`, return true if
 *   `s` can be segmented into a space-separated sequence of dictionary
 *   words (words may be reused).
 * ---------------------------------------------------------------------
 * INTUITION
 *   s is breakable iff some PREFIX s[0:j) is breakable AND the suffix
 *   s[j:i) is a dictionary word. The same suffix is tested by many
 *   prefixes → overlapping subproblems (the classic DP fingerprint).
 *   The dictionary must answer "is this slice a word?" fast → an
 *   unordered_set hash table (O(1) per probe) or a trie.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bottom-up DP + hash set (BEST)
 *   dp[i] = s[0:i) is breakable. dp[0] = true (empty prefix).
 *   Recurrence : dp[i] = OR over j < i of ( dp[j] && wordSet.count(s[j:i]) )
 *   State space : i ∈ [0, n] → n+1 booleans on array dp[n+1], filled
 *                left→right. Cell i reads EVERY earlier cell j → the
 *                full table is required (no rolling-variable shortcut).
 *   Time  Complexity : O(n²·m) — n² (i, j) pairs × O(m) substring hash,
 *                      m = max word length.
 *   Space Complexity : O(n) dp + O(total word chars) hash set.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down memoized DFS (suffix-first)
 *   f(i) = can s[i:] be broken? For each word w: if s[i:] starts with
 *   w AND f(i + w.size()) → true. memo[i] caches solved suffixes.
 *   Trade-off : touches only word-aligned boundaries (fewer probes in
 *               practice than all n² boundaries); recursion depth n.
 *   Time  Complexity : O(n·W·m)   Space Complexity : O(n) memo + set.
 * ---------------------------------------------------------------------
 * DEEP DIVE — hash set vs trie vs string hashing
 *   Option 1 (here): std::unordered_set<std::string> — separate
 *   chaining buckets, O(1) average membership. Each probe hashes the
 *   slice → O(m) per probe, m = word length.
 *   Option 2 (trie): walk the slice through a trie one char at a time;
 *   no hashing of the slice — O(m) worst case too, but shares the
 *   prefix walk across probe positions and avoids re-hashing.
 *   Option 3 (string hashing / rolling hash): precompute a polynomial
 *   rolling hash of s so any slice s[j:i) is O(1) to hash, then probe
 *   the set of word hashes — turns dp into O(n²) total. Prefer it when
 *   words are long; a hash collision check (compare actual strings on
 *   hit) keeps it correct.
 *   State-space math: n+1 boolean states; each state scans ≤ n split
 *   points → O(n²) combine work. Real life : predictive text input,
 *   dictionary-driven sentence segmentation, regex tokenizers.
 * =====================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <sys/resource.h>

/* =====================================================================
 * APPROACH 1 : bottom-up DP with a word-set hash table
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether `s` segments into words of `wordDict`.
     * Inputs  : s — the string to segment.
     *           wordDict — allowed dictionary words.
     * Output  : bool — true when a valid segmentation exists.
     */
    bool wordBreak(const std::string& s, const std::vector<std::string>& wordDict) {
        // Hash table (chaining buckets) → O(1) average membership test.
        std::unordered_set<std::string> wordSet(wordDict.begin(), wordDict.end());
        const int n = static_cast<int>(s.size());
        std::vector<bool> dp(n + 1, false);
        dp[0] = true;  // the empty prefix is trivially breakable

        // Fill left→right: is prefix s[0:i) breakable?
        for (int i = 1; i <= n; ++i) {
            // Try every split point j: breakable prefix + word suffix.
            for (int j = 0; j < i; ++j) {
                if (dp[j] && wordSet.count(s.substr(j, i - j))) {
                    dp[i] = true;  // one valid split suffices
                    break;         // stop probing further split points
                }
            }
        }
        return dp[n];
    }
};

/* =====================================================================
 * APPROACH 2 : top-down memoized DFS over suffixes
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether `s` segments into words of `wordDict`.
     * Inputs  : s — the string to segment.
     *           wordDict — allowed dictionary words.
     * Output  : bool — true when a valid segmentation exists.
     */
    bool wordBreak(const std::string& s, const std::vector<std::string>& wordDict) {
        str = s;
        words = wordDict;
        // memo[i] = -1 unknown, 0 false, 1 true.
        memo.assign(s.size(), -1);
        return f(0);
    }

private:
    std::string str;
    std::vector<std::string> words;
    std::vector<int> memo;

    /*
     * Purpose : Recursive suffix solver with caching (top-down DP).
     * Inputs  : i — start index of the remaining suffix.
     * Output  : bool — whether str[i:] can be segmented.
     */
    bool f(int i) {
        if (i == static_cast<int>(str.size())) {
            return true;          // suffix fully consumed → breakable
        }
        if (memo[i] != -1) {
            return memo[i] == 1;  // overlapping subproblem → reuse
        }
        // Try every dictionary word as the head of the suffix.
        for (const std::string& w : words) {
            if (str.compare(i, w.size(), w) == 0 && f(i + static_cast<int>(w.size()))) {
                memo[i] = 1;      // cache the answer
                return true;
            }
        }
        memo[i] = 0;
        return false;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on every test, compare time + RAM
 * ===================================================================== */
int main() {
    // Test battery: (s, wordDict, expected). Both solutions must match.
    struct Test { std::string s; std::vector<std::string> words; bool expected; };
    const std::vector<Test> tests = {
        {"leetcode",       {"leet", "code"},                 true},
        {"applepenapple",  {"apple", "pen"},                 true},
        {"catsandog",      {"cats", "dog", "sand", "and", "cat"}, false}
    };

    double total_us_1 = 0.0, total_us_2 = 0.0;
    long total_kb_1 = 0, total_kb_2 = 0;
    bool allPass = true;

    for (const Test& t : tests) {
        // --- Approach 1: time via steady_clock, RAM via getrusage ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        const auto start1 = std::chrono::steady_clock::now();
        const bool r1 = Solution_1().wordBreak(t.s, t.words);
        const auto end1 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after1);
        // ru_maxrss delta = peak RAM consumed by THIS run (KB on Linux).
        const double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end1 - start1).count() / 1000.0;
        const long kb1 = after1.ru_maxrss - before1.ru_maxrss;
        total_us_1 += us1;
        total_kb_1 += kb1;

        // --- Approach 2 ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        const auto start2 = std::chrono::steady_clock::now();
        const bool r2 = Solution_2().wordBreak(t.s, t.words);
        const auto end2 = std::chrono::steady_clock::now();
        getrusage(RUSAGE_SELF, &after2);
        const double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end2 - start2).count() / 1000.0;
        const long kb2 = after2.ru_maxrss - before2.ru_maxrss;
        total_us_2 += us2;
        total_kb_2 += kb2;

        const bool ok = (r1 == t.expected) && (r2 == t.expected);
        allPass = allPass && ok;

        std::cout << "s=" << t.s << "  A1=" << (r1 ? "true" : "false")
                  << "  A2=" << (r2 ? "true" : "false")
                  << "  expected=" << (t.expected ? "true" : "false")
                  << (ok ? "  PASS" : "  FAIL")
                  << "  A1 " << us1 << "µs/" << kb1 << "KB  A2 " << us2
                  << "µs/" << kb2 << "KB\n";
    }

    std::cout << "Totals: A1 " << total_us_1 << "µs/" << total_kb_1
              << "KB | A2 " << total_us_2 << "µs/" << total_kb_2 << "KB\n";
    std::cout << (allPass
                  ? "PASS : both approaches match every expected output."
                  : "FAIL : at least one answer is wrong.")
              << "\n";
    return allPass ? 0 : 1;
}