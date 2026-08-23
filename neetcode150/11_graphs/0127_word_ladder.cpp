/*
 * =====================================================================
 * LeetCode 127 : Word Ladder                                         (Hard)
 * https://leetcode.com/problems/word-ladder/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A transformation sequence from `beginWord` to `endWord` is a list
 *   of words where every adjacent pair differs by exactly ONE letter,
 *   and every word after the first must exist in `wordList`. Return
 *   the SHORTEST such sequence length (counting beginWord), or 0 if
 *   no such sequence exists.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Words are NODES of a graph; an edge connects two words that differ
 *   in one letter. Finding the shortest transformation = BFS from
 *   beginWord until we reach endWord. The graph is implicit — instead
 *   of building adjacency lists up-front, each node's neighbours are
 *   GENERATED on the fly by mutating every letter to a..z (26 × L
 *   candidate words, each an O(1) set lookup). BFS guarantees the
 *   first time endWord is dequeued is along the shortest path.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Plain BFS (BEST for correctness)
 *   Queue holds (word, depth). Erase each word from the dict when it
 *   is first enqueued so no word is ever visited twice.
 *   Time  Complexity : O(n · L²)  — n words, L letters each, L² to
 *                        build/compare each candidate string.
 *   Space Complexity : O(n · L)   — dict + queue hold all words.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Bidirectional BFS (BEST for speed)
 *   Grow TWO frontiers (begin side + end side). Expand the SMALLER
 *   frontier each round; when a generated word lands in the opposite
 *   frontier the two waves meet → depth found. Halves the search
 *   breadth on average: b^(d) vs 2·b^(d/2).
 *   Time  Complexity : O(n · L²)  — same worst case, far fewer nodes
 *                        visited in practice.
 *   Space Complexity : O(n · L)   — two frontiers + dict.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — BFS vs DFS on implicit graphs
 *   BFS explores in layers from the source: the FIRST hit of the
 *   target is provably the SHORTEST path (unweighted edges). DFS
 *   would find SOME path — not necessarily the shortest — so it is
 *   wrong for this problem. std::unordered_set is the C++ equivalent
 *   of Python's set: separate chaining, O(1) average insert/lookup.
 *   Python's dict/set use open addressing with linear probing:
 *         h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
 *   The probing cost is why the dict stays a hash table even when the
 *   graph is "implicit" — every candidate word is just a probe.
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — input word list
#include <string>           // std::string — words
#include <queue>            // std::queue — BFS frontier
#include <unordered_map>    // std::unordered_map — hash table (chaining)
#include <unordered_set>    // std::unordered_set — visited/dict hash set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement
#include <utility>          // std::pair — (word, depth) queue entries
#include <algorithm>        // std::swap — smaller-frontier trick (A2)

/* =====================================================================
 * APPROACH 1 : BFS on the implicit word graph
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the shortest transformation sequence length.
     * Inputs  : beginWord — starting word.
     *           endWord   — target word.
     *           wordList  — dictionary of allowed intermediate words.
     * Output  : int ladder length (beginWord included), 0 if impossible.
     */
    int ladderLength(const std::string& beginWord, const std::string& endWord,
                     const std::vector<std::string>& wordList) {
        // dict : the unvisited words. Copy into a set for O(1) probes.
        std::unordered_set<std::string> dict(wordList.begin(), wordList.end());
        // endWord must be reachable — if it is not even in the dict
        // the graph has no path to it at all → 0 immediately.
        if (dict.find(endWord) == dict.end()) return 0;
        // beginWord may itself be in the dict — erase it so the BFS
        // never "visits" the start node twice through a cycle.
        dict.erase(beginWord);

        // queue : frontier of (word, depth). BFS visits in layer order.
        std::queue<std::pair<std::string, int>> q;
        q.push({beginWord, 1}); // beginWord counts as depth 1

        while (!q.empty()) {
            auto [word, depth] = q.front();
            q.pop();

            // Reached the target → BFS first-hit guarantee: shortest.
            if (word == endWord) return depth;

            // Generate ALL neighbours of `word` by mutating each of
            // the L positions to every possible letter (26 options).
            std::string next = word;
            for (size_t i = 0; i < next.size(); ++i) {
                char original = next[i];   // restore after the inner loop
                for (char c = 'a'; c <= 'z'; ++c) {
                    next[i] = c;
                    // One-letter-different word inside the dict = a
                    // real graph edge. Erase on first sight so each
                    // node is enqueued exactly once (prevents cycles).
                    auto it = dict.find(next);
                    if (it != dict.end()) {
                        dict.erase(it);
                        q.push({next, depth + 1});
                    }
                }
                next[i] = original;        // undo this position's mutation
            }
        }
        // Queue emptied without ever dequeuing endWord → unreachable.
        return 0;
    }
};

/* =====================================================================
 * APPROACH 2 : Bidirectional BFS — meet in the middle
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the shortest transformation sequence length.
     * Inputs  : beginWord — starting word.
     *           endWord   — target word.
     *           wordList  — dictionary of allowed intermediate words.
     * Output  : int ladder length (beginWord included), 0 if impossible.
     */
    int ladderLength(const std::string& beginWord, const std::string& endWord,
                     const std::vector<std::string>& wordList) {
        std::unordered_set<std::string> dict(wordList.begin(), wordList.end());
        if (dict.find(endWord) == dict.end()) return 0;
        dict.erase(beginWord);

        // Two frontiers: `front` grows from beginWord, `back` from
        // endWord. Both sides remember only their CURRENT layer.
        std::unordered_set<std::string> front{beginWord};
        std::unordered_set<std::string> back{endWord};
        int depth = 1; // each round = one layer on each side

        while (!front.empty() && !back.empty()) {
            // ALWAYS expand the smaller side: keeps the frontier as
            // narrow as possible → dramatically fewer generated words.
            if (front.size() > back.size()) std::swap(front, back);

            std::unordered_set<std::string> nextLayer;
            for (const std::string& word : front) {
                std::string s = word;
                for (size_t i = 0; i < s.size(); ++i) {
                    char original = s[i];
                    for (char c = 'a'; c <= 'z'; ++c) {
                        s[i] = c;
                        // Generated word hits the OTHER wave → the two
                        // fronts just touched: path length = depth + 1.
                        if (back.find(s) != back.end()) return depth + 1;
                        // Else if it is an unvisited dict word, claim
                        // it for this side (erase = visited).
                        auto it = dict.find(s);
                        if (it != dict.end()) {
                            dict.erase(it);
                            nextLayer.insert(s);
                        }
                    }
                    s[i] = original;
                }
            }
            front = std::move(nextLayer); // advance the wave one layer
            ++depth;
        }
        return 0; // one wave exhausted → no path exists
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 official-style tests
 * ===================================================================== */
int main() {
    // Test 1 (official): hit→cog via hot→dot→dog→lot→log → length 5.
    std::string b1 = "hit", e1 = "cog";
    std::vector<std::string> w1 = {"hot", "dot", "dog", "lot", "log", "cog"};
    // Test 2 (official): endWord absent from dict → 0.
    std::string b2 = "hit", e2 = "cog";
    std::vector<std::string> w2 = {"hot", "dot", "dog", "lot", "log"};
    // Test 3: one-letter start → direct edge → length 2.
    std::string b3 = "a", e3 = "c";
    std::vector<std::string> w3 = {"a", "b", "c"};

    struct { std::string b, e; std::vector<std::string> w; int expected; } tests[] = {
        {b1, e1, w1, 5}, {b2, e2, w2, 0}, {b3, e3, w3, 2}
    };

    bool allPass = true;
    for (int t = 0; t < 3; ++t) {
        // --- Approach 1 timing + memory ---
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto s1 = std::chrono::high_resolution_clock::now();
        int r1 = Solution_1().ladderLength(tests[t].b, tests[t].e, tests[t].w);
        auto e1_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);

        // --- Approach 2 timing + memory ---
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto s2 = std::chrono::high_resolution_clock::now();
        int r2 = Solution_2().ladderLength(tests[t].b, tests[t].e, tests[t].w);
        auto e2_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);

        // ru_maxrss is the cumulative peak → the delta is what THIS
        // call consumed; report in KB as requested.
        long mem1 = (after1.ru_maxrss - before1.ru_maxrss);
        long mem2 = (after2.ru_maxrss - before2.ru_maxrss);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1_ - s1).count() / 1000.0;
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2_ - s2).count() / 1000.0;

        bool ok = (r1 == tests[t].expected) && (r2 == tests[t].expected) && (r1 == r2);
        allPass = allPass && ok;
        std::cout << "Test " << (t + 1) << " (" << tests[t].b << "->" << tests[t].e << ") "
                  << (ok ? "PASS" : "FAIL")
                  << " | A1=" << r1 << " (expect " << tests[t].expected << ")"
                  << "  time=" << us1 << " µs  mem=" << mem1 << " KB"
                  << " | A2=" << r2 << "  time=" << us2 << " µs  mem=" << mem2 << " KB\n";
    }
    std::cout << (allPass ? "PASS : all tests green on both approaches.\n"
                          : "FAIL : at least one test/approach disagrees.\n");
    return 0;
}