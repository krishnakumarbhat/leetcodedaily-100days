/*
 * =====================================================================
 * LeetCode 17  : Letter Combinations of a Phone Number               (Medium)
 * https://leetcode.com/problems/letter-combinations-of-a-phone-number/
 * Category   : Backtracking
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Map digits 2-9 to letters (phone keypad); return every letter
 *   combination the digits could stand for.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Each digit is an independent dimension of choices — the output is
 *   a Cartesian product. Backtracking enumerates it without storing
 *   partial prefixes beyond the current path.
 * ---------------------------------------------------------------------
 * APPROACH 1 · Backtracking (best)
 *   dfs(d): d == len(digits) → record current prefix. Else for each
 *   letter of digits[d]: append, recurse(d+1), pop.
 * APPROACH 2 · Iterative product (BFS-ish)
 *   Start with [""]; for every digit, extend every existing prefix
 *   with each letter — pure list comprehension.
 * ---------------------------------------------------------------------
 * DEEP DIVE · Product enumeration and the count formula
 *   The answer has Π(letters(digit)) strings — e.g. "23" → 3×3 = 9.
 *   Both approaches visit exactly that many leaves; the iterative one
 *   allocates all prefixes per level (memory O(Σ outputs × length)),
 *   while DFS keeps one shared mutable prefix (O(len)). Empty input
 *   must return [] — a classic off-by-one for both idioms (the
 *   iterative version must special-case the [""] seed).
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(4^n) worst (all 9's) — 4 letters per digit.
 * MEMORY COMPLEXITY: O(n) DFS depth.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    const std::array<std::string, 8> map_ = {"abc", "def", "ghi", "jkl",
                                             "mno", "pqrs", "tuv", "wxyz"};
    std::vector<std::string> out_;
    std::string cur_;
    std::string* d_;
    void dfs(int pos) {
        if (pos == static_cast<int>(d_->size())) { out_.push_back(cur_); return; }
        for (char ch : map_[(*d_)[pos] - '2']) {
            cur_.push_back(ch);
            dfs(pos + 1);
            cur_.pop_back();                   // backtrack the letter
        }
    }
public:
    std::vector<std::string> letterCombinations(std::string digits) {
        if (digits.empty()) return {};
        d_ = &digits;
        dfs(0);
        return out_;
    }
};

class Solution_2 {
public:
    std::vector<std::string> letterCombinations(std::string digits) {
        if (digits.empty()) return {};
        const std::array<std::string, 8> map = {"abc", "def", "ghi", "jkl",
                                                "mno", "pqrs", "tuv", "wxyz"};
        std::vector<std::string> out = {""};
        for (char dg : digits) {
            std::vector<std::string> next;
            for (const auto& prefix : out)
                for (char ch : map[dg - '2'])
                    next.push_back(prefix + ch);
            out = std::move(next);
        }
        return out;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    struct Case { std::string d; int want; };
    const Case cases[] = {{"23", 9}, {"", 0}, {"2", 3}, {"999", 64}};
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        int r1 = static_cast<int>(Solution_1().letterCombinations(c.d).size());
        int r2 = static_cast<int>(Solution_2().letterCombinations(c.d).size());
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "\"" << c.d << "\" → A1=" << r1 << " A2=" << r2
                  << " (want " << c.want << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
