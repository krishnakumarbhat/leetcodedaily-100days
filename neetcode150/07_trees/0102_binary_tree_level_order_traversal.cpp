/*
 * =====================================================================
 * LeetCode 102 : Binary Tree Level Order Traversal                  (Medium)
 * https://leetcode.com/problems/binary-tree-level-order-traversal/
 * Category   : Trees — BFS
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, return a vector of vectors: one
 *   vector per LEVEL, listing that level's values left → right.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A level IS a frontier: the set of nodes at depth d. BFS processes
 *   the tree exactly one frontier at a time — if we snapshot the whole
 *   queue before expanding it, each snapshot is one output row. The
 *   queue is thus both the work list AND the level delimiter.
 * ---------------------------------------------------------------------
 * APPROACH 1 — BFS with a per-level snapshot (BEST)
 *   At each iteration record size = queue.size(), pop exactly `size`
 *   nodes into one row, enqueue their children for the next row.
 *   Time  Complexity : O(n)  — every node enters/leaves the queue once.
 *   Space Complexity : O(n)  — queue holds at most a full level
 *                              (worst: all leaves of a balanced tree).
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS with depth-indexed rows (no queue at all)
 *   Recursively visit nodes carrying their depth; append each value
 *   into rows[depth] (growing the vector on first visit to a depth).
 *   Same output, different traversal order (preorder instead of BFS).
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, plus O(n) for the answer.
 * ---------------------------------------------------------------------
 * DEEP DIVE — queue = the classic level-order machine
 *   FIFO is THE container for breadth-first walks: a node's children
 *   are appended AFTER everything already queued, so nodes at depth d
 *   are always processed before any node at depth d+1. Stacks would
 *   produce DFS (depth-first) instead. The "snapshot the size first"
 *   trick converts a FIFO stream into explicit level boundaries —
 *   the same pattern powers right-side view and zigzag traversal.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — rows output / level-order tests
#include <queue>          // std::queue — FIFO used by approach 1
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : BFS with per-level snapshots
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the tree's values level by level, left → right.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : vector of rows; row i holds depth-i nodes' values.
     */
    std::vector<std::vector<int>> levelOrder(TreeNode* root) {
        std::vector<std::vector<int>> rows;   // one vector per level
        if (root == nullptr) {
            return rows;                      // empty tree → empty output
        }

        std::queue<TreeNode*> pending;        // FIFO of the next frontier
        pending.push(root);

        // While any nodes remain, slice off one full level at a time.
        while (!pending.empty()) {
            std::vector<int> row;
            // Snapshot size BEFORE expanding: exactly this many nodes
            // form the current level — children join for the NEXT one.
            int level_size = static_cast<int>(pending.size());
            for (int i = 0; i < level_size; ++i) {
                TreeNode* cur = pending.front();
                pending.pop();
                row.push_back(cur->val);      // collect this level's value
                // Children are the next frontier — appended behind any
                // nodes of the CURRENT level still in the queue.
                if (cur->left != nullptr) {
                    pending.push(cur->left);
                }
                if (cur->right != nullptr) {
                    pending.push(cur->right);
                }
            }
            rows.push_back(row);              // commit the finished level
        }
        return rows;
    }
};

/* =====================================================================
 * APPROACH 2 : DFS with depth-indexed rows
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the tree's values level by level, left → right.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : vector of rows; row i holds depth-i nodes' values.
     */
    std::vector<std::vector<int>> levelOrder(TreeNode* root) {
        std::vector<std::vector<int>> rows;
        walk(root, 0, rows);                  // root sits at depth 0
        return rows;
    }

private:
    /* Purpose : Preorder visit carrying the node's depth.
       Inputs  : node — current node; depth — its distance from root;
                 rows — output, grown on first visit to each depth.
       Output  : nothing (appends node->val into rows[depth]). */
    void walk(TreeNode* node, int depth, std::vector<std::vector<int>>& rows) {
        // No node → nothing to record at this position.
        if (node == nullptr) {
            return;
        }
        // First visit to this depth → allocate its row.
        if (depth == static_cast<int>(rows.size())) {
            rows.push_back({});
        }
        rows[depth].push_back(node->val);     // preorder: root first
        walk(node->left, depth + 1, rows);    // then the whole left subtree
        walk(node->right, depth + 1, rows);   // then the whole right subtree
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: the official example → [[3],[9,20],[15,7]].
    TreeNode* t1 = buildTree({3, 9, 20, std::nullopt, std::nullopt, 15, 7});
    // Test 2: single node → [[1]].
    TreeNode* t2 = buildTree({1});
    // Test 3: skewed chain → one row per node.
    TreeNode* t3 = buildTree({1, 2, std::nullopt, 3});
    // Expected rows for verification.
    const std::vector<std::vector<int>> expected[3] = {
        {{3}, {9, 20}, {15, 7}}, {{1}}, {{1}, {2}, {3}}
    };

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    std::vector<std::vector<int>> r1[3] = {Solution_1().levelOrder(t1),
                                           Solution_1().levelOrder(t2),
                                           Solution_1().levelOrder(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    std::vector<std::vector<int>> r2[3] = {Solution_2().levelOrder(t1),
                                           Solution_2().levelOrder(t2),
                                           Solution_2().levelOrder(t3)};
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

    std::cout << "Solution_1 (BFS snapshots)    : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (DFS + depth rows) : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : both produce the expected levels."
                         : "FAIL : at least one output differs.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t3);
    return 0;
}
