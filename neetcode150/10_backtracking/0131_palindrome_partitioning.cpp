/*
 * =====================================================================
 * LeetCode 131 : Palindrome Partitioning                            (Medium)
 * https://leetcode.com/problems/palindrome-partitioning/
 * Category   : Backtracking
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Split a string into substrings that are ALL palindromes; return
 *   every possible such partition.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Choose where to cut: try every possible first palindrome prefix
 *   (s[i..j] palindrome), recurse on the rest. This is backtracking
 *   over cut positions; the palindrome test prunes bad cuts early.
 * ---------------------------------------------------------------------
 * APPROACH 1 · DFS with on-the-fly palindrome check (best)
 *   dfs(start): start == n → record. Else for end in start..n-1:
 *   if s[start..end] is a palindrome, take it, recurse(end+1).
 * APPROACH 2 · DP palindrome table + DFS
 *   Precompute isPal[i][j] in O(n²), then the DFS queries O(1) per cut.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Why the O(1) palindrome table matters at n = 16
 *   Naive checking costs O(n) per cut probe → worst O(n·2^n). The
 *   DP table isPal[i][j] = (s[i]==s[j]) && (j-i < 2 || isPal[i+1][j-1])
 *   turns each probe into O(1), making the whole search O(n² + #partitions).
 *   Both variants share the same DFS skeleton — this file shows the
 *   direct check as A1 and the table as A2, with identical outputs.
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(n · 2^n) naive; O(2^n) with a DP table.
 * MEMORY COMPLEXITY: O(n) depth (+ O(n²) table in A2).
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::vector<std::vector<std::string>> out_;
    std::vector<std::string> cur_;
    std::string* s_;
    bool isPal(int l, int r) {                 // direct O(n) check
        while (l < r) if ((*s_)[l++] != (*s_)[r--]) return false;
        return true;
    }
    void dfs(int start) {
        if (start == static_cast<int>(s_->size())) { out_.push_back(cur_); return; }
        for (int end = start; end < static_cast<int>(s_->size()); ++end) {
            if (!isPal(start, end)) continue;
            cur_.push_back(s_->substr(start, end - start + 1));
            dfs(end + 1);
            cur_.pop_back();                   // backtrack the cut
        }
    }
public:
    std::vector<std::vector<std::string>> partition(std::string s) {
        s_ = &s;
        dfs(0);
        return out_;
    }
};

class Solution_2 {
    std::vector<std::vector<std::string>> out_;
    std::vector<std::string> cur_;
    std::string s_;
    std::vector<std::vector<bool>> pal_;
    void dfs(int start) {
        if (start == static_cast<int>(s_.size())) { out_.push_back(cur_); return; }
        for (int end = start; end < static_cast<int>(s_.size()); ++end) {
            if (!pal_[start][end]) continue;   // O(1) table query
            cur_.push_back(s_.substr(start, end - start + 1));
            dfs(end + 1);
            cur_.pop_back();
        }
    }
public:
    std::vector<std::vector<std::string>> partition(std::string s) {
        s_ = s;
        int n = static_cast<int>(s.size());
        pal_.assign(n, std::vector<bool>(n, false));
        for (int i = n - 1; i >= 0; --i)
            for (int j = i; j < n; ++j)
                pal_[i][j] = s[i] == s[j] && (j - i < 2 || pal_[i + 1][j - 1]);
        dfs(0);
        return out_;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::string s; int want; };
    const Case cases[] = {{"aab", 2}, {"a", 1}, {"aaa", 4}};
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = static_cast<int>(Solution_1().partition(c.s).size());
        int r2 = static_cast<int>(Solution_2().partition(c.s).size());
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "\"" << c.s << "\" → A1=" << r1 << " A2=" << r2
                  << " (want " << c.want << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
