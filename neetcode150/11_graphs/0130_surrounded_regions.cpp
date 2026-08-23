/*
 * =====================================================================
 * LeetCode 130 : Surrounded Regions                                   (Medium)
 * https://leetcode.com/problems/surrounded-regions/
 * Category   : Graphs
 * ---------------------------------------------------------------------
 * PROBLEM
 *   An m×n board of 'X' and 'O'. Flip every 'O' that is NOT connected
 *   to the border through other 'O's into 'X'. Border 'O's (and any
 *   'O' reachable from them) survive.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The condition "surrounded" is really about REACHABILITY: an 'O'
 *   must be flipped iff it cannot walk to the board's edge. So flip
 *   the problem — instead of testing every 'O', find all 'O's that
 *   CAN reach the border (multi-source search from every border 'O'),
 *   mark them, then flip every unmarked 'O'. That is one flood fill
 *   pass instead of a per-cell search.
 * ---------------------------------------------------------------------
 * APPROACH 1 — BFS from every border 'O' (BEST)
 *   Queue all border 'O's, mark 'E' (escape). BFS through 4-direction
 *   neighbours; any 'O' reached also escapes. Finally flip all 'O'
 *   that were never marked 'E'.
 *   Time  Complexity : O(m·n)  — every cell touched a constant times.
 *   Space Complexity : O(m·n)  — worst-case queue + board mutation.
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS recursion from every border 'O'
 *   Same reachability idea, but recursion does the traversal. The
 *   call stack can reach O(m·n) depth on a snake-shaped island —
 *   real risk of stack overflow on large boards.
 *   Time  Complexity : O(m·n)   Space Complexity : O(m·n) (stack).
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — grid graphs & the dirs array
 *   A grid IS a graph: cell (r,c) is a node; edges go to its 4
 *   neighbours. The canonical trick is the DIRS array:
 *         dirs = {(-1,0),(1,0),(0,-1),(0,1)}
 *   — one loop over 4 offsets replaces four copy-pasted branches.
 *   BFS vs DFS here: identical worst-case complexity; BFS avoids the
 *   recursion depth trap of a long winding island. DFS is slightly
 *   simpler to write recursively. Both must guard bounds BEFORE
 *   probing the cell (r<0 || r>=m || c<0 || c>=n → skip).
 * =====================================================================
 */

#include <iostream>         // std::cout — printing benchmark results
#include <vector>           // std::vector — the 2D board
#include <string>           // std::string — board rows
#include <queue>            // std::queue — BFS frontier
#include <unordered_map>    // std::unordered_map — hash table (chaining)
#include <unordered_set>    // std::unordered_set — visited set
#include <chrono>           // std::chrono — high-resolution timing
#include <sys/resource.h>   // getrusage — peak RAM measurement
#include <utility>          // std::pair — (r,c) coordinates

/* =====================================================================
 * APPROACH 1 : Multi-source BFS from every border 'O'
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Flip surrounded 'O' regions into 'X' in place.
     * Inputs  : board — m×n grid of 'X'/'O' (mutated in place).
     * Output  : void — board modified so only border-connected 'O'
     *           survive.
     */
    void solve(std::vector<std::vector<char>>& board) {
        int m = static_cast<int>(board.size());
        if (m == 0) return;              // empty board — nothing to do
        int n = static_cast<int>(board[0].size());

        // Frontier of every border 'O' — a multi-source BFS start set.
        std::queue<std::pair<int, int>> q;
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                // Only cells ON the rim can seed the escape wave.
                bool border = (r == 0 || r == m - 1 || c == 0 || c == n - 1);
                if (border && board[r][c] == 'O') {
                    board[r][c] = 'E';   // 'E' = escapes (temporary mark)
                    q.push({r, c});
                }
            }
        }

        // dirs : the 4 cardinal offsets — one loop over 4 neighbours.
        const int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        // BFS: any 'O' reachable from a border 'O' escapes too.
        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            for (int d = 0; d < 4; ++d) {
                int nr = r + dirs[d][0];
                int nc = c + dirs[d][1];
                // Bounds guard FIRST — never index outside the grid.
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                if (board[nr][nc] != 'O') continue; // only unvisited 'O'
                board[nr][nc] = 'E';     // claim: this cell escapes
                q.push({nr, nc});
            }
        }

        // Final sweep: 'E' reverts to 'O'; any remaining 'O' is truly
        // enclosed → flip to 'X'.
        for (int r = 0; r < m; ++r) {
            for (int c = 0; c < n; ++c) {
                if (board[r][c] == 'E') board[r][c] = 'O';
                else if (board[r][c] == 'O') board[r][c] = 'X';
            }
        }
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive DFS from every border 'O'
 * ===================================================================== */
class Solution_2 {
private:
    // Member state so the recursive helper needs no extra parameters.
    int m_, n_;
    std::vector<std::vector<char>>* b_;

    /*
     * Purpose : Flood-fill 'O' cells reachable from (r,c) with 'E'.
     * Inputs  : r, c — current cell; preconditions: in bounds, is 'O'.
     * Output  : void — mutates the board through pointer member b_.
     */
    void dfs(int r, int c) {
        // Recursion guard: stop at walls, visited cells, or the rim.
        if (r < 0 || r >= m_ || c < 0 || c >= n_) return;
        if ((*b_)[r][c] != 'O') return;
        (*b_)[r][c] = 'E';   // mark as escaping BEFORE recursing — the
                             // classic "mark-on-entry" anti-cycle guard.
        dfs(r - 1, c);       // up
        dfs(r + 1, c);       // down
        dfs(r, c - 1);       // left
        dfs(r, c + 1);       // right
    }

public:
    /*
     * Purpose : Flip surrounded 'O' regions into 'X' in place.
     * Inputs  : board — m×n grid of 'X'/'O' (mutated in place).
     * Output  : void — board modified so only border-connected 'O'
     *           survive.
     */
    void solve(std::vector<std::vector<char>>& board) {
        m_ = static_cast<int>(board.size());
        if (m_ == 0) return;
        n_ = static_cast<int>(board[0].size());
        b_ = &board;

        // Seed DFS from every border 'O' — same multi-source idea as
        // BFS, just recursive traversal.
        for (int r = 0; r < m_; ++r) {
            for (int c = 0; c < n_; ++c) {
                bool border = (r == 0 || r == m_ - 1 || c == 0 || c == n_ - 1);
                if (border && board[r][c] == 'O') dfs(r, c);
            }
        }

        // Same final sweep: 'E' → 'O', leftover 'O' → 'X'.
        for (int r = 0; r < m_; ++r) {
            for (int c = 0; c < n_; ++c) {
                if (board[r][c] == 'E') board[r][c] = 'O';
                else if (board[r][c] == 'O') board[r][c] = 'X';
            }
        }
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 tests, compare full boards
 * ===================================================================== */
int main() {
    // Test 1 (official): center 2×2 enclosed; border ring survives.
    std::vector<std::vector<char>> b1 = {
        {'X', 'X', 'X', 'X'},
        {'X', 'O', 'O', 'X'},
        {'X', 'X', 'O', 'X'},
        {'X', 'O', 'X', 'X'}
    };
    // Test 2 (official): single border 'O' → nothing flipped.
    std::vector<std::vector<char>> b2 = {
        {'X'}
    };
    // Test 3: 'O' column touching the rim saves the whole corridor.
    std::vector<std::vector<char>> b3 = {
        {'O', 'X', 'X'},
        {'O', 'X', 'O'},
        {'O', 'O', 'O'}
    };
    std::vector<std::vector<std::vector<char>>> tests = {b1, b2, b3};

    bool allPass = true;
    for (int t = 0; t < 3; ++t) {
        // --- Approach 1 timing + memory (on a fresh copy each time) ---
        auto boardA = tests[t];
        struct rusage before1, after1;
        getrusage(RUSAGE_SELF, &before1);
        auto s1 = std::chrono::high_resolution_clock::now();
        Solution_1().solve(boardA);
        auto e1_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after1);

        // --- Approach 2 timing + memory ---
        auto boardB = tests[t];
        struct rusage before2, after2;
        getrusage(RUSAGE_SELF, &before2);
        auto s2 = std::chrono::high_resolution_clock::now();
        Solution_2().solve(boardB);
        auto e2_ = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after2);

        long mem1 = (after1.ru_maxrss - before1.ru_maxrss);
        long mem2 = (after2.ru_maxrss - before2.ru_maxrss);
        double us1 = std::chrono::duration_cast<std::chrono::nanoseconds>(e1_ - s1).count() / 1000.0;
        double us2 = std::chrono::duration_cast<std::chrono::nanoseconds>(e2_ - s2).count() / 1000.0;

        // Both approaches must produce IDENTICAL final boards.
        bool same = (boardA == boardB);
        // Spot-verify against the known official result for test 1.
        bool known = true;
        if (t == 0) {
            std::vector<std::vector<char>> expect = {
                {'X', 'X', 'X', 'X'},
                {'X', 'X', 'X', 'X'},
                {'X', 'X', 'X', 'X'},
                {'X', 'O', 'X', 'X'}
            };
            known = (boardA == expect);
        }
        bool ok = same && known;
        allPass = allPass && ok;

        std::cout << "Test " << (t + 1) << (ok ? " PASS" : " FAIL")
                  << " | A1 time=" << us1 << " µs mem=" << mem1 << " KB"
                  << " | A2 time=" << us2 << " µs mem=" << mem2 << " KB\n";
        if (!ok) {
            std::cout << "  A1 board:\n";
            for (const auto& row : boardA) {
                for (char c : row) std::cout << c;
                std::cout << "\n";
            }
            std::cout << "  A2 board:\n";
            for (const auto& row : boardB) {
                for (char c : row) std::cout << c;
                std::cout << "\n";
            }
        }
    }
    std::cout << (allPass ? "PASS : all tests green on both approaches.\n"
                          : "FAIL : at least one test/approach disagrees.\n");
    return 0;
}