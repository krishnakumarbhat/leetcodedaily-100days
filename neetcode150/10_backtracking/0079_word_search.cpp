/*
 * =====================================================================
 * LeetCode 79  : Word Search                                         (Medium)
 * https://leetcode.com/problems/word-search/
 * Category   : Backtracking on a grid
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Does `word` exist as a path of ADJACENT cells (up/down/left/right)
 *   in an m×n board of letters? A cell may be used at most once.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Try every cell as the start; DFS match character by character,
 *   marking visited cells; un-mark when the branch fails (backtrack).
 * ---------------------------------------------------------------------
 * APPROACH 1 · DFS with in-place marking (best)
 *   dfs(i, j, k): board[i][j] must equal word[k]; mark with a sentinel
 *   ('#' or '0'), recurse 4 neighbours for k+1, restore the letter.
 * APPROACH 2 · visited[][] bitmap
 *   Same search but keep a separate bool grid (clearer, 1 extra array).
 * ---------------------------------------------------------------------
 * DEEP DIVE · Sentinel marking — the 1-byte state machine
 *   Instead of a visited[] array we overwrite the cell with a value
 *   that can never match a letter ('\0' or '#'), then restore it on
 *   unwind. This makes "used" implicit in the board itself — no
 *   allocation, perfect cache locality, and the restoration is forced
 *   (any buggy path that forgets to restore corrupts the board, which
 *   makes errors loud). Worst case with all cells matching the first
 *   letter: O(m·n·3^k) (3 neighbours after the first step).
 * ---------------------------------------------------------------------
 * TIME COMPLEXITY : O(m·n·3^L) worst, L = word length.
 * MEMORY COMPLEXITY: O(L) recursion depth.
 * =====================================================================
 */
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <sys/resource.h>

class Solution_1 {
    std::vector<std::vector<char>>* b_;
    std::string* w_;
    int m_, n_;
    bool dfs(int i, int j, int k) {
        if (k == static_cast<int>(w_->size())) return true;
        if (i < 0 || j < 0 || i >= m_ || j >= n_) return false;
        if ((*b_)[i][j] != (*w_)[k]) return false;
        char save = (*b_)[i][j];
        (*b_)[i][j] = '\0';                        // mark visited in-place
        bool ok = dfs(i + 1, j, k + 1) || dfs(i - 1, j, k + 1) ||
                  dfs(i, j + 1, k + 1) || dfs(i, j - 1, k + 1);
        (*b_)[i][j] = save;                        // un-mark (backtrack)
        return ok;
    }
public:
    bool exist(std::vector<std::vector<char>>& board, std::string word) {
        b_ = &board;
        w_ = &word;
        m_ = static_cast<int>(board.size());
        n_ = static_cast<int>(board[0].size());
        for (int i = 0; i < m_; ++i)
            for (int j = 0; j < n_; ++j)
                if (dfs(i, j, 0)) return true;
        return false;
    }
};

class Solution_2 {
    std::vector<std::vector<char>> b_;
    std::string w_;
    int m_, n_;
    bool dfs(int i, int j, int k, std::vector<std::vector<bool>>& vis) {
        if (k == static_cast<int>(w_.size())) return true;
        if (i < 0 || j < 0 || i >= m_ || j >= n_ || vis[i][j]) return false;
        if (b_[i][j] != w_[k]) return false;
        vis[i][j] = true;
        bool ok = dfs(i + 1, j, k + 1, vis) || dfs(i - 1, j, k + 1, vis) ||
                  dfs(i, j + 1, k + 1, vis) || dfs(i, j - 1, k + 1, vis);
        vis[i][j] = false;
        return ok;
    }
public:
    bool exist(std::vector<std::vector<char>>& board, std::string word) {
        b_ = board;
        w_ = word;
        m_ = static_cast<int>(board.size());
        n_ = static_cast<int>(board[0].size());
        std::vector<std::vector<bool>> vis(m_, std::vector<bool>(n_, false));
        for (int i = 0; i < m_; ++i)
            for (int j = 0; j < n_; ++j)
                if (dfs(i, j, 0, vis)) return true;
        return false;
    }
};

static long long nowUs() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();
}
static long memKb() { struct rusage r{}; getrusage(RUSAGE_SELF, &r); return r.ru_maxrss; }

int main() {
    std::vector<std::vector<char>> board = {
        {'A', 'B', 'C', 'E'}, {'S', 'F', 'C', 'S'}, {'A', 'D', 'E', 'E'}};
    struct Case { std::string w; bool want; };
    const Case cases[] = {{"ABCCED", true}, {"SEE", true}, {"ABCB", false}};
    const long mem0 = memKb();
    auto t0 = nowUs();
    bool allOk = true;
    for (const auto& c : cases) {
        auto b1 = board, b2 = board;
        bool r1 = Solution_1().exist(b1, c.w);
        bool r2 = Solution_2().exist(b2, c.w);
        bool ok = r1 == c.want && r2 == c.want;
        allOk = allOk && ok;
        std::cout << "\"" << c.w << "\" → A1=" << (r1 ? "T" : "F")
                  << " A2=" << (r2 ? "T" : "F") << " (want " << (c.want ? "T" : "F")
                  << ") " << (ok ? "PASS" : "FAIL") << "\n";
    }
    auto t1 = nowUs();
    std::cout << (allOk ? "PASS : all cases" : "FAIL") << " | time: " << (t1 - t0)
              << " us | mem: " << (memKb() - mem0) << " KB\n";
    return 0;
}
