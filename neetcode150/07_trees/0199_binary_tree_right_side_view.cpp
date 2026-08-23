/*
 * =====================================================================
 * LeetCode 199 : Binary Tree Right Side View                        (Medium)
 * https://leetcode.com/problems/binary-tree-right-side-view/
 * Category   : Trees — BFS / level capture
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Imagine standing to the RIGHT of a binary tree: report, top to
 *   bottom, the value of the node you see at every level — i.e. the
 *   LAST node of each level (rightmost existing node).
 * ---------------------------------------------------------------------
 * INTUITION
 *   A level's rightmost node is simply its LAST value when the level
 *   is collected left → right. Level-order BFS therefore answers the
 *   question almost for free: finish a level, take its tail.
 *   A DFS alternative: if we always walk RIGHT before LEFT, the FIRST
 *   node ever visited at a given depth is exactly its rightmost node.
 * ---------------------------------------------------------------------
 * APPROACH 1 — BFS level snapshots (BEST, intuitive)
 *   Same per-level snapshot loop as level-order traversal; instead of
 *   storing the whole row, keep only its last element.
 *   Time  Complexity : O(n)  — every node enqueued/dequeued once.
 *   Space Complexity : O(n)  — queue holds the widest level (≤ n).
 * ---------------------------------------------------------------------
 * APPROACH 2 — DFS, right-first, first-visit-per-depth
 *   dfs(node, depth): if depth equals the count of levels recorded so
 *   far, this is the FIRST node seen at that depth → append it. Then
 *   recurse RIGHT first, LEFT second — rightmost wins the race.
 *   Time  Complexity : O(n)  — every node visited exactly once.
 *   Space Complexity : O(h)  — call stack, h = tree height.
 * ---------------------------------------------------------------------
 * DEEP DIVE — same answer, two traversal philosophies
 *   BFS sees levels HORIZONTALLY (who is last in the row) — O(w)
 *   queue memory. DFS sees levels VERTICALLY (who is first to arrive
 *   at a depth) — O(h) stack memory. On a wide-but-shallow tree BFS
 *   costs more memory; on a narrow-but-deep tree DFS does. Both are
 *   O(n) time; the choice is which axis you want to pay for.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — output + level-order tests
#include <queue>          // std::queue — FIFO used by approach 1
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : BFS — keep the last node of every level
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Return the rightmost value of every level, top-down.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : vector<int> — the right side view, root first.
     */
    std::vector<int> rightSideView(TreeNode* root) {
        std::vector<int> view;
        if (root == nullptr) {
            return view;
        }
        std::queue<TreeNode*> pending;   // FIFO — next frontier
        pending.push(root);

        while (!pending.empty()) {
            int level_size = static_cast<int>(pending.size());
            int last_val = 0;            // will hold the row's tail
            for (int i = 0; i < level_size; ++i) {
                TreeNode* cur = pending.front();
                pending.pop();
                last_val = cur->val;     // overwritten → ends as LAST
                if (cur->left != nullptr) {
                    pending.push(cur->left);
                }
                if (cur->right != nullptr) {
                    pending.push(cur->right);
                }
            }
            view.push_back(last_val);    // rightmost node of this level
        }
        return view;
    }
};

/* =====================================================================
 * APPROACH 2 : DFS right-first — first visit to a depth wins
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Return the rightmost value of every level, top-down.
     * Inputs  : root — pointer to the tree's root (may be nullptr).
     * Output  : vector<int> — the right side view, root first.
     */
    std::vector<int> rightSideView(TreeNode* root) {
        std::vector<int> view;
        walk(root, 0, view);
        return view;
    }

private:
    /* Purpose : Right-first preorder; record first node per depth.
       Inputs  : node — current node; depth — its distance from root;
                 view — output, grown on first visit to each depth.
       Output  : nothing (may append node->val to view). */
    void walk(TreeNode* node, int depth, std::vector<int>& view) {
        if (node == nullptr) {
            return;
        }
        // depth == view.size() ⇔ no node at this depth was visited yet
        // → THIS is the rightmost (we always descend right first).
        if (depth == static_cast<int>(view.size())) {
            view.push_back(node->val);
        }
        walk(node->right, depth + 1, view);   // right side has priority
        walk(node->left, depth + 1, view);    // left fills the gaps
    }
};

/* =====================================================================
 * BENCHMARK — both solutions on 3 tests: time + peak RAM
 * ===================================================================== */
int main() {
    // Test 1: official example → [1,3,4].
    TreeNode* t1 = buildTree({1, 2, 3, std::nullopt, 5, std::nullopt, 4});
    // Test 2: single node → [1].
    TreeNode* t2 = buildTree({1});
    // Test 3: left chain 1→2→3 — only left nodes exist → [1,2,3].
    TreeNode* t3 = buildTree({1, 2, std::nullopt, 3});
    const std::vector<int> expected[3] = {{1, 3, 4}, {1}, {1, 2, 3}};

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    std::vector<int> r1[3] = {Solution_1().rightSideView(t1),
                              Solution_1().rightSideView(t2),
                              Solution_1().rightSideView(t3)};
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    std::vector<int> r2[3] = {Solution_2().rightSideView(t1),
                              Solution_2().rightSideView(t2),
                              Solution_2().rightSideView(t3)};
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
        std::cout << "] (expected [";
        for (size_t j = 0; j < expected[i].size(); ++j) { std::cout << expected[i][j] << (j + 1 < expected[i].size() ? "," : ""); }
        std::cout << "])" << (ok ? "  PASS" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (BFS snapshots)     : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (DFS right-first)   : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : both views match expected."
                         : "FAIL : at least one view differs.")
              << "\n";

    destroyTree(t1); destroyTree(t2); destroyTree(t3);
    return 0;
}