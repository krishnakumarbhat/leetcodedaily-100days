/*
 * =====================================================================
 * LeetCode 235 : Lowest Common Ancestor of a Binary Search Tree      (Medium)
 * https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
 * Category   : Trees — BST descent
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given a BST root and two nodes p, q inside it, return their
 *   LOWEST COMMON ANCESTOR — the deepest node that has both p and q
 *   as descendants (a node counts as its own descendant).
 * ---------------------------------------------------------------------
 * INTUITION
 *   The BST's ORDERING makes the answer a one-way street: at any node
 *   `cur`, p and q lie either both LEFT (both smaller → keep going
 *   left), both RIGHT (both larger → keep going right), or they
 *   SPLIT (one smaller, one larger — or one IS cur). The moment they
 *   split, `cur` is the first node able to contain both → THE LCA.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Iterative descent (BEST)
 *   Walk from the root; branch left/right while both targets are on
 *   the same side; the first split (or equality) node is the answer.
 *   Time  Complexity : O(h)  — at most one root→leaf walk, h = height.
 *   Space Complexity : O(1)  — two pointers, no containers at all.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Recursive descent
 *   Same branching rules, expressed as recursion: the base case is
 *   exactly the "split" condition; otherwise recurse into the side
 *   both nodes share.
 *   Time  Complexity : O(h)  — same descent path.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why the BST beats the generic-tree algorithm
 *   For a general binary tree, LCA needs a parent-pointer/ancestor-set
 *   or a post-order search (O(n)). Here the ORDERING prunes one side
 *   of the tree at every step — the search space halves per level,
 *   giving O(h) instead of O(n). The splitting test (p < cur < q or
 *   q < cur < p) is the entire algorithm in one condition; the LCA is
 *   the node where that test first succeeds on the descent.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Iterative descent — O(h) time, O(1) space
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the lowest common ancestor of p and q.
     * Inputs  : root — BST root; p, q — nodes guaranteed to exist.
     * Output  : pointer to the LCA node.
     */
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        TreeNode* cur = root;
        // Descend until the targets split sides — or one IS the node.
        while (cur != nullptr) {
            // Both targets smaller → LCA must live in the left subtree.
            if (p->val < cur->val && q->val < cur->val) {
                cur = cur->left;
            }
            // Both targets larger → LCA must live in the right subtree.
            else if (p->val > cur->val && q->val > cur->val) {
                cur = cur->right;
            }
            // They split (or one equals cur): cur is the FIRST node
            // that can have both as descendants → the LCA.
            else {
                return cur;
            }
        }
        return nullptr;                // unreachable per problem statement
    }
};

/* =====================================================================
 * APPROACH 2 : Recursive descent — same rule, implicit call stack
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the lowest common ancestor of p and q.
     * Inputs  : root — BST root; p, q — nodes guaranteed to exist.
     * Output  : pointer to the LCA node.
     */
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        // Empty subtree cannot contain the targets.
        if (root == nullptr) {
            return nullptr;
        }
        // Both targets below → LCA is somewhere in the left subtree.
        if (p->val < root->val && q->val < root->val) {
            return lowestCommonAncestor(root->left, p, q);
        }
        // Both targets above → LCA is somewhere in the right subtree.
        if (p->val > root->val && q->val > root->val) {
            return lowestCommonAncestor(root->right, p, q);
        }
        // Split/equality case — root itself is the lowest common ancestor.
        return root;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — [6,2,8,0,4,7,9,null,null,3,5],
    //         p=2 (left subtree), q=8 (right subtree) → LCA = 6.
    TreeNode* t1 = buildTree({6, 2, 8, 0, 4, 7, 9, std::nullopt, std::nullopt, 3, 5});
    TreeNode* p1 = t1->left;                 // node 2
    TreeNode* q1 = t1->right;                // node 8
    // Test 2: p=2, q=4 → both in the left subtree, 4 is 2's child → 2.
    TreeNode* p2 = t1->left;
    TreeNode* q2 = t1->left->right;          // node 4
    // Test 3: p=4, q=5 → both under node 2; 4 is 5's parent → LCA = 4.
    TreeNode* p3 = t1->left->right;          // node 4
    TreeNode* q3 = t1->left->right->right;   // node 5
    const int expected[3] = {6, 2, 4};
    TreeNode* ps[3] = {p1, p2, p3};
    TreeNode* qs[3] = {q1, q2, q3};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    int r1[3];
    for (int i = 0; i < 3; ++i) { r1[i] = Solution_1().lowestCommonAncestor(t1, ps[i], qs[i])->val; }
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    int r2[3];
    for (int i = 0; i < 3; ++i) { r2[i] = Solution_2().lowestCommonAncestor(t1, ps[i], qs[i])->val; }
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
        std::cout << "Test " << (i + 1) << " (p=" << ps[i]->val << ",q=" << qs[i]->val
                  << "): S1=" << r1[i] << " S2=" << r2[i]
                  << " (expected " << expected[i] << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (iterative descent): time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (recursive descent): time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all LCAs match expected."
                         : "FAIL : at least one LCA is wrong.")
              << "\n";

    destroyTree(t1);
    return 0;
}