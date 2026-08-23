/*
 * =====================================================================
 * LeetCode 36 : Valid Sudoku                                    (Medium)
 * https://leetcode.com/problems/valid-sudoku/
 * Category   : Arrays & Hashing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Determine if a 9×9 Sudoku board is VALID — no repeated digits
 *   in any row, column, or 3×3 box. Empty cells ('.') are ignored.
 *   (The board is NOT required to be solvable.)
 * ---------------------------------------------------------------------
 * INTUITION
 *   Three independent "no duplicates" checks: one per row, per column,
 *   per box. A duplicate check is a hash-set membership test; with a
 *   fixed universe of 9 digits we can compress each set into a single
 *   9-bit integer (a BITMASK): bit d set ⟺ digit d already seen.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Bitmask per row / column / box (MEMORY-OPTIMAL)
 *   rows[9], cols[9], boxes[9] : one 9-bit int each.
 *   For every digit d at (r,c): if its bit is already set in the
 *   row/col/box mask → duplicate → invalid. Else set the bit.
 *   Box index = (r/3)*3 + c/3  — the 3×3 group containing (r,c).
 *   Time  Complexity : O(9²) = O(81) constant   Space : O(9+9+9) ints.
 *   WHY bitmasks: 27 ints ≈ 108 bytes total. A set-based version
 *   needs 27 containers with hashing overhead. Same O() class,
 *   drastically smaller constants.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Python set of (row, digit) / (col, digit) / (box, digit)
 *   One set, keys are tuples — simplest to write, uses hashing.
 *   Time  Complexity : O(81)   Space Complexity : O(81).
 *   Pedagogical contrast: hash sets trade memory for simplicity;
 *   bitmasks trade a little cleverness for compactness.
 * =====================================================================
 */

#include <vector>          // std::vector — board rows
#include <string>          // std::string — each board row is 9 chars
#include <chrono>          // timing for the benchmark
#include <iostream>        // std::cout — benchmark output
#include <sys/resource.h>  // getrusage — peak RAM measurement

using namespace std;

/* =====================================================================
 * APPROACH 1 : Bitmask per row / column / box — 27 ints total
 * ===================================================================== */
class Solution_Bitmask {
public:
    /*
     * Purpose : Validate a Sudoku board's rows/cols/boxes.
     * Inputs  : board — 9 strings of length 9 with digits or '.'.
     * Output  : true when no digit repeats in any row/col/box.
     */
    bool isValidSudoku(const vector<string>& board) {

        // One 9-bit mask per row, per column, per box — bit d = digit d+1.
        int rows[9] = {0};
        int cols[9] = {0};
        int boxes[9] = {0};

        // Visit every one of the 81 cells exactly once.
        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {

                // Empty cells impose no constraint — skip them.
                if (board[r][c] == '.') {
                    continue;
                }

                // Map digit '1'..'9' to bit 0..8 and lift it to a mask.
                int bit = 1 << (board[r][c] - '1');

                // The 3×3 box containing (r,c): row-group*3 + col-group.
                int box = (r / 3) * 3 + (c / 3);

                // If the bit is already set in ANY of the three masks,
                // this digit repeats inside that row/col/box → invalid.
                if ((rows[r] & bit) || (cols[c] & bit) || (boxes[box] & bit)) {
                    return false;
                }

                // First sighting → record it in all three masks.
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[box] |= bit;
            }
        }
        return true;
    }
};

/* =====================================================================
 * APPROACH 2 : Three hash-set families (simpler, more memory)
 * ===================================================================== */
class Solution_SetOfTuples {
public:
    /*
     * Purpose : Validate a Sudoku board (set-of-tuples variant).
     * Inputs  : board — 9 strings of length 9 with digits or '.'.
     * Output  : true when no digit repeats in any row/col/box.
     */
    bool isValidSudoku(const vector<string>& board) {

        // seen : every (owner, digit) pair already placed on the board.
        // "3-1-5" = row 3 has digit 5; "c-2-8" = column 2 has 8; etc.
        vector<string> seen;

        // Visit every cell once.
        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {
                char d = board[r][c];
                if (d == '.') {
                    continue;  // empty → no constraint
                }

                // Encode the three ownership claims as strings.
                string rowKey = "r" + to_string(r) + "-" + d;
                string colKey = "c" + to_string(c) + "-" + d;
                string boxKey = "b" + to_string((r / 3) * 3 + (c / 3)) + "-" + d;

                // Any claim already present → duplicate → invalid.
                for (const string& key : {rowKey, colKey, boxKey}) {
                    for (const string& s : seen) {
                        if (s == key) {
                            return false;
                        }
                    }
                    seen.push_back(key);
                }
            }
        }
        return true;
    }
};

/* =====================================================================
 * BENCHMARK — time + peak RAM for both approaches
 * ===================================================================== */
int main() {
    // The official VALID example board.
    vector<string> board = {
        "53..7....",
        "6..195...",
        ".98....6.",
        "8...6...3",
        "4..8.3..1",
        "7...2...6",
        ".6....28.",
        "...419..5",
        "....8..79"
    };

    // --- Approach 1 ---
    struct rusage b1, a1;
    getrusage(RUSAGE_SELF, &b1);
    auto s1 = chrono::high_resolution_clock::now();
    bool r1 = Solution_Bitmask().isValidSudoku(board);
    auto e1 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a1);
    double us1 = chrono::duration_cast<chrono::nanoseconds>(e1 - s1).count() / 1000.0;
    long mem1 = (a1.ru_maxrss - b1.ru_maxrss) / 1024;

    // --- Approach 2 ---
    struct rusage b2, a2;
    getrusage(RUSAGE_SELF, &b2);
    auto s2 = chrono::high_resolution_clock::now();
    bool r2 = Solution_SetOfTuples().isValidSudoku(board);
    auto e2 = chrono::high_resolution_clock::now();
    getrusage(RUSAGE_SELF, &a2);
    double us2 = chrono::duration_cast<chrono::nanoseconds>(e2 - s2).count() / 1000.0;
    long mem2 = (a2.ru_maxrss - b2.ru_maxrss) / 1024;

    cout << "Approach 1 (bitmask)         : " << (r1 ? "true" : "false")
         << "  time = " << us1 << " µs  peak-ram-delta = " << mem1 << " MB\n";
    cout << "Approach 2 (set of tuples)   : " << (r2 ? "true" : "false")
         << "  time = " << us2 << " µs  peak-ram-delta = " << mem2 << " MB\n";

    cout << ((r1 == r2) ? "PASS : both approaches agree."
                        : "FAIL : approaches disagree.")
         << "\n";
    return 0;
}