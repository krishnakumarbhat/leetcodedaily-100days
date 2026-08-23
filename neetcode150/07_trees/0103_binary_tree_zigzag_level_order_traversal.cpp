/*
 * =====================================================================
 * LeetCode 103 : Binary Tree Zigzag Level Order Traversal            (Medium)
 * https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
 * Category   : Trees — BFS + direction flips
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Return the level-order values, but ALTERNATE direction per level:
 *   level 0 left→right, level 1 right→left, level 2 left→right, …
 *   ("zigzag")
 * ---------------------------------------------------------------------
 * INTUITION
 *   A level's values are collected left→right by ordinary BFS; the
 *   zigzag is purely a PRESENTATION choice — reverse every ODD level
 *   before reporting it. Equivalently, keep a direction flag and
 *   flip it after each finished level.
 * ---------------------------------------------------------------------
 * APPROACH 1 — BFS + reverse odd levels (BEST, clearest)
 *   Standard per-level snapshot loop; after collecting a row, reverse
 *   it when its index is odd.
 *   Time  Complexity : O(n)  — each node processed once; reversing a
 *                        row is linear in its own size.
 *   Space Complexity : O(n)  — BFS queue width (≤ n).
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS with depth-indexed rows + parity reversal
 *   Collect rows exactly like 0102's DFS variant (preorder into
 *   rows[depth]), then reverse every odd-indexed row at the end.
 *   Time  Complexity : O(n)  — one DFS + one sweep over all rows.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * DEEP DIVE — when to reverse: inline flag vs end-of-pass
 *   Both approaches compute the SAME zigzag; the difference is WHERE
 *   the reversal happens. The BFS flag flips per level during the
 *   walk (queue discipline); the DFS variant defers all reversals to
 *   one final pass over the rows. Same cost, different code — the
 *   deferred version is easier to verify because the plain level-
 *   order result stays visible before the flip.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — rows output / level-order tests
#include <queue>          // std::queue — FIFO used by approach 1
#include <algorithm>      // std::reverse — flipping odd rows
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : BFS with per-level direction flip
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return level-order values, alternating direction.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : rows; odd rows are right→left.
     */
    std::vector<std::vector<int>> zigzagLevelOrder(TreeNode* root) {
        std::vector<std::vector<int>> rows;
        if (root == nullptr) {
            return rows;
        }
        std::queue<TreeNode*> pending;   // FIFO — next frontier
        pending.push(root);
        int level = 0;                   // parity decides the direction

        while (!pending.empty()) {
            int level_size = static_cast<int>(pending.size());
            std::vector<int> row;
            for (int i = 0; i < level_size; ++i) {
                TreeNode* cur = pending.front();
                pending.pop();
                row.push_back(cur->val);
                if (cur->left != nullptr) {
                    pending.push(cur->left);
                }
                if (cur->right != nullptr) {
                    pending.push(cur->right);
                }
            }
            // Odd levels are collected left→right but reported reversed.
            if (level % 2 == 1) {
                std::reverse(row.begin(), row.end());
            }
            rows.push_back(row);
            ++level;                     // next level flips direction
        }
        return rows;
    }
};

/* =====================================================================
 * APPROACH 2 : DFS rows + deferred parity reversal
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return level-order values, alternating direction.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : rows; odd rows are right→left.
     */
    std::vector<std::vector<int>> zigzagLevelOrder(TreeNode* root) {
        std::vector<std::vector<int>> rows;
        walk(root, 0, rows);             // preorder fills rows by depth
        // One deferred pass flips every odd row — the zigzag rule.
        for (int i = 1; i < static_cast<int>(rows.size()); i += 2) {
            std::reverse(rows[i].begin(), rows[i].end());
        }
        return rows;
    }

private:
    /* Purpose : Preorder fill of rows[depth].
       Inputs  : node — current node; depth — its distance from root;
                 rows — output, grown on first visit to each depth.
       Output  : nothing (appends node->val into rows[depth]). */
    void walk(TreeNode* node, int depth, std::vector<std::vector<int>>& rows) {
        if (node == nullptr) {
            return;
        }
        if (depth == static_cast<int>(rows.size())) {
            rows.push_back({});
        }
        rows[depth].push_back(node->val);
        walk(node->left, depth + 1, rows);
        walk(node->right, depth + 1, rows);
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example → [[3],[20,9],[15,7]].
    TreeNode* t1 = buildTree({3, 9, 20, std::nullopt, std::nullopt, 15, 7});
    // Test 2: single node → [[1]].
    TreeNode* t2 = buildTree({1});
    // Test 3: empty tree → [].
    TreeNode* t3 = nullptr;
    const std::vector<std::vector<int>> expected[3] = {
        {{3}, {20, 9}, {15, 7}}, {{1}}, {}
    };

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    std::vector<std::vector<int>> r1[3] = {Solution_1().zigzagLevelOrder(t1),
                                           Solution_1().zigzagLevelOrder(t2),
                                           Solution_1().zigzagLevelOrder(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    std::vector<std::vector<int>> r2[3] = {Solution_2().zigzagLevelOrder(t1),
                                           Solution_2().zigzagLevelOrder(t2),
                                           Solution_2().zigzagLevelOrder(t3)};
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB on Linux
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    bool all_ok = true;
    for (int i = 0; i < 3; ++i) {
        bool ok = (r1[i] == expected[i]) && (r2[i] == expected[i]);
        all_ok = all_ok && ok;
        std::cout << "Test " << (i + 1) << ": S1 rows=" << r1[i].size()
                  << " S2 rows=" << r2[i].size()
                  << " (expected " << expected[i].size() << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (BFS + flip)         : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (DFS + deferred flip): time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : both zigzags match expected."
                         : "FAIL : at least one zigzag differs.")
              << "\n";

    destroyTree(t1); destroyTree(t2);
    return 0;
}