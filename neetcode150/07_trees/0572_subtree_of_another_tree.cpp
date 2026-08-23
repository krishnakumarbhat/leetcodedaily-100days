/*
 * =====================================================================
 * LeetCode 572 : Subtree of Another Tree                             (Easy)
 * https://leetcode.com/problems/subtree-of-another-tree/
 * Category   : Trees — nested equality
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two binary trees root and subRoot, decide whether subRoot
 *   is a SUBTREE of root: some node of root, together with ALL its
 *   descendants, is EXACTLY equal to subRoot (structure + values).
 * ---------------------------------------------------------------------
 * INTUITION
 *   A subtree lives at exactly one node of root. So the answer is:
 *   "does root match subRoot, or does root.left match it, or does
 *   root.right match it?" — a recursion over candidate anchor nodes,
 *   each checked with the Same-Tree comparison.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive anchor search + equality walk (BEST)
 *   isSubtree(root, sub) = sameTree(root, sub) || isSubtree(root->left,
 *   sub) || isSubtree(root->right, sub). Each candidate is compared
 *   wholesale — no partial matches allowed below the anchor.
 *   Time  Complexity : O(n·m)  worst — each of n anchors may walk m
 *                        nodes when shapes tease the walk apart.
 *   Space Complexity : O(h + hm) — the two call stacks interleaved.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Serialize both, then string search
 *   Flatten root and subRoot into preorder-with-null-marker strings
 *   (see problem 297 — the markers disambiguate shape!) and check
 *   `sub` occurs inside `root`. The SAME canonical string appears iff
 *   the subtree is truly equal.
 *   Time  Complexity : O(n + m)  — two walks + one substring search
 *                        (linear with an efficient find).
 *   Space Complexity : O(n + m)  — the two serialized strings.
 *   WHY SERIALIZATION WORKS: with null markers, identical trees
 *   produce identical strings and vice versa — structure is encoded
 *   in the text, so string equality == tree equality.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why markers matter here too
 *   Serializing WITHOUT null markers is ambiguous ([1,2] could be
 *   several shapes) — a naive find would give false positives. The
 *   marker discipline from 0297 makes the encoding injective, which
 *   is precisely what turns a tree problem into a string problem.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <string>         // std::string — serialized canonical forms
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive anchor search with full equality checks
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether `subRoot` matches some node's whole
     *           subtree inside `root`.
     * Inputs  : root — candidate host tree; subRoot — tree to find.
     * Output  : true iff an exact whole-subtree match exists.
     */
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        // No host left to anchor at → impossible.
        if (root == nullptr) {
            return false;
        }
        // THIS node matches the whole subtree → done.
        if (sameTree(root, subRoot)) {
            return true;
        }
        // Otherwise hunt for an anchor inside either child subtree.
        return isSubtree(root->left, subRoot) ||
               isSubtree(root->right, subRoot);
    }

private:
    /* Purpose : Full structural equality of two trees.
       Inputs  : a, b — the two roots to compare.
       Output  : true iff identical values at identical positions. */
    bool sameTree(TreeNode* a, TreeNode* b) {
        // Both empty → match; exactly one empty → mismatch.
        if (a == nullptr || b == nullptr) {
            return a == b;
        }
        // Values must agree AND both child pairs must fully match.
        return a->val == b->val &&
               sameTree(a->left, b->left) &&
               sameTree(a->right, b->right);
    }
};

/* =====================================================================
 * APPROACH 2 : Canonical serialization + substring search
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether `subRoot` is a subtree of `root`.
     * Inputs  : root — candidate host tree; subRoot — tree to find.
     * Output  : true iff an exact whole-subtree match exists.
     */
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        // Canonical strings: preorder with explicit null markers.
        // With markers the encoding is INJECTIVE — string equality
        // exactly mirrors tree equality (no false positives).
        std::string host = encode(root);
        std::string sub = encode(subRoot);
        // Substring search: O(n + m) with std::string's find.
        return host.find(sub) != std::string::npos;
    }

private:
    /* Purpose : Preorder flattening with "null" markers.
       Inputs  : node — current subtree root (may be nullptr).
       Output  : canonical string, e.g. "3,9,X,X,20,15,X,X,7,X,X". */
    std::string encode(TreeNode* node) {
        // Empty child → explicit marker (the shape-preserving token).
        if (node == nullptr) {
            return "X,";
        }
        // node → left → right with delimiters so "1,2" ≠ "12".
        return std::to_string(node->val) + "," +
               encode(node->left) + encode(node->right);
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — [3,4,5,1,2] contains [4,1,2] → true.
    TreeNode* r1 = buildTree({3, 4, 5, 1, 2});
    TreeNode* s1 = buildTree({4, 1, 2});
    // Test 2: same trees, extra leaf 0 under 2 → NOT a subtree → false.
    TreeNode* r2 = buildTree({3, 4, 5, 1, 2, std::nullopt, std::nullopt, std::nullopt, 0});
    TreeNode* s2 = buildTree({4, 1, 2});
    // Test 3: subRoot equal to the whole root → true.
    TreeNode* r3 = buildTree({1, 2, 3});
    TreeNode* s3 = buildTree({1, 2, 3});
    const bool expected[3] = {true, false, true};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool r1v[3] = {Solution_1().isSubtree(r1, s1),
                   Solution_1().isSubtree(r2, s2),
                   Solution_1().isSubtree(r3, s3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    bool r2v[3] = {Solution_2().isSubtree(r1, s1),
                   Solution_2().isSubtree(r2, s2),
                   Solution_2().isSubtree(r3, s3)};
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB on Linux
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    bool all_ok = true;
    for (int i = 0; i < 3; ++i) {
        bool ok = (r1v[i] == expected[i]) && (r2v[i] == expected[i]);
        all_ok = all_ok && ok;
        std::cout << "Test " << (i + 1) << ": S1=" << (r1v[i] ? "true" : "false")
                  << " S2=" << (r2v[i] ? "true" : "false")
                  << " (expected " << (expected[i] ? "true" : "false") << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (recursive anchors) : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (serialize + find)  : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all subtree verdicts match expected."
                         : "FAIL : at least one verdict is wrong.")
              << "\n";

    destroyTree(r1); destroyTree(s1);
    destroyTree(r2); destroyTree(s2);
    destroyTree(r3); destroyTree(s3);
    return 0;
}