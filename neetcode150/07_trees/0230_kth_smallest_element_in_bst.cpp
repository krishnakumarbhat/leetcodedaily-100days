/*
 * =====================================================================
 * LeetCode 230 : Kth Smallest Element in a BST                      (Medium)
 * https://leetcode.com/problems/kth-smallest-element-in-a-bst/
 * Category   : Trees — inorder traversal
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary SEARCH tree (unique values) and an
 *   integer k (1-based), return the k-th smallest value in the tree.
 * ---------------------------------------------------------------------
 * INTUITION
 *   The defining property of a BST: an INORDER walk (left, node,
 *   right) visits values in ASCENDING order. So "the k-th smallest"
 *   is exactly "the k-th value emitted by an inorder walk" — and we
 *   can STOP the walk the instant the k-th value appears instead of
 *   traversing the rest of the tree.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative inorder with early stop (BEST)
 *   Explicit stack descends the left spine, pops the smallest unseen
 *   value, counts it, then steps right. Stop at count == k.
 *   Time  Complexity : O(h + k) — h spine descent + k pops.
 *   Space Complexity : O(h)     — explicit stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive inorder with early stop
 *   Identical ordering, implicit call stack; the recursion returns a
 *   boolean "already found?" to unwind early.
 *   Time  Complexity : O(h + k) — same walk, same stop condition.
 *   Space Complexity : O(h)     — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why inorder ⇔ sorted for BSTs
 *   A BST stores every node's left subtree BELOW it and right subtree
 *   ABOVE it. Inorder emits left → node → right, so a value arrives
 *   only after everything smaller (left subtree) and before everything
 *   larger (right subtree) — induction over the whole tree gives a
 *   fully sorted sequence. Any "k-th" question about a BST is really
 *   an inorder question; the explicit-stack version is the classic
 *   interview answer because it makes the early stop visible.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <stack>          // std::stack — explicit inorder stack
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Iterative inorder with an explicit stack
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the k-th smallest value in a BST.
     * Inputs  : root — BST root; k — 1-based rank to find.
     * Output  : the value that would appear k-th in sorted order.
     */
    int kthSmallest(TreeNode* root, int k) {
        std::stack<TreeNode*> pending;   // explicit call-stack stand-in
        TreeNode* cur = root;
        int visited = 0;                 // values already emitted in order

        // Standard iterative inorder: left spine, visit, go right.
        while (cur != nullptr || !pending.empty()) {
            // Descend the left spine — smallest unseen values live there.
            while (cur != nullptr) {
                pending.push(cur);
                cur = cur->left;
            }
            // Pop the next value in ascending order.
            cur = pending.top();
            pending.pop();

            // Count it; the k-th one is the answer — stop RIGHT NOW,
            // the remaining (larger) values can stay unvisited.
            if (++visited == k) {
                return cur->val;
            }
            cur = cur->right;            // continue with the right subtree
        }
        return -1;                       // k > tree size (never per spec)
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive inorder with early-stop unwinding
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the k-th smallest value in a BST.
     * Inputs  : root — BST root; k — 1-based rank to find.
     * Output  : the value that would appear k-th in sorted order.
     */
    int kthSmallest(TreeNode* root, int k) {
        counter = 0;                     // reset per call (member state)
        return walk(root, k);
    }

private:
    int counter;                         // values emitted so far

    /* Purpose : Inorder recursion that stops as soon as k is reached.
       Inputs  : node — current subtree root; k — rank we seek.
       Output  : the k-th smallest value, or -1 if not below `node`. */
    int walk(TreeNode* node, int k) {
        if (node == nullptr) {
            return -1;                   // empty subtree holds nothing
        }
        // LEFT first — smaller values always precede the node itself.
        int from_left = walk(node->left, k);
        if (from_left != -1) {
            return from_left;            // answer found below → unwind
        }
        // Node itself is the next value in sorted order.
        if (++counter == k) {
            return node->val;            // found → stop recursion cold
        }
        // RIGHT last — larger values only.
        return walk(node->right, k);
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — [3,1,4,null,2], k=1 → 1.
    TreeNode* t1 = buildTree({3, 1, 4, std::nullopt, 2});
    // Test 2: k=3 on the same tree → 3.
    // Test 3: BST [8,5,11,2,6,null,12] — sorted: 2,5,6,8,11,12;
    //         k=5 → 11.
    TreeNode* t3 = buildTree({8, 5, 11, 2, 6, std::nullopt, 12});
    const int k[3] = {1, 3, 5};
    const int expected[3] = {1, 3, 11};
    TreeNode* trees[3] = {t1, t1, t3};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    int r1[3];
    for (int i = 0; i < 3; ++i) { r1[i] = Solution_1().kthSmallest(trees[i], k[i]); }
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    int r2[3];
    for (int i = 0; i < 3; ++i) { r2[i] = Solution_2().kthSmallest(trees[i], k[i]); }
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
        std::cout << "Test " << (i + 1) << " (k=" << k[i] << "): S1=" << r1[i]
                  << " S2=" << r2[i] << " (expected " << expected[i] << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (iterative inorder): time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (recursive inorder): time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : both find the k-th smallest value."
                         : "FAIL : at least one answer is wrong.")
              << "\n";

    destroyTree(t1); destroyTree(t3);
    return 0;
}