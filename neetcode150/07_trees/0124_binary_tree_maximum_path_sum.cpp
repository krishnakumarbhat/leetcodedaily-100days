/*
 * =====================================================================
 * LeetCode 124 : Binary Tree Maximum Path Sum                       (Hard)
 * https://leetcode.com/problems/binary-tree-maximum-path-sum/
 * Category   : Trees — post-order info passing
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A PATH is any sequence of nodes connected by tree edges (can start
 *   and end ANYWHERE, may not visit a node twice). Return the LARGEST
 *   sum a path can collect. Node values may be negative.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Every path has a HIGHEST node (the one closest to the root).
 *   Decompose: at each node, the best path passing THROUGH it is
 *   bestDown(left) + node.val + bestDown(right), where bestDown is
 *   the best sum of a path that starts at a node and goes DOWN into
 *   one subtree. Only two facts must travel upward: the best down-sum
 *   through each child (to extend the parent's path) and the global
 *   best-so-far. Post-order = the child answers arrive before the
 *   parent composes them.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Post-order with best-so-far (BEST)
 *   dfs(node) returns the best single-branch down-sum through node;
 *   the caller updates a shared `best` with the full path through it.
 *   Negative branches are dropped (max(0, child)) — a path may simply
 *   not extend into a subtree that would shrink it.
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Brute force, path-through-every-node (contrast)
 *   For every node compute the max down-sum through each child with a
 *   separate helper, then combine. Same idea, but each child's down-
 *   sum is recomputed for every ancestor.
 *   Time  Complexity : O(n²)  worst — recomputation per ancestor.
 *   Space Complexity : O(h)   — call stacks.
 *   WHY SHOW IT: identical math, wildly different cost — the whole
 *   point of carrying info up instead of re-deriving it.
 * ---------------------------------------------------------------------
 * DEEP DIVE — "return a summary, keep a global" (the tree-DP shape)
 *   dfs returning ONE value while a shared accumulator tracks the
 *   answer is the canonical Hard-tree pattern: the return value is
 *   the "legal to extend" summary (one branch only), the global is
 *   the "any shape" answer (both branches, no parent). Confusing the
 *   two is THE classic bug on this problem — a path can bend through
 *   the node (left + right) but can only EXTEND upward along one
 *   branch. Clamping child contributions at 0 is safe because an
 *   empty path is always allowed.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <algorithm>      // std::max — clamping child contributions
#include <climits>        // INT_MIN — the "−∞" starter for best-so-far
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Post-order, one down-sum per node, global best
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the maximum sum of any root-to-anywhere path.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : largest path sum; 0 for an empty tree.
     */
    int maxPathSum(TreeNode* root) {
        best = INT_MIN;                 // -∞: every node re-arms the max
        downSum(root);
        return best;
    }

private:
    int best;                           // global answer across ALL nodes

    /* Purpose : Best single-branch path sum starting at `node`.
       Inputs  : node — current subtree root (may be nullptr).
       Output  : max over {node.val, node.val + bestDown(left),
                 node.val + bestDown(right)}; also folds the full
                 left+node+right path into the global `best`. */
    int downSum(TreeNode* node) {
        // No node → contributes nothing to any path through its parent.
        if (node == nullptr) {
            return 0;
        }
        // Children FIRST (post-order): their down-sums are ready here.
        // max(..., 0): a negative branch is better NOT extended into.
        int left = std::max(0, downSum(node->left));
        int right = std::max(0, downSum(node->right));

        // A path can BEND through this node: left leg + node + right leg.
        // That shape can never extend upward, so it only feeds `best`.
        best = std::max(best, left + node->val + right);

        // What we hand the PARENT: the better single leg through us.
        // One branch only — the parent's path must stay a simple chain.
        return node->val + std::max(left, right);
    }
};

/* =====================================================================
 * APPROACH 2 : Brute force — re-derive each child's down-sum
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the maximum sum of any path in the tree.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : largest path sum; 0 for an empty tree.
     */
    int maxPathSum(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        best = INT_MIN;
        consider(root);                 // every node as the path's peak
        return best;
    }

private:
    int best;

    /* Purpose : Evaluate the best path whose highest node is `node`.
       Inputs  : node — the candidate apex of the path.
       Output  : nothing; updates `best` with left + val + right. */
    void consider(TreeNode* node) {
        if (node == nullptr) {
            return;
        }
        // Recomputes BOTH legs from scratch — the O(n) waste per node.
        int left = std::max(0, downSum(node->left));
        int right = std::max(0, downSum(node->right));
        best = std::max(best, left + node->val + right);
        consider(node->left);           // every node gets its turn
        consider(node->right);
    }

    /* Purpose : Best downward-branch sum starting at `node`.
       Inputs  : node — subtree root (may be nullptr).
       Output  : node.val + the better of the two child branches. */
    int downSum(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        int left = std::max(0, downSum(node->left));
        int right = std::max(0, downSum(node->right));
        return node->val + std::max(left, right);
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example → best path 4→2→1→3 = 6.
    TreeNode* t1 = buildTree({1, 2, 3});
    // Test 2: negative root, best path 15→20→7 = 42.
    TreeNode* t2 = buildTree({-10, 9, 20, std::nullopt, std::nullopt, 15, 7});
    // Test 3: all-negative chain → the largest single node (-1).
    TreeNode* t3 = buildTree({-3, -1, std::nullopt, -2});
    const int expected[3] = {6, 42, -1};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    int r1[3] = {Solution_1().maxPathSum(t1), Solution_1().maxPathSum(t2),
                 Solution_1().maxPathSum(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    int r2[3] = {Solution_2().maxPathSum(t1), Solution_2().maxPathSum(t2),
                 Solution_2().maxPathSum(t3)};
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
    std::cout << "Solution_2 (brute force, O(n²)) : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all path sums match expected."
                         : "FAIL : at least one path sum is wrong.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t3);
    return 0;
}