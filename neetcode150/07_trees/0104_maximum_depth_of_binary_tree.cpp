/*
 * =====================================================================
 * LeetCode 104 : Maximum Depth of Binary Tree                         (Easy)
 * https://leetcode.com/problems/maximum-depth-of-binary-tree/
 * Category   : Trees — recursion fundamentals
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, return its MAXIMUM DEPTH — the
 *   number of nodes along the longest root→leaf path. (Empty tree = 0.)
 * ---------------------------------------------------------------------
 * INTUITION
 *   The depth of a node is 1 + the deeper of its children's depths —
 *   a self-referential statement, so recursion is the natural fit:
 *   the base case (empty subtree → depth 0) stops the descent, and
 *   every level adds exactly one.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive post-order (BEST, canonical)
 *   Ask both children for their depths, take the max, add 1 for the
 *   current node. The answer assembles itself bottom-up.
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative BFS (count the levels)
 *   Process level by level with a queue; every finished level adds 1
 *   to a counter. No recursion at all — depth = number of rows.
 *   Time  Complexity : O(n)  — every node enqueued/dequeued once.
 *   Space Complexity : O(w)  — queue holds the widest level (≤ n).
 * ---------------------------------------------------------------------
 * DEEP DIVE — the recursion POST-ORDER shape
 *   Computing a value from children BEFORE acting on the node itself
 *   is a post-order pattern: the child answers arrive first, the
 *   parent's answer composes them. This exact shape powers max path
 *   sum, diameter and balanced-tree checks — every "climb back up
 *   with a summary value" problem. Approach 2 sidesteps recursion
 *   entirely because BFS measures depth horizontally, one level at a
 *   time — no call stack, but O(n) worst-case queue memory instead
 *   of O(h).
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <queue>          // std::queue — FIFO used by approach 2
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive post-order
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the maximum depth of `root`.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : number of nodes on the longest root→leaf path.
     */
    int maxDepth(TreeNode* root) {
        // Empty subtree contributes zero levels — the recursion's base.
        if (root == nullptr) {
            return 0;
        }
        // Ask both children, keep the taller one, add this node itself.
        // POST-ORDER: children are fully answered before the parent.
        int left_depth = maxDepth(root->left);
        int right_depth = maxDepth(root->right);
        return (left_depth > right_depth ? left_depth : right_depth) + 1;
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative BFS — count the levels
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the maximum depth of `root`.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : number of nodes on the longest root→leaf path.
     */
    int maxDepth(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        std::queue<TreeNode*> pending;   // FIFO — the next frontier
        pending.push(root);
        int depth = 0;

        // Each complete pass over the current queue = exactly one level.
        while (!pending.empty()) {
            int level_size = static_cast<int>(pending.size());
            // Drain this level entirely; children queue up behind it.
            for (int i = 0; i < level_size; ++i) {
                TreeNode* cur = pending.front();
                pending.pop();
                if (cur->left != nullptr) {
                    pending.push(cur->left);
                }
                if (cur->right != nullptr) {
                    pending.push(cur->right);
                }
            }
            ++depth;                     // one more level fully consumed
        }
        return depth;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example → depth 3.
    TreeNode* t1 = buildTree({3, 9, 20, std::nullopt, std::nullopt, 15, 7});
    // Test 2: single root → depth 1.
    TreeNode* t2 = buildTree({1});
    // Test 3: empty tree → depth 0.
    TreeNode* t3 = nullptr;
    // Test 4: left chain 1→2→3→4 → depth 4 (worst-case height).
    TreeNode* t4 = buildTree({1, 2, std::nullopt, 3, std::nullopt, std::nullopt, 4});
    const int expected[4] = {3, 1, 0, 4};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    int r1[4] = {Solution_1().maxDepth(t1), Solution_1().maxDepth(t2),
                 Solution_1().maxDepth(t3), Solution_1().maxDepth(t4)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    int r2[4] = {Solution_2().maxDepth(t1), Solution_2().maxDepth(t2),
                 Solution_2().maxDepth(t3), Solution_2().maxDepth(t4)};
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB on Linux
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    bool all_ok = true;
    for (int i = 0; i < 4; ++i) {
        bool ok = (r1[i] == expected[i]) && (r2[i] == expected[i]);
        all_ok = all_ok && ok;
        std::cout << "Test " << (i + 1) << ": S1=" << r1[i] << " S2=" << r2[i]
                  << " (expected " << expected[i] << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (recursive post-order): time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (iterative BFS)       : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all depths match expected."
                         : "FAIL : at least one depth is wrong.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t4);
    return 0;
}
