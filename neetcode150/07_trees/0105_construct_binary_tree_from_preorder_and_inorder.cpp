/*
 * =====================================================================
 * LeetCode 105 : Construct Binary Tree from Preorder and Inorder    (Medium)
 * https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder/
 * Category   : Trees — divide & conquer
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given two integer vectors — a tree's PREORDER and INORDER
 *   traversals (all values distinct) — reconstruct the original
 *   binary tree.
 * ---------------------------------------------------------------------
 * INTUITION
 *   Preorder starts with the ROOT. That root splits inorder into
 *   [left subtree values][root][right subtree values] — and the two
 *   halves tell us EXACTLY how big the left/right subtrees are. Then
 *   each subtree is the same problem on smaller slices: divide and
 *   conquer all the way down. Every slice is identified by its
 *   (preorder range, inorder range) pair.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Hash map of inorder indices (BEST)
 *   Pre-scan inorder into unordered_map value→index so "how big is
 *   the left subtree?" is an O(1) arithmetic question: left_size =
 *   in_map[root] - in_left. Build slices recursively.
 *   Time  Complexity : O(n)  — one map build + each node built once.
 *   Space Complexity : O(n)  — the map, plus O(h) call stack.
 *   WHY THE MAP: every recursion step needs "where is this value in
 *   inorder?" A linear scan costs O(n) per step → O(n²) total. The
 *   map turns it into O(1). Python's dict does this with OPEN
 *   ADDRESSING / LINEAR PROBING:
 *       h(k, i) = (hash(k) + i) mod m ,  i = 0, 1, 2, ...
 *   while C++ unordered_map uses separate chaining — both give O(1)
 *   average, which is all we need here.
 * ---------------------------------------------------------------------
 * APPROACH 2 — No map: linear scan (conceptually simpler, slower)
 *   Identical recursion, but the inorder root is located by scanning
 *   the slice linearly each time.
 *   Time  Complexity : O(n²)  — O(n) scan per recursion level.
 *   Space Complexity : O(h)   — only the call stack (no map).
 *   WHY BOTHER: proves the map is what buys the O(n) bound; on small
 *   inputs both are equally fast, on skewed input A2 degrades.
 * ---------------------------------------------------------------------
 * DEEP DIVE — slicing invariant
 *   Preorder range [pl, pr] and inorder range [il, ir] always describe
 *   the SAME subtree. root = pre[pl]. left subtree = pre[pl+1,
 *   pl+1+ls) × inorder [il, mid); right = pre[pl+1+ls, pr] × inorder
 *   (mid, ir]. Empty ranges → nullptr. That is the whole algorithm —
 *   recursion is just the for-loop of divide & conquer.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — traversal inputs
#include <unordered_map>  // std::unordered_map — value→index (approach 1)
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Recursion + hash map of inorder indices
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Rebuild a binary tree from its preorder + inorder.
     * Inputs  : preorder, inorder — the two traversals (unique values).
     * Output  : root pointer of the reconstructed tree (heap-allocated).
     */
    TreeNode* buildTree(const std::vector<int>& preorder, const std::vector<int>& inorder) {
        // value → index inside inorder: O(1) subtree-size arithmetic.
        std::unordered_map<int, int> in_index;
        for (int i = 0; i < static_cast<int>(inorder.size()); ++i) {
            in_index[inorder[i]] = i;
        }
        // Kick off the recursion over the FULL ranges of both vectors.
        return build(preorder, 0, static_cast<int>(preorder.size()) - 1,
                     inorder, 0, static_cast<int>(inorder.size()) - 1,
                     in_index);
    }

private:
    /* Purpose : Build one subtree from aligned range slices.
       Inputs  : pre/in — the two traversals; pl/pr + il/ir — the slice
                 bounds of the subtree being built; in_index — map.
       Output  : root pointer of the subtree (nullptr for empty range). */
    TreeNode* build(const std::vector<int>& pre, int pl, int pr,
                    const std::vector<int>& in, int il, int ir,
                    const std::unordered_map<int, int>& in_index) {
        // Empty slice → empty subtree (leaf sentinel of the recursion).
        if (pl > pr || il > ir) {
            return nullptr;
        }
        // PREORDER's first element of the slice is always the root.
        int root_val = pre[pl];
        TreeNode* root = new TreeNode(root_val);

        // The root's inorder position splits the slice in two halves.
        int mid = in_index.at(root_val);
        int left_size = mid - il;            // how many nodes sit left

        // Left subtree: pre[pl+1 .. pl+left_size] × in[il .. mid-1].
        root->left = build(pre, pl + 1, pl + left_size, in, il, mid - 1, in_index);
        // Right subtree: pre[pl+1+left_size .. pr] × in[mid+1 .. ir].
        root->right = build(pre, pl + 1 + left_size, pr, in, mid + 1, ir, in_index);
        return root;
    }
};

/* =====================================================================
 * APPROACH 2 : Same recursion, linear inorder scan (no map)
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Rebuild a binary tree from its preorder + inorder.
     * Inputs  : preorder, inorder — the two traversals (unique values).
     * Output  : root pointer of the reconstructed tree (heap-allocated).
     */
    TreeNode* buildTree(const std::vector<int>& preorder, const std::vector<int>& inorder) {
        return build(preorder, 0, static_cast<int>(preorder.size()) - 1,
                     inorder, 0, static_cast<int>(inorder.size()) - 1);
    }

private:
    /* Purpose : Build one subtree; finds the inorder root by scanning.
       Inputs  : pre/in — traversals; pl/pr + il/ir — slice bounds.
       Output  : root pointer of the subtree (nullptr for empty slice).
       Cost    : O(slice length) per call → O(n²) overall on skew. */
    TreeNode* build(const std::vector<int>& pre, int pl, int pr,
                    const std::vector<int>& in, int il, int ir) {
        if (pl > pr || il > ir) {
            return nullptr;
        }
        int root_val = pre[pl];
        TreeNode* root = new TreeNode(root_val);

        // Linear scan inside the inorder slice — the only difference
        // from approach 1, and the reason this is O(n²), not O(n).
        int mid = il;
        while (in[mid] != root_val) {
            ++mid;
        }
        int left_size = mid - il;
        root->left = build(pre, pl + 1, pl + left_size, in, il, mid - 1);
        root->right = build(pre, pl + 1 + left_size, pr, in, mid + 1, ir);
        return root;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example — preorder [3,9,20,15,7] × inorder [9,3,15,20,7]
    //         → tree [3,9,20,null,null,15,7].
    std::vector<int> pre1 = {3, 9, 20, 15, 7};
    std::vector<int> in1 = {9, 3, 15, 20, 7};
    // Test 2: single node.
    std::vector<int> pre2 = {-1};
    std::vector<int> in2 = {-1};
    // Test 3: right chain 1→2→3: pre [1,2,3] × in [1,2,3].
    std::vector<int> pre3 = {1, 2, 3};
    std::vector<int> in3 = {1, 2, 3};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    TreeNode* r1a = Solution_1().buildTree(pre1, in1);
    TreeNode* r1b = Solution_1().buildTree(pre2, in2);
    TreeNode* r1c = Solution_1().buildTree(pre3, in3);
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    TreeNode* r2a = Solution_2().buildTree(pre1, in1);
    TreeNode* r2b = Solution_2().buildTree(pre2, in2);
    TreeNode* r2c = Solution_2().buildTree(pre3, in3);
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB on Linux
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    // Verify by round-trip: a correct reconstruction must print the
    // SAME level-order tree as the reference built directly.
    std::cout << "Test 1: S1=";
    printTree(r1a);
    std::cout << " S2=";
    printTree(r2a);
    std::cout << " (expected [3,9,20,null,null,15,7])\n";
    std::cout << "Test 2: S1=";
    printTree(r1b);
    std::cout << " S2=";
    printTree(r2b);
    std::cout << " (expected [-1])\n";
    std::cout << "Test 3: S1=";
    printTree(r1c);
    std::cout << " S2=";
    printTree(r2c);
    std::cout << " (expected [1,2,3,null,null,null,null])\n";

    // Structural comparison against the expected trees. A local lambda
    // `eq` is the recursive equality walk — matches every node pair.
    bool all_ok = true;
    TreeNode* e1 = buildTree({3, 9, 20, std::nullopt, std::nullopt, 15, 7});
    auto eq = [](auto&& self, TreeNode* x, TreeNode* y) -> bool {
        if (x == nullptr || y == nullptr) { return x == y; }
        return x->val == y->val &&
               self(self, x->left, y->left) &&
               self(self, x->right, y->right);
    };
    all_ok = eq(eq, r1a, e1) && eq(eq, r2a, e1);
    std::cout << (all_ok ? "PASS : reconstruction matches expected trees."
                         : "FAIL : reconstruction differs from expected.")
              << "\n";

    std::cout << "Solution_1 (hash map, O(n))    : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (linear scan, O(n²)): time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";

    destroyTree(r1a); destroyTree(r1b); destroyTree(r1c);
    destroyTree(r2a); destroyTree(r2b); destroyTree(r2c);
    destroyTree(e1);
    return 0;
}
