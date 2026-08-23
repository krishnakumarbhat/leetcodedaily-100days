/*
 * =====================================================================
 * LeetCode 100 : Same Tree                                            (Easy)
 * https://leetcode.com/problems/same-tree/
 * Category   : Trees — structural equality
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the roots of two binary trees p and q, decide whether they
 *   are the SAME tree: identical structure AND identical values at
 *   every position.
 * ---------------------------------------------------------------------
 * INTUITION
 *   "Same" decomposes recursively: the two roots must hold equal
 *   values AND their left subtrees must be the same AND their right
 *   subtrees must be the same. A null mismatch (one side empty, the
 *   other not) is the only structural failure — and it terminates the
 *   recursion without ever comparing values.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive equality (BEST, clearest)
 *   Three base cases (both null → true; one null → false; values
 *   differ → false), then recurse into both child pairs.
 *   Time  Complexity : O(min(n, m)) — stops at the first mismatch.
 *   Space Complexity : O(h)         — call stack depth, h = height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative BFS (queue of node pairs)
 *   Same logic, but the work is held in an explicit FIFO queue of
 *   (p, q) pairs instead of the call stack — a flat loop, immune to
 *   deep-recursion stack overflow on skewed trees.
 *   Time  Complexity : O(min(n, m)) — each pair dequeued once.
 *   Space Complexity : O(w)         — queue width at the widest level.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why BOTH approaches are "the same algorithm"
 *   Recursive DFS and iterative BFS explore in different ORDERS but
 *   compare exactly the same pairs of nodes. The choice is about the
 *   container: the call stack (A1) vs an explicit queue (A2). For an
 *   O(n) tree walk, either is fine; the queue version shines when the
 *   tree is so deep that recursion would blow the runtime stack.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <queue>          // std::queue — FIFO of node pairs (approach 2)
#include <utility>        // std::pair — (p, q) bundles in the queue
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive equality
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Decide whether two trees are structurally identical.
     * Inputs  : p, q — roots of the two trees (either may be nullptr).
     * Output  : true iff structure and every value match.
     */
    bool isSameTree(TreeNode* p, TreeNode* q) {
        // Both empty → nothing to compare → same.
        if (p == nullptr && q == nullptr) {
            return true;
        }
        // Exactly one empty → structure differs → not the same.
        if (p == nullptr || q == nullptr) {
            return false;
        }
        // Roots differ → not the same. Short-circuits the whole walk.
        if (p->val != q->val) {
            return false;
        }
        // Both halves must match — the recursive definition of "same".
        return isSameTree(p->left, q->left) &&
               isSameTree(p->right, q->right);
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative BFS — queue of (p, q) pairs
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Decide whether two trees are structurally identical.
     * Inputs  : p, q — roots of the two trees (either may be nullptr).
     * Output  : true iff structure and every value match.
     */
    bool isSameTree(TreeNode* p, TreeNode* q) {
        // FIFO of node pairs still waiting to be compared level by level.
        std::queue<std::pair<TreeNode*, TreeNode*>> pending;
        pending.push({p, q});

        // Drain the queue; a mismatch at any pair ends the walk early.
        while (!pending.empty()) {
            auto [a, b] = pending.front();
            pending.pop();

            // Both null → this pair matches, nothing more to enqueue.
            if (a == nullptr && b == nullptr) {
                continue;
            }
            // One null, or two different values → structural mismatch.
            if (a == nullptr || b == nullptr || a->val != b->val) {
                return false;
            }
            // Matching pair → compare their children in the same way.
            pending.push({a->left, b->left});
            pending.push({a->right, b->right});
        }
        return true;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 test pairs: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: identical trees → true.
    TreeNode* p1 = buildTree({1, 2, 3});
    TreeNode* q1 = buildTree({1, 2, 3});
    // Test 2: same root, different right child → false.
    TreeNode* p2 = buildTree({1, 2, 3});
    TreeNode* q2 = buildTree({1, 2, std::nullopt});
    // Test 3: mirrored structure, different values → false.
    TreeNode* p3 = buildTree({1, 2, 1});
    TreeNode* q3 = buildTree({1, 1, 2});
    const bool expected[3] = {true, false, false};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    bool r1[3] = {Solution_1().isSameTree(p1, q1),
                  Solution_1().isSameTree(p2, q2),
                  Solution_1().isSameTree(p3, q3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    bool r2[3] = {Solution_2().isSameTree(p1, q1),
                  Solution_2().isSameTree(p2, q2),
                  Solution_2().isSameTree(p3, q3)};
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
        std::cout << "Test " << (i + 1) << ": S1=" << (r1[i] ? "true" : "false")
                  << " S2=" << (r2[i] ? "true" : "false")
                  << " (expected " << (expected[i] ? "true" : "false") << ")"
                  << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (recursive)        : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (iterative BFS)    : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : all verdicts match expected."
                         : "FAIL : at least one verdict is wrong.")
              << "\n";

    destroyTree(p1); destroyTree(q1);
    destroyTree(p2); destroyTree(q2);
    destroyTree(p3); destroyTree(q3);
    return 0;
}
