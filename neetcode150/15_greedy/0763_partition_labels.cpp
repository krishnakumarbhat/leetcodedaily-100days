/*
 * =====================================================================
 * LeetCode 763 : Partition Labels                                 (Medium)
 * https://leetcode.com/problems/partition-labels/
 * Category   : Greedy
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Split a lowercase string s into as MANY non-empty parts as
 *   possible such that every character appears in at most ONE part.
 *   Return the list of part lengths.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A part is forced to be a SUFFIX of every character inside it.
 *   Precompute last[i] = final occurrence of s[i]. While sweeping,
 *   keep `segEnd` = max(last[·]) over the current part. The earliest
 *   index where i == segEnd is the EARLIEST safe cut: cutting later
 *   only merges parts (never more parts); cutting earlier leaks a
 *   character into two parts (invalid). Earliest safe cut ⇒ maximal
 *   part count ⇒ greedy is exact (exchange argument: any valid
 *   partition's first cut is ≥ our first cut, and removing the common
 *   prefix preserves the argument for the remainder — induction).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Last-index map + sweep (BEST)
 *     last[c] = i for every char; sweep i, segEnd = max(segEnd,
 *     last[s[i]]); if i == segEnd → emit length, reset segment.
 *   Time  Complexity : O(n)   Space Complexity : O(1)
 *   (26 lowercase letters → constant-size last[] table.)
 * ---------------------------------------------------------------------
 * APPROACH 2 — Merge character intervals (same idea, other lens)
 *   Every character c spans interval [first[c], last[c]]. A part is a
 *   MERGE of all intervals it contains: sort the ≤26 intervals by
 *   start, merge overlapping ones (like "Merge Intervals"), emit
 *   merged lengths.
 *   Time  Complexity : O(n + k log k), k ≤ 26 → O(n) effective.
 *   Space Complexity : O(k) → O(1).
 * ---------------------------------------------------------------------
 * DEEP DIVE — why "earliest safe cut" is provably maximal
 *   Greedy exchange: let G cut at index e = segEnd (earliest safe),
 *   let O be any optimal partition with first cut at o. Claim o ≥ e:
 *   if o < e then some character in [0, o] has a later occurrence
 *   after o (since e is the earliest point where ALL characters in
 *   [0, e] have appeared) → O's first part leaks → O invalid. Hence
 *   every valid first cut is ≥ e, so cutting at e never loses parts.
 *   By induction on the remainder, greedy emits the maximal count.
 * =====================================================================
 */

#include <iostream>       // std::cout — benchmark output
#include <vector>         // std::vector — result lengths
#include <string>         // std::string — the input
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak RSS measurement

/* =====================================================================
 * APPROACH 1 : Last-index table + sweep (earliest safe cuts)
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return maximal partition lengths, one per part.
     * Inputs  : s — lowercase string to partition.
     * Output  : vector<int> — length of each consecutive part.
     */
    std::vector<int> partitionLabels(const std::string& s) {
        // last[c] = final occurrence index of character c.
        // 26 fixed slots → O(1) memory, O(1) lookups.
        std::vector<int> last(26, -1);
        for (int i = 0; i < static_cast<int>(s.size()); ++i) {
            last[s[i] - 'a'] = i;
        }

        std::vector<int> parts;
        int segStart = 0; // left edge of the current part
        int segEnd = 0;   // furthest required extent of current part

        for (int i = 0; i < static_cast<int>(s.size()); ++i) {
            // The current part must extend to this char's final spot.
            int e = last[s[i] - 'a'];
            if (e > segEnd) segEnd = e;

            if (i == segEnd) {
                // Every char in [segStart, i] has appeared → earliest
                // safe cut. Later cuts only merge parts.
                parts.push_back(i - segStart + 1);
                segStart = i + 1; // next part begins right after
            }
        }
        return parts;
    }
};

/* =====================================================================
 * APPROACH 2 : Merge per-character intervals (≤26 intervals)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return maximal partition lengths, one per part.
     * Inputs  : s — lowercase string to partition.
     * Output  : vector<int> — length of each consecutive part.
     */
    std::vector<int> partitionLabels(const std::string& s) {
        // Span of each character: first and last occurrence.
        std::vector<int> first(26, -1), last(26, -1);
        for (int i = 0; i < static_cast<int>(s.size()); ++i) {
            int c = s[i] - 'a';
            if (first[c] == -1) first[c] = i; // first sighting
            last[c] = i;                      // keep overwriting → final
        }

        // Collect intervals for characters that actually appear.
        std::vector<std::pair<int, int> > intervals;
        for (int c = 0; c < 26; ++c) {
            if (first[c] != -1) intervals.emplace_back(first[c], last[c]);
        }

        // Insertion sort by start — ≤26 items, no <algorithm> needed.
        for (int i = 1; i < static_cast<int>(intervals.size()); ++i) {
            std::pair<int, int> key = intervals[i];
            int j = i - 1;
            while (j >= 0 && intervals[j].first > key.first) {
                intervals[j + 1] = intervals[j];
                --j;
            }
            intervals[j + 1] = key;
        }

        // Merge overlapping intervals → each merged block is one part.
        std::vector<int> parts;
        int curStart = intervals[0].first;
        int curEnd = intervals[0].second;
        for (int i = 1; i < static_cast<int>(intervals.size()); ++i) {
            if (intervals[i].first <= curEnd) {
                if (intervals[i].second > curEnd) curEnd = intervals[i].second;
            } else {
                parts.push_back(curEnd - curStart + 1); // close a part
                curStart = intervals[i].first;
                curEnd = intervals[i].second;
            }
        }
        parts.push_back(curEnd - curStart + 1); // close the last part
        return parts;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, time + peak RAM
 * ===================================================================== */
int main() {
    // Official example + all-distinct + single char + repeated char.
    const std::vector<std::string> tests = {
        "ababcbacadefegdehijhklij",   // → {9,7,8}
        "eccbbbbdec",                 // → {10}
        "caedbdedda",                 // → {1,9}
        "a",                          // → {1}
        "abc",                        // → {1,1,1}
        "aaaa"                        // → {4}
    };
    const std::vector<std::vector<int> > expected = {
        { 9, 7, 8 }, { 10 }, { 1, 9 }, { 1 }, { 1, 1, 1 }, { 4 }
    };

    auto run_all = [&](int which, std::vector<int> (*solve)(const std::string&)) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto t0 = std::chrono::high_resolution_clock::now();

        bool ok = true;
        for (int t = 0; t < static_cast<int>(tests.size()); ++t) {
            if (solve(tests[t]) != expected[t]) ok = false;
        }

        auto t1 = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);
        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1000.0;
        long mem_kb = after.ru_maxrss - before.ru_maxrss; // delta, KB

        std::cout << "Approach " << which
                  << " : " << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " µs  peak-ram-delta = " << mem_kb << " KB\n";
        return ok;
    };

    bool a1 = run_all(1, [](const std::string& s) { return Solution_1().partitionLabels(s); });
    bool a2 = run_all(2, [](const std::string& s) { return Solution_2().partitionLabels(s); });
    std::cout << (a1 && a2 ? "PASS : both approaches produce the maximal partition."
                           : "FAIL : at least one approach is wrong.") << "\n";
    return 0;
}
