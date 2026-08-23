/*
 * =====================================================================
 * LeetCode 226 : Invert Binary Tree                                   (Easy)
 * https://leetcode.com/problems/invert-binary-tree/
 * Category   : Trees — pointer surgery
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given the root of a binary tree, INVERT it in place — mirror it
 *   horizontally: every node's left and right children swap. Return
 *   the root of the inverted tree.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Inversion is a per-node operation: swap the two child pointers,
 *   then invert both subtrees. Order does not matter — swap-then-
 *   recurse and recurse-then-swap produce the same mirror because the
 *   swap is independent at every node. That freedom lets us write it
 *   either recursively (implicit call stack) or with an explicit
 *   work list.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Recursive swap (BEST, 3 lines of essence)
 *   swap(node->left, node->right); invert(left); invert(right).
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Iterative BFS/DFS with an explicit queue
 *   Same swaps, but a std::queue (or stack) holds the nodes still
 *   awaiting their swap — no recursion, safe on pathologically deep
 *   trees where the runtime stack would overflow.
 *   Time  Complexity : O(n)  — every node dequeued exactly once.
 *   Space Complexity : O(w)  — queue width (≤ n).
 * ---------------------------------------------------------------------
 * DEEP DIVE — pointer swaps ARE the mutation
 *   The tree is a set of heap nodes linked by pointers. "Inverting"
 *   changes NO node values and allocates NOTHING — it rewrites two
 *   pointers per node in place. That is why the operation is O(n)
 *   time and O(1) extra space per node; the recursion/queue memory is
 *   the only overhead. Watch the animation: the addresses stay fixed,
 *   the arrows flip.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — level-order test inputs
#include <queue>          // std::queue — FIFO work list (approach 2)
#include <utility>        // std::swap — flipping child pointers
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursive swap
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Mirror the tree in place and return its root.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : root of the inverted (same) tree.
     */
    TreeNode* invertTree(TreeNode* root) {
        // Empty subtree has nothing to mirror.
        if (root == nullptr) {
            return nullptr;
        }
        // Swap this node's children — the ONLY mutation the problem needs.
        std::swap(root->left, root->right);
        // Mirror both halves; order is irrelevant (independent swaps).
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};

/* =====================================================================
 * APPROACH 2 : Iterative — explicit FIFO of pending nodes
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Mirror the tree in place and return its root.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : root of the inverted (same) tree.
     */
    TreeNode* invertTree(TreeNode* root) {
        if (root == nullptr) {
            return nullptr;
        }
        // Queue plays the role the call stack had in approach 1: it
        // remembers which subtrees still need their swap.
        std::queue<TreeNode*> pending;
        pending.push(root);

        while (!pending.empty()) {
            TreeNode* cur = pending.front();
            pending.pop();

            // Same pointer flip as before — explicit, visible, in place.
            std::swap(cur->left, cur->right);

            // Children now point at swapped subtrees; schedule both.
            if (cur->left != nullptr) {
                pending.push(cur->left);
            }
            if (cur->right != nullptr) {
                pending.push(cur->right);
            }
        }
        return root;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Each solution gets its OWN copy of every test tree — inversion
    // mutates in place, so sharing one tree between the two runs would
    // let the second solution see the first one's output.
    // Test 1: official example → inverted [4,7,2,9,6,3,1].
    TreeNode* t1a = buildTree({4, 2, 7, 1, 3, 6, 9});
    TreeNode* t1b = buildTree({4, 2, 7, 1, 3, 6, 9});
    // Test 2: single node → unchanged [1].
    TreeNode* t2a = buildTree({1});
    TreeNode* t2b = buildTree({1});
    // Test 3: right chain 1→2→3 → becomes a LEFT chain [1,2,null,3].
    TreeNode* t3a = buildTree({1, std::nullopt, 2, std::nullopt, 3});
    TreeNode* t3b = buildTree({1, std::nullopt, 2, std::nullopt, 3});

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    TreeNode* r1a = Solution_1().invertTree(t1a);
    TreeNode* r1b = Solution_1().invertTree(t2a);
    TreeNode* r1c = Solution_1().invertTree(t3a);
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    TreeNode* r2a = Solution_2().invertTree(t1b);
    TreeNode* r2b = Solution_2().invertTree(t2b);
    TreeNode* r2c = Solution_2().invertTree(t3b);
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB on Linux
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    // Show the inverted shapes for eyeball verification.
    std::cout << "Test 1 inverted: S1=";
    printTree(r1a);
    std::cout << " S2=";
    printTree(r2a);
    std::cout << "\nTest 2 inverted: S1=";
    printTree(r1b);
    std::cout << " S2=";
    printTree(r2b);
    std::cout << "\nTest 3 inverted: S1=";
    printTree(r1c);
    std::cout << " S2=";
    printTree(r2c);
    std::cout << "\n";

    // Cross-check both solutions against the expected inverted shapes.
    bool all_ok = true;
    TreeNode* e1 = buildTree({4, 7, 2, 9, 6, 3, 1});
    TreeNode* e2 = buildTree({1});
    TreeNode* e3 = buildTree({1, 2, std::nullopt, 3});
    auto eq = [](auto&& self, TreeNode* x, TreeNode* y) -> bool {
        if (x == nullptr || y == nullptr) { return x == y; }
        return x->val == y->val && self(self, x->left, y->left) && self(self, x->right, y->right);
    };
    all_ok = eq(eq, r1a, e1) && eq(eq, r2a, e1) &&
             eq(eq, r1b, e2) && eq(eq, r2b, e2) &&
             eq(eq, r1c, e3) && eq(eq, r2c, e3);

    std::cout << "Solution_1 (recursive)         : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (iterative queue)   : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : inverted trees match expected."
                         : "FAIL : inversion produced a wrong tree.")
              << "\n";

    destroyTree(t1a); destroyTree(t1b);
    destroyTree(t2a); destroyTree(t2b);
    destroyTree(t3a); destroyTree(t3b);
    destroyTree(e1); destroyTree(e2); destroyTree(e3);
    return 0;
}