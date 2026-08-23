/*
 * =====================================================================
 * LeetCode 98 : Validate Binary Search Tree                        (Medium)
 * https://leetcode.com/problems/validate-binary-search-tree/
 * Category   : Trees — BST property
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, decide whether it is a VALID
 *   binary search tree (BST). For EVERY node:
 *     • its left subtree holds only values STRICTLY LESS than it,
 *     • its right subtree holds only values STRICTLY GREATER than it,
 *     • both subtrees are themselves valid BSTs. No duplicates.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Checking only direct children is WRONG: [5,4,6,null,null,3,7]
 *   passes that test, yet 3 sits in 5's RIGHT subtree with 3 < 5.
 *   The correct rule: every node carries an allowed interval (lo, hi)
 *   inherited from its ancestors — going LEFT replaces hi by the
 *   parent's value, going RIGHT replaces lo. A node is valid iff its
 *   value lies strictly inside its inherited interval.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive interval propagation (BEST)
 *   DFS down the tree carrying (lo, hi); each node must satisfy
 *   lo < val < hi. long long gives us ±∞ without overflow.
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — recursion call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative inorder (must be strictly ascending)
 *   A BST's inorder walk emits values in STRICTLY increasing order —
 *   and only a BST does. Walk iteratively with an explicit stack;
 *   if the current value is <= the previous one → not a BST.
 *   Time  Complexity : O(n)  — each node pushed/popped exactly once.
 *   Space Complexity : O(h)  — explicit stack, h = tree height.
 * ---------------------------------------------------------------------
 * DEEP DIVE — recursion = the implicit call stack
 *   Every function call pushes a FRAME (locals + return address) onto
 *   the call stack; the frame pops when the callee returns. Recursive
 *   tree code therefore costs O(h) extra memory — one frame per
 *   ancestor still on the current path. Approach 1 lets the runtime
 *   maintain that stack invisibly; Approach 2 builds the SAME stack by
 *   hand with std::stack. Identical memory behaviour — recursion just
 *   hides the bookkeeping, which is why tree code prefers it.
 * =====================================================================
 */

#include <iostream>      // std::cout — printing benchmark results
#include <vector>        // std::vector — level-order test inputs
#include <stack>         // std::stack — explicit inorder stack (approach 2)
#include <climits>       // LLONG_MIN / LLONG_MAX — ±∞ bounds for approach 1
#include <chrono>        // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h>// getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"   // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive interval propagation
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether `root` is a valid BST.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : true when every node lies strictly inside the interval
     *           inherited from its ancestors.
     */
    bool isValidBST(TreeNode* root) {
        // Root has no constraints: ±∞ both ways (long long, no overflow).
        return validate(root, LLONG_MIN, LLONG_MAX);
    }

private:
    /* Purpose : Check the subtree `node` against inherited interval.
       Inputs  : node — current node; lo/hi — strict allowed bounds.
       Output  : true if node and both subtrees respect (lo, hi). */
    bool validate(TreeNode* node, long long lo, long long hi) {
        // Empty subtree cannot violate anything — base case of the walk.
        if (node == nullptr) {
            return true;
        }
        // The node's own value must be strictly inside its interval.
        if (node->val <= lo || node->val >= hi) {
            return false;
        }
        // LEFT subtree is bounded above by this value; right subtree is
        // bounded below by it. Both must pass for the whole tree to pass.
        return validate(node->left, lo, node->val) &&
               validate(node->right, node->val, hi);
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative inorder — values must be strictly ascending
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether `root` is a valid BST via inorder walk.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : true iff the inorder traversal is strictly increasing.
     */
    bool isValidBST(TreeNode* root) {
        // Explicit stack replaces the call stack: frames are nodes that
        // were visited but whose RIGHT subtree is still pending.
        std::stack<TreeNode*> pending;
        TreeNode* cur = root;
        TreeNode* prev = nullptr;   // last value emitted by the walk

        // Classic iterative inorder: descend left, visit, go right.
        while (cur != nullptr || !pending.empty()) {
            // Push the whole left spine; we will visit these later.
            while (cur != nullptr) {
                pending.push(cur);
                cur = cur->left;
            }
            // Pop the deepest unvisited node — that is the next value.
            cur = pending.top();
            pending.pop();

            // Inorder must be strictly ascending; equality = duplicate
            // = violation of the BST property.
            if (prev != nullptr && prev->val >= cur->val) {
                return false;
            }
            prev = cur;

            // After visiting a node, walk its right subtree (or climb
            // back up if none — the stack holds the ancestors).
            cur = cur->right;
        }
        return true;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM per solution
 * ===================================================================== */
int main() {
    // Test trees (level-order = LeetCode's "[a,b,c,null,...]" format).
    // t1: 2's right subtree contains 3 (which is < 5) → INVALID.
    TreeNode* t1 = buildTree({5, 1, 4, std::nullopt, std::nullopt, 3, 6});
    // t2: classic valid BST.
    TreeNode* t2 = buildTree({2, 1, 3});
    // t3: [5,4,6,null,null,3,7] — the famous trap: 3 < 5 but in right
    // subtree → INVALID (direct-child check would wrongly say valid).
    TreeNode* t3 = buildTree({5, 4, 6, std::nullopt, std::nullopt, 3, 7});
    // Expected verdicts per test (1 = valid, 0 = invalid).
    const int expected[3] = {0, 1, 0};

    // --- Run both solutions while timing them (steady clock) ---
    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool r1a = Solution_1().isValidBST(t1);
    bool r1b = Solution_1().isValidBST(t2);
    bool r1c = Solution_1().isValidBST(t3);
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    bool r2a = Solution_2().isValidBST(t1);
    bool r2b = Solution_2().isValidBST(t2);
    bool r2c = Solution_2().isValidBST(t3);
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    // ru_maxrss is in KB on Linux; the delta is what THIS run consumed.
    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    // Per-test verdicts from both solutions.
    bool r1[3] = {r1a, r1b, r1c};
    bool r2[3] = {r2a, r2b, r2c};
    bool all_ok = true;
    for (int i = 0; i < 3; ++i) {
        bool ok = (r1[i] == (expected[i] == 1)) && (r2[i] == (expected[i] == 1));
        all_ok = all_ok && ok;
        std::cout << "Test " << (i + 1) << ": S1=" << (r1[i] ? "true" : "false")
                  << " S2=" << (r2[i] ? "true" : "false")
                  << " (expected " << (expected[i] ? "true" : "false") << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (recursive intervals): time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (iterative inorder)  : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all verdicts match expected."
                         : "FAIL : at least one verdict is wrong.")
              << "\n";

    // Free every heap node — post-order destroy, zero leaks.
    destroyTree(t1);
    destroyTree(t2);
    destroyTree(t3);
    return 0;
}
