/*
 * =====================================================================
 * LeetCode 110 : Balanced Binary Tree                                (Easy)
 * https://leetcode.com/problems/balanced-binary-tree/
 * Category   : Trees — post-order info passing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, decide whether it is HEIGHT-
 *   BALANCED: for every node, the heights of its two subtrees differ
 *   by at most 1 — and both subtrees are themselves balanced.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Balanced" needs two facts about each subtree: its HEIGHT (to
 *   compare siblings) and its BALANCEDNESS (to propagate up). Those
 *   are exactly the two values a single post-order pass can carry
 *   back: each node computes height = max(children) + 1 and flags
 *   itself unbalanced if |left_h - right_h| > 1 or either child was.
 *   One walk, both answers — no separate height recomputation.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Single post-order pass (BEST)
 *   dfs(node) returns the subtree height, or -1 as a sentinel meaning
 *   "unbalanced somewhere below". Every node is touched once.
 *   Time  Complexity : O(n)  — one visit per node.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Top-down double recursion (contrast)
 *   isBalanced(root) = |height(left) − height(right)| ≤ 1 AND
 *   balanced(left) AND balanced(right), recomputing height() per node.
 *   Time  Complexity : O(n²)  worst — height() re-walks subtrees for
 *                        every ancestor (skewed chain: 1+2+…+n).
 *   Space Complexity : O(h)   — two interleaved call stacks.
 *   WHY SHOW IT: the naive recursion looks identical but hides the
 *   O(n²) price — the classic "accidental quadratic".
 * ---------------------------------------------------------------------
 * DEEP DIVE — post-order info passing (the tree-DP pattern)
 *   "Return a compact summary from each subtree, compose at the node"
 *   is the fundamental pattern of tree DP: max path sum, diameter,
 *   and balanced checks are ALL this. The summary is a PAIR here —
 *   (height, balanced) — encoded cleverly as a single int: height ≥ 0,
 *   or -1 meaning "imbalanced". One value, two meanings, zero extra
 *   structs. Approach 2 shows the cost of NOT passing info up: every
 *   level re-asks the same subtree questions it already knew the
 *   answer to.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Single post-order pass, -1 sentinel for "unbalanced"
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether `root` is height-balanced.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : true iff every node's children differ by ≤ 1 in height
     *           and both subtrees are themselves balanced.
     */
    bool isBalanced(TreeNode* root) {
        // -1 from the walk = some subtree below was unbalanced.
        return height(root) != -1;
    }

private:
    /* Purpose : Post-order height probe with an imbalance sentinel.
       Inputs  : node — current subtree root (may be nullptr).
       Output  : subtree height (≥ 0), or -1 if unbalanced below. */
    int height(TreeNode* node) {
        // Empty subtree: height 0, trivially balanced.
        if (node == nullptr) {
            return 0;
        }
        // Children first — the answers flow BOTTOM-UP.
        int left_h = height(node->left);
        int right_h = height(node->right);
        // A child reporting -1 propagates the verdict unchanged.
        if (left_h == -1 || right_h == -1) {
            return -1;
        }
        // The balance rule at THIS node: heights differ by at most 1.
        int diff = left_h > right_h ? left_h - right_h : right_h - left_h;
        if (diff > 1) {
            return -1;
        }
        // Balanced here: height = taller child + 1, passed upward.
        return (left_h > right_h ? left_h : right_h) + 1;
    }
};

/* =====================================================================
 * APPROACH 2 : Top-down — recompute height() at every node (O(n²))
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether `root` is height-balanced.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : true iff every node passes the |Δheight| ≤ 1 rule.
     */
    bool isBalanced(TreeNode* root) {
        // Empty tree is trivially balanced.
        if (root == nullptr) {
            return true;
        }
        // Check the local rule at this node...
        int diff = height(root->left) - height(root->right);
        if (diff > 1 || diff < -1) {
            return false;
        }
        // ...AND recurse into both children. The waste: height() is
        // recomputed for EVERY ancestor — O(n) per node → O(n²).
        return isBalanced(root->left) && isBalanced(root->right);
    }

private:
    /* Purpose : Compute a subtree's height the plain recursive way.
       Inputs  : node — subtree root (may be nullptr).
       Output  : number of levels under `node`. */
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
 * BENCHMARK — both solutions on 4 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: balanced example → true.
    TreeNode* t1 = buildTree({3, 9, 20, std::nullopt, std::nullopt, 15, 7});
    // Test 2: unbalanced (20's right leg 7→4 hangs 2 deeper) → false.
    TreeNode* t2 = buildTree({1, 2, 2, 3, 3, std::nullopt, std::nullopt, 4, 4});
    // Test 3: empty tree → true.
    TreeNode* t3 = nullptr;
    // Test 4: left chain 1→2→3 — height difference 2 at the root → false.
    TreeNode* t4 = buildTree({1, 2, std::nullopt, 3});
    const bool expected[4] = {true, false, true, false};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool r1[4] = {Solution_1().isBalanced(t1), Solution_1().isBalanced(t2),
                  Solution_1().isBalanced(t3), Solution_1().isBalanced(t4)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    bool r2[4] = {Solution_2().isBalanced(t1), Solution_2().isBalanced(t2),
                  Solution_2().isBalanced(t3), Solution_2().isBalanced(t4)};
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
        std::cout << "Test " << (i + 1) << ": S1=" << (r1[i] ? "true" : "false")
                  << " S2=" << (r2[i] ? "true" : "false")
                  << " (expected " << (expected[i] ? "true" : "false") << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (post-order, O(n))   : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (top-down, O(n²))    : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all verdicts match expected."
                         : "FAIL : at least one verdict is wrong.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t4);
    return 0;
}