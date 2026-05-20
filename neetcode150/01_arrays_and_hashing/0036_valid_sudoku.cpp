/*
 * LeetCode 36: Valid Sudoku
 * Link: https://leetcode.com/problems/valid-sudoku/
 * Difficulty: Medium
 */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// ============= Variation 1: Brute Force =============
// Algorithm: Check rows by iterating each row, cols by iterating each col.
// Then use nested loops stepping by 3 to validate each 3x3 subgrid.
// Time: O(81) = O(1)  Space: O(81) = O(1)
class Solution_v1 {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        for (int i = 0; i < 9; i++) {
            unordered_set<char> row, col;
            for (int j = 0; j < 9; j++) {
                if (board[i][j] != '.') { if (row.count(board[i][j])) return false; row.insert(board[i][j]); }
                if (board[j][i] != '.') { if (col.count(board[j][i])) return false; col.insert(board[j][i]); }
            }
        }
        for (int br = 0; br < 3; br++)
            for (int bc = 0; bc < 3; bc++) {
                unordered_set<char> box;
                for (int r = 0; r < 3; r++)
                    for (int c = 0; c < 3; c++) {
                        char v = board[br*3+r][bc*3+c];
                        if (v != '.') { if (box.count(v)) return false; box.insert(v); }
                    }
            }
        return true;
    }
};

// ============= Variation 2: Single Pass =============
// Algorithm: Map cell indices to unique string identifiers (e.g. "5r0" for 5 in row 0).
// If an identifier is already in our set, then a duplicate exists.
// Time: O(81) = O(1)  Space: O(81) = O(1)
class Solution_v2 {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        unordered_set<string> seen;
        for (int r = 0; r < 9; r++)
            for (int c = 0; c < 9; c++) {
                char v = board[r][c];
                if (v == '.') continue;
                string rv = string(1, v) + "r" + to_string(r);
                string cv = string(1, v) + "c" + to_string(c);
                string bv = string(1, v) + "b" + to_string(r/3) + to_string(c/3);
                if (seen.count(rv) || seen.count(cv) || seen.count(bv)) return false;
                seen.insert(rv); seen.insert(cv); seen.insert(bv);
            }
        return true;
    }
};

int main() {
    vector<vector<char>> board = {
        {'5','3','.','.','7','.','.','.','.'},
        {'6','.','.','1','9','5','.','.','.'},
        {'.','9','8','.','.','.','.','6','.'},
        {'8','.','.','.','6','.','.','.','3'},
        {'4','.','.','8','.','3','.','.','1'},
        {'7','.','.','.','2','.','.','.','6'},
        {'.','6','.','.','.','.','2','8','.'},
        {'.','.','.','4','1','9','.','.','5'},
        {'.','.','.','.','8','.','.','7','9'}
    };

    {
        auto data = board;
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v1().isValidSudoku(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var1 (Brute Force): result=" << res << ", time = " << us << " µs" << endl;
    }
    {
        auto data = board;
        auto start = chrono::high_resolution_clock::now();
        bool res = Solution_v2().isValidSudoku(data);
        auto end = chrono::high_resolution_clock::now();
        double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
        cout << "var2 (Single Pass): result=" << res << ", time = " << us << " µs" << endl;
    }
    return 0;
}

// var1 mem = N/A and time = 13.684 µs
// var2 mem = N/A and time = 38.066 µs
