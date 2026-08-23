/*
 * =====================================================================
 * LeetCode 144 : Binary Tree Preorder Traversal                      (Easy)
 * https://leetcode.com/problems/binary-tree-preorder-traversal/
 * Category   : Trees — DFS
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, return the PREORDER traversal:
 *   visit the node, then its left subtree, then its right subtree
 *   (root → left → right).
 * ---------------------------------------------------------------------
 * INTUITION
 *   Preorder is THE traversal that matches how recursion naturally
 *   descends: "act on the node first, then let each subtree act on
 *   itself". The order is entirely defined by WHEN you emit the node
 *   relative to the two recursive calls.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive (BEST, the definition itself)
 *   emit(node); preorder(left); preorder(right).
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative with an explicit stack
 *   Because PREORDER needs "root, then LEFT first", a LIFO stack is
 *   pushed RIGHT-first: the right child is stored away and the left
 *   child pops out next. The stack IS the call stack, made visible.
 *   Time  Complexity : O(n)  — every node pushed/popped exactly once.
 *   Space Complexity : O(h)  — stack holds at most one level's worth
 *                        of pending right subtrees.
 * ---------------------------------------------------------------------
 * DEEP DIVE — recursion vs the explicit stack
 *   Recursion hides a stack frame per open call; the iterative
 *   version allocates the same frames on the heap as std::stack.
 *   The push-right-then-pop-left trick is the whole insight: LIFO
 *   reverses insertion order, so inserting right first makes left
 *   come out first — reproducing preorder exactly. The same pattern
 *   with a FIFO queue produces level order instead (different
 *   container, different traversal).
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — output + level-order tests
#include <stack>          // std::stack — LIFO work list (approach 2)
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive preorder
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the preorder (root, left, right) value list.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : vector<int> in preorder order.
     */
    std::vector<int> preorderTraversal(TreeNode* root) {
        std::vector<int> out;
        walk(root, out);
        return out;
    }

private:
    /* Purpose : Preorder visit of one subtree.
       Inputs  : node — current node; out — list being built.
       Output  : nothing (appends node values in preorder). */
    void walk(TreeNode* node, std::vector<int>& out) {
        // Empty subtree emits nothing.
        if (node == nullptr) {
            return;
        }
        out.push_back(node->val);     // 1. the node itself
        walk(node->left, out);        // 2. the whole left subtree
        walk(node->right, out);       // 3. the whole right subtree
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative — explicit stack, right pushed first
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the preorder (root, left, right) value list.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : vector<int> in preorder order.
     */
    std::vector<int> preorderTraversal(TreeNode* root) {
        std::vector<int> out;
        if (root == nullptr) {
            return out;
        }
        std::stack<TreeNode*> pending;   // explicit call-stack stand-in
        pending.push(root);

        while (!pending.empty()) {
            TreeNode* cur = pending.top();
            pending.pop();
            out.push_back(cur->val);     // emit the node when popped
            // RIGHT is pushed FIRST so the LEFT child pops first —
            // LIFO reverses order → preorder (root, left, right).
            if (cur->right != nullptr) {
                pending.push(cur->right);
            }
            if (cur->left != nullptr) {
                pending.push(cur->left);
            }
        }
        return out;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — [1,null,2,3] → [1,2,3].
    TreeNode* t1 = buildTree({1, std::nullopt, 2, 3});
    // Test 2: empty tree → [].
    TreeNode* t2 = nullptr;
    // Test 3: full-ish tree → [1,2,4,5,3,6].
    TreeNode* t3 = buildTree({1, 2, 3, 4, 5, 6});
    const std::vector<int> expected[3] = {{1, 2, 3}, {}, {1, 2, 4, 5, 3, 6}};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    std::vector<int> r1[3] = {Solution_1().preorderTraversal(t1),
                              Solution_1().preorderTraversal(t2),
                              Solution_1().preorderTraversal(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    std::vector<int> r2[3] = {Solution_2().preorderTraversal(t1),
                              Solution_2().preorderTraversal(t2),
                              Solution_2().preorderTraversal(t3)};
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
        std::cout << "Test " << (i + 1) << ": S1=[";
        for (size_t j = 0; j < r1[i].size(); ++j) { std::cout << r1[i][j] << (j + 1 < r1[i].size() ? "," : ""); }
        std::cout << "] S2=[";
        for (size_t j = 0; j < r2[i].size(); ++j) { std::cout << r2[i][j] << (j + 1 < r2[i].size() ? "," : ""); }
        std::cout << "]" << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (recursive)          : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (iterative stack)    : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : both preorders match expected."
                         : "FAIL : at least one preorder differs.")
              << "\n";

    destroyTree(t1); destroyTree(t3);
    return 0;
}