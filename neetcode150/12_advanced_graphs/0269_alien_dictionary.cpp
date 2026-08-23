/*
 * =====================================================================
 * LeetCode 269 : Alien Dictionary                                  (Hard)
 * https://leetcode.com/problems/alien-dictionary/
 * Category   : Advanced graphs / topological sort
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given words sorted in an unknown alien alphabet, derive the
 *   alphabetical order of the letters. Return "" if inconsistent.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Each adjacent word pair gives at most ONE order constraint: the
 *   first differing letter a→b means "a comes before b". Build a DAG
 *   of constraints and topologically sort it (Kahn's algorithm).
 * ---------------------------------------------------------------------
 * APPROACH 1 · Kahn's algorithm (best)
 *   1. Collect all letters; for each adjacent pair find the first
 *      differing char and add edge a→b (indegree[b]++).
 *   2. Queue all zero-indegree nodes; pop → append to order, decrement
 *      children. Cycle (queue empties early) → "".
 * APPROACH 2 · DFS with 3-color cycle detection
 *   1. Same edges; DFS each node with states 0/1/2.
 *   2. Gray node revisited → cycle → ""; append post-order, reverse.
 * ---------------------------------------------------------------------
 * DEEP DIVE · What can go wrong, and why
 *   (1) "abc" vs "ab" → shorter prefix first is a CONSTRAINT VIOLATION
 *   (return ""), but only when the common prefix differs in length.
 *   (2) The "first differing letter" rule drops ALL later letters —
 *   they give no information.
 *   (3) A cycle (e.g. a<b, b<a) is impossible in a real alphabet;
 *   the graph must be a DAG or the order is undefined.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(C) — C total characters across all words.
 * MEMORY COMPLEXITY: O(1) — at most 26 letters.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <algorithm>
#include <array>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
public:
    std::string alienOrder(std::vector<std::string>& words) {
        std::array<std::array<bool, 26>, 26> adj{};   // adj[u][v] = edge u→v
        std::array<int, 26> indeg{};                  // indegree per letter
        std::array<bool, 26> present{};               // letters that exist
        for (const auto& w : words)
            for (char c : w) present[c - 'a'] = true;
        for (size_t i = 0; i + 1 < words.size(); ++i) {
            const auto& a = words[i];
            const auto& b = words[i + 1];
            size_t j = 0;
            while (j < a.size() && j < b.size() && a[j] == b[j]) ++j;
            if (j == b.size() && j < a.size()) return "";  // "abc" > "ab"
            if (j < a.size() && j < b.size() && !adj[a[j] - 'a'][b[j] - 'a']) {
                adj[a[j] - 'a'][b[j] - 'a'] = true;
                ++indeg[b[j] - 'a'];
            }
        }
        std::queue<int> q;
        for (int i = 0; i < 26; ++i)
            if (present[i] && indeg[i] == 0) q.push(i);
        std::string order;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(static_cast<char>('a' + u));
            for (int v = 0; v < 26; ++v)
                if (adj[u][v] && --indeg[v] == 0) q.push(v);
        }
        for (int i = 0; i < 26; ++i)
            if (present[i] && indeg[i] > 0) return "";   // leftover = cycle
        return order;
    }
};

class Solution_2 {
    std::array<std::array<bool, 26>, 26> adj_{};
    std::array<bool, 26> present_{};
    std::array<int, 26> state_{};                         // 0=white 1=gray 2=black
    std::string order_;
    bool dfs(int u) {
        state_[u] = 1;                                    // gray: on the stack
        for (int v = 0; v < 26; ++v)
            if (adj_[u][v]) {
                if (state_[v] == 1) return false;         // back edge = cycle
                if (state_[v] == 0 && !dfs(v)) return false;
            }
        state_[u] = 2;                                    // black: finished
        order_.push_back(static_cast<char>('a' + u));     // post-order
        return true;
    }
public:
    std::string alienOrder(std::vector<std::string>& words) {
        for (const auto& w : words)
            for (char c : w) present_[c - 'a'] = true;
        for (size_t i = 0; i + 1 < words.size(); ++i) {
            const auto& a = words[i];
            const auto& b = words[i + 1];
            size_t j = 0;
            while (j < a.size() && j < b.size() && a[j] == b[j]) ++j;
            if (j == b.size() && j < a.size()) return "";
            if (j < a.size() && j < b.size()) adj_[a[j] - 'a'][b[j] - 'a'] = true;
        }
        for (int i = 0; i < 26; ++i)
            if (present_[i] && state_[i] == 0 && !dfs(i)) return "";
        std::reverse(order_.begin(), order_.end());       // reverse post-order
        return order_;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::vector<std::string> w; std::string want; };
    const Case cases[] = {
        {{"wrt", "wrf", "er", "ett", "rftt"}, "wertf"},
        {{"z", "x"}, "zx"},
        {{"z", "x", "z"}, ""},
        {{"ab", "abc"}, "abc"}
    };
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        std::vector<std::string> v1 = c.w, v2 = c.w;
        std::string r1 = Solution_1().alienOrder(v1);
        std::string r2 = Solution_2().alienOrder(v2);
        bool ok = (r1 == c.want || (c.want.empty() ? r1.empty() : r1.size() == c.want.size() && std::is_permutation(r1.begin(), r1.end(), c.want.begin()))) &&
                  (r2 == c.want || (c.want.empty() ? r2.empty() : r2.size() == c.want.size() && std::is_permutation(r2.begin(), r2.end(), c.want.begin())));
        allOk = allOk && ok;
        std::cout << "[" << c.w[0] << " ...] → A1=" << r1 << " A2=" << r2
                  << " (want " << c.want << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
