/*
 * =====================================================================
 * LeetCode 1448 : Count Good Nodes in Binary Tree                    (Medium)
 * https://leetcode.com/problems/count-good-nodes-in-binary-tree/
 * Category   : Trees — path-state DFS
 * ---------------------------------------------------------------------
 * PROBLEM
 *   A node X is GOOD when, on the path from the ROOT to X, X's value
 *   is >= every value seen so far (X itself included). Count all good
 *   nodes in the tree.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Goodness is a PATH property, not a subtree property: it depends
 *   on the maximum value inherited from the root. DFS is the natural
 *   fit — carry "largest value on the path so far" down, compare at
 *   each node, and update the carried max for the children.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive DFS with max-so-far (BEST)
 *   dfs(node, maxSoFar): node is good iff val >= maxSoFar; children
 *   receive max(maxSoFar, val). Sum the good verdicts bottom-up.
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative DFS with an explicit stack
 *   Stack holds (node, maxSoFar) pairs — the path state travels in
 *   the stack frame instead of the recursion frame.
 *   Time  Complexity : O(n)  — every pair pushed/popped once.
 *   Space Complexity : O(h)  — stack depth, h = tree height.
 * ---------------------------------------------------------------------
 * DEEP DIVE — path state as the recursion's "luggage"
 *   Some tree questions need context from the ROOT (this max), others
 *   need summaries from the LEAVES (diameter). This problem is a
 *   "top-down luggage" problem: the extra argument is what makes each
 *   subtree question well-posed, and it travels DOWN only. Contrast
 *   with 0543/0124 where the info travels UP — recognizing which
 *   direction the state flows is half of solving tree problems.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <stack>          // std::stack — explicit DFS stack (approach 2)
#include <utility>        // std::pair — (node, maxSoFar) frames
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive DFS carrying the path maximum
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Count nodes whose value is >= every ancestor's value.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : number of good nodes.
     */
    int goodNodes(TreeNode* root) {
        // Root has no ancestors — its own value is the starting max.
        return dfs(root, root->val);
    }

private:
    /* Purpose : Count good nodes inside a subtree, given path max.
       Inputs  : node — current node; max_so_far — largest value on
                 the root→node path (excluding node itself... see below).
       Output  : good-count of the subtree. */
    int dfs(TreeNode* node, int max_so_far) {
        // Empty subtree holds no nodes to count.
        if (node == nullptr) {
            return 0;
        }
        // The current node is good iff nothing above it is larger.
        int count = (node->val >= max_so_far) ? 1 : 0;
        // Children inherit an UPDATED path maximum (include this node).
        int new_max = (node->val > max_so_far) ? node->val : max_so_far;
        return count + dfs(node->left, new_max) + dfs(node->right, new_max);
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative DFS — (node, maxSoFar) stack frames
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Count nodes whose value is >= every ancestor's value.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : number of good nodes.
     */
    int goodNodes(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        // Each frame = one open recursive call: the node AND the path
        // maximum that was in force when we reached it.
        std::stack<std::pair<TreeNode*, int>> pending;
        pending.push({root, root->val});
        int count = 0;

        while (!pending.empty()) {
            auto [node, max_so_far] = pending.top();
            pending.pop();

            // Same good-test as the recursive version.
            if (node->val >= max_so_far) {
                ++count;
            }
            int new_max = (node->val > max_so_far) ? node->val : max_so_far;
            // Children inherit the updated max — order doesn't matter.
            if (node->left != nullptr) {
                pending.push({node->left, new_max});
            }
            if (node->right != nullptr) {
                pending.push({node->right, new_max});
            }
        }
        return count;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — [3,1,4,3,null,1,5] → good = 4 (3,3,4,5).
    TreeNode* t1 = buildTree({3, 1, 4, 3, std::nullopt, 1, 5});
    // Test 2: [3,3,null,4,2] → good = 3 (3,3,4).
    TreeNode* t2 = buildTree({3, 3, std::nullopt, 4, 2});
    // Test 3: single node → 1.
    TreeNode* t3 = buildTree({1});
    const int expected[3] = {4, 3, 1};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    int r1[3] = {Solution_1().goodNodes(t1), Solution_1().goodNodes(t2),
                 Solution_1().goodNodes(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    int r2[3] = {Solution_2().goodNodes(t1), Solution_2().goodNodes(t2),
                 Solution_2().goodNodes(t3)};
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

    std::cout << "Solution_1 (recursive DFS)     : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (iterative stack)   : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all good-node counts match expected."
                         : "FAIL : at least one count is wrong.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t3);
    return 0;
}