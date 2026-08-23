/*
 * =====================================================================
 * LeetCode 543 : Diameter of Binary Tree                             (Easy)
 * https://leetcode.com/problems/diameter-of-binary-tree/
 * Category   : Trees — post-order info passing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, return its DIAMETER — the number
 *   of EDGES on the longest path between any two nodes. The path does
 *   not have to pass through the root.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Any longest path has a HIGHEST node. At that node the path is
 *   exactly: (longest downward chain in the LEFT subtree) + (longest
 *   downward chain in the RIGHT subtree). So per node, the candidate
 *   is leftHeight + rightHeight — and the global answer is the max of
 *   every candidate. Post-order hands each node its children's
 *   heights for free: one walk, all candidates.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Post-order (height, best) pair (BEST)
 *   dfs(node) returns the node's height (for its parent's candidate)
 *   while a shared `best` tracks max(leftH + rightH) across all nodes.
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Node-by-node recomputation (contrast)
 *   For every node compute height(left) + height(right) with a
 *   separate height() helper — the classic accidental O(n²).
 *   Time  Complexity : O(n²)  worst — heights recomputed per ancestor.
 *   Space Complexity : O(h)   — interleaved call stacks.
 *   WHY SHOW IT: identical formula, quadratic price — the exact cost
 *   of NOT passing information up the tree.
 * ---------------------------------------------------------------------
 * DEEP DIVE — the (height, best) two-value pattern
 *   This is the same post-order DP as max path sum and balanced tree:
 *   the node's own candidate combines BOTH children (leftH + rightH),
 *   but the value passed UP is a single-branch summary (height).
 *   Encoded as an int return + an out-param/global, no struct needed:
 *       best  = max(best,  lh + rh)      ← "bent" path, stays local
 *       return max(lh, rh) + 1           ← "straight" chain, goes up
 *   Watch it in the animation: every node reports its height while
 *   the running best silently updates.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <algorithm>      // std::max — folding the best candidate
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Post-order — height up, best sideways
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the longest edge-path between any two nodes.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : diameter in edges; 0 for empty/single-node trees.
     */
    int diameterOfBinaryTree(TreeNode* root) {
        best = 0;                        // reset per call
        height(root);
        return best;
    }

private:
    int best;                            // max leftH + rightH seen so far

    /* Purpose : Height of `node`, folding its diameter candidate in.
       Inputs  : node — current subtree root (may be nullptr).
       Output  : subtree height (edges to its deepest leaf). */
    int height(TreeNode* node) {
        // Empty subtree: height 0, no candidate to consider.
        if (node == nullptr) {
            return 0;
        }
        // Children FIRST — their heights arrive bottom-up.
        int left_h = height(node->left);
        int right_h = height(node->right);
        // The longest path THROUGH this node bends here: one edge into
        // the left chain + one edge into the right chain.
        best = std::max(best, left_h + right_h);
        // But the PARENT can only continue along one chain — height.
        return (left_h > right_h ? left_h : right_h) + 1;
    }
};

/* =====================================================================
 * APPROACH 2 : For-every-node recomputation (O(n²) contrast)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the longest edge-path between any two nodes.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : diameter in edges; 0 for empty/single-node trees.
     */
    int diameterOfBinaryTree(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        // Candidate at the root: left chain + right chain through it.
        int through_root = height(root->left) + height(root->right);
        // Then recurse — the best path may skip the root entirely.
        int left_best = diameterOfBinaryTree(root->left);
        int right_best = diameterOfBinaryTree(root->right);
        // Best of the three candidates.
        int m = std::max(through_root, left_best);
        return std::max(m, right_best);
    }

private:
    /* Purpose : Plain subtree height, recomputed on every call.
       Inputs  : node — subtree root (may be nullptr).
       Output  : number of edges to the deepest leaf. */
    int height(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        int l = height(node->left);
        int r = height(node->right);
        return (l > r ? l : r) + 1;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — diameter 3 (path 4→2→5 or 5→2→3).
    TreeNode* t1 = buildTree({1, 2, 3, 4, 5});
    // Test 2: single node → diameter 0.
    TreeNode* t2 = buildTree({1});
    // Test 3: chain 1→2→3→4 (level-order) → diameter 3 (edge count).
    TreeNode* t3 = buildTree({1, 2, std::nullopt, 3, std::nullopt, std::nullopt, 4});
    const int expected[3] = {3, 0, 3};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    int r1[3] = {Solution_1().diameterOfBinaryTree(t1),
                 Solution_1().diameterOfBinaryTree(t2),
                 Solution_1().diameterOfBinaryTree(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    int r2[3] = {Solution_2().diameterOfBinaryTree(t1),
                 Solution_2().diameterOfBinaryTree(t2),
                 Solution_2().diameterOfBinaryTree(t3)};
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
        std::cout << "Test " << (i + 1) << ": S1=" << r1[i] << " S2=" << r2[i]
                  << " (expected " << expected[i] << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (post-order, O(n))   : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (node-by-node, O(n²)): time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all diameters match expected."
                         : "FAIL : at least one diameter is wrong.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t3);
    return 0;
}