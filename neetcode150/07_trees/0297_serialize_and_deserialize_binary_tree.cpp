/*
 * =====================================================================
 * LeetCode 297 : Serialize and Deserialize Binary Tree                (Hard)
 * https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
 * Category   : Trees — encoding
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design two operations:
 *     serialize(root)     → a string encoding the WHOLE tree,
 *     deserialize(str)    → rebuilds the identical tree from it.
 *   The format is ours to choose — any string that round-trips works.
 * ---------------------------------------------------------------------
 * INTUITION
 *   A traversal alone is ambiguous (inorder fits MANY trees). The fix:
 *   make every ABSENT child explicit. Recording a null marker for each
 *   missing child turns any traversal into a complete blueprint — a
 *   preorder walk with "null" markers contains every pointer decision
 *   needed to rebuild, in order.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Preorder DFS + null markers (BEST)
 *   Serialize: preorder visit, writing "null" for empty children.
 *   Deserialize: replay the token list in the SAME preorder.
 *   Time  Complexity : O(n)  — every node written/read exactly once.
 *   Space Complexity : O(n)  — the token string/list itself.
 *   WHY PREORDER: the ROOT comes first, so deserialization can build
 *   greedily — read a token, allocate the node, recurse into children.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Level-order BFS (LeetCode's own format)
 *   Serialize: queue-based level-order, "null" for missing children.
 *   Deserialize: queue replays the same level-order.
 *   Time  Complexity : O(n)  — every node processed exactly once.
 *   Space Complexity : O(n)  — token list + BFS queue width.
 * ---------------------------------------------------------------------
 * DEEP DIVE — why null markers make ANY traversal unambiguous
 *   n-node binary trees come in Catalan-many shapes but a traversal
 *   without markers has only 2n−1 slots to describe 2n pointers — the
 *   null entries ARE the missing pointers. Preorder+nulls is exactly
 *   the classic "1 2 X X 3 X X" format; level-order+nulls is exactly
 *   the "[3,9,20,null,null,15,7]" format LeetCode's own test harness
 *   uses. Both round-trip perfectly — the marker discipline is the
 *   entire trick.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — token storage / level-order
#include <string>         // std::string — the serialized payload
#include <sstream>        // std::istringstream — token splitting
#include <queue>          // std::queue — BFS (approach 2) + deserialize
#include <chrono>         // std::chrono — steady_clock timing for benchmark
#include <sys/resource.h> // getrusage — peak-RAM measurement for benchmark
#include "tree_node.h"    // shared TreeNode + buildTree/printTree/destroyTree

/* =====================================================================
 * APPROACH 1 : Preorder DFS + "null" markers
 * ===================================================================== */
class Solution_1 {
public:
    /*
     * Purpose : Flatten a tree into a preorder string with nulls.
     * Inputs  : root — tree root (may be nullptr).
     * Output  : e.g. "1,2,null,null,3,null,null".
     */
    std::string serialize(TreeNode* root) {
        std::string out;
        write(root, out);
        return out;
    }

    /*
     * Purpose : Rebuild the tree from a preorder+nulls string.
     * Inputs  : data — the string produced by serialize().
     * Output  : root pointer of the reconstructed (heap-allocated) tree.
     */
    TreeNode* deserialize(const std::string& data) {
        // Split on commas into tokens — the replay buffer.
        std::istringstream stream(data);
        std::string token;
        std::vector<std::string> tokens;
        while (std::getline(stream, token, ',')) {
            tokens.push_back(token);
        }
        // Shared cursor walks the token list; read() consumes as needed.
        int idx = 0;
        return read(tokens, idx);
    }

private:
    /* Purpose : Preorder write of one subtree into `out`.
       Inputs  : node — current node; out — string being built.
       Output  : nothing (appends "val," or "null,"). */
    void write(TreeNode* node, std::string& out) {
        // Absent child → explicit null marker: the shape-preserving bit.
        if (node == nullptr) {
            if (!out.empty()) { out += ","; }
            out += "null";
            return;
        }
        if (!out.empty()) { out += ","; }
        out += std::to_string(node->val);
        write(node->left, out);       // preorder: node, left, right
        write(node->right, out);
    }

    /* Purpose : Preorder read — allocate nodes from tokens.
       Inputs  : tokens — replay buffer; idx — shared cursor.
       Output  : root of the rebuilt subtree (nullptr for "null"). */
    TreeNode* read(const std::vector<std::string>& tokens, int& idx) {
        // "null" marker → no child here; consume it, hand back nothing.
        if (tokens[idx] == "null") {
            ++idx;
            return nullptr;
        }
        // Otherwise allocate the node and rebuild children in preorder.
        TreeNode* node = new TreeNode(std::stoi(tokens[idx++]));
        node->left = read(tokens, idx);
        node->right = read(tokens, idx);
        return node;
    }
};

/* =====================================================================
 * APPROACH 2 : Level-order BFS — LeetCode's own "[..,null,..]" format
 * ===================================================================== */
class Solution_2 {
public:
    /*
     * Purpose : Flatten a tree into a level-order string with nulls.
     * Inputs  : root — tree root (may be nullptr).
     * Output  : e.g. "3,9,20,null,null,15,7".
     */
    std::string serialize(TreeNode* root) {
        if (root == nullptr) {
            return "";                   // empty tree → empty payload
        }
        std::string out;
        std::queue<TreeNode*> pending;   // BFS frontier, nulls included
        pending.push(root);
        while (!pending.empty()) {
            TreeNode* cur = pending.front();
            pending.pop();
            if (!out.empty()) { out += ","; }
            if (cur == nullptr) {
                out += "null";           // missing child, explicit marker
                continue;                // nothing to enqueue for nulls
            }
            out += std::to_string(cur->val);
            // Enqueue BOTH children even when absent — their null
            // markers are what preserve the tree's exact shape.
            pending.push(cur->left);
            pending.push(cur->right);
        }
        return out;
    }

    /*
     * Purpose : Rebuild the tree from a level-order+nulls string.
     * Inputs  : data — the string produced by serialize().
     * Output  : root pointer of the reconstructed (heap-allocated) tree.
     */
    TreeNode* deserialize(const std::string& data) {
        // Empty payload → empty tree.
        if (data.empty()) {
            return nullptr;
        }
        std::istringstream stream(data);
        std::string token;
        std::vector<std::string> tokens;
        while (std::getline(stream, token, ',')) {
            tokens.push_back(token);
        }
        // First token is the root; queue replays parent→children order.
        TreeNode* root = new TreeNode(std::stoi(tokens[0]));
        std::queue<TreeNode*> pending;
        pending.push(root);
        int i = 1;                       // next token to consume
        while (!pending.empty() && i < static_cast<int>(tokens.size())) {
            TreeNode* cur = pending.front();
            pending.pop();
            // Next token = left child; "null" → child simply absent.
            if (tokens[i] != "null") {
                cur->left = new TreeNode(std::stoi(tokens[i]));
                pending.push(cur->left);
            }
            ++i;
            // Following token = right child of the same parent.
            if (i < static_cast<int>(tokens.size()) && tokens[i] != "null") {
                cur->right = new TreeNode(std::stoi(tokens[i]));
                pending.push(cur->right);
            }
            ++i;
        }
        return root;
    }
};

/* =====================================================================
 * BENCHMARK — both solutions: serialize→deserialize→compare round-trip
 * ===================================================================== */
int main() {
    // Test 1: official example — [1,2,3,null,null,4,5].
    TreeNode* t1 = buildTree({1, 2, 3, std::nullopt, std::nullopt, 4, 5});
    // Test 2: empty tree.
    TreeNode* t2 = nullptr;
    // Test 3: left chain 1→2→3 — plenty of null markers.
    TreeNode* t3 = buildTree({1, 2, std::nullopt, 3});

    // Local recursive equality walk for round-trip verification.
    auto eq = [](auto&& self, TreeNode* x, TreeNode* y) -> bool {
        if (x == nullptr || y == nullptr) { return x == y; }
        return x->val == y->val && self(self, x->left, y->left) && self(self, x->right, y->right);
    };

    struct rusage before_1, after_1, before_2, after_2;
    getrusage(RUSAGE_SELF, &before_1);
    auto start_1 = std::chrono::steady_clock::now();
    TreeNode* back1[3] = {nullptr, nullptr, nullptr};
    std::string s1[3];
    for (int i = 0; i < 3; ++i) {
        s1[i] = Solution_1().serialize(i == 0 ? t1 : (i == 1 ? t2 : t3));
        back1[i] = Solution_1().deserialize(s1[i]);
    }
    auto end_1 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_1);

    getrusage(RUSAGE_SELF, &before_2);
    auto start_2 = std::chrono::steady_clock::now();
    TreeNode* back2[3] = {nullptr, nullptr, nullptr};
    std::string s2[3];
    for (int i = 0; i < 3; ++i) {
        s2[i] = Solution_2().serialize(i == 0 ? t1 : (i == 1 ? t2 : t3));
        back2[i] = Solution_2().deserialize(s2[i]);
    }
    auto end_2 = std::chrono::steady_clock::now();
    getrusage(RUSAGE_SELF, &after_2);

    long mem_1 = after_1.ru_maxrss - before_1.ru_maxrss;   // KB on Linux
    long mem_2 = after_2.ru_maxrss - before_2.ru_maxrss;
    double us_1 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_1 - start_1).count() / 1000.0;
    double us_2 = std::chrono::duration_cast<std::chrono::nanoseconds>(end_2 - start_2).count() / 1000.0;

    TreeNode* originals[3] = {t1, t2, t3};
    bool all_ok = true;
    for (int i = 0; i < 3; ++i) {
        bool ok = eq(eq, back1[i], originals[i]) && eq(eq, back2[i], originals[i]);
        all_ok = all_ok && ok;
        std::cout << "Test " << (i + 1) << ": S1=\"" << s1[i] << "\" S2=\"" << s2[i]
                  << "\"" << (ok ? "  PASS (round-trip)" : "  FAIL") << "\n";
    }

    std::cout << "Solution_1 (preorder + nulls) : time = " << us_1
              << " µs  peak-ram-delta = " << mem_1 << " KB\n";
    std::cout << "Solution_2 (level-order BFS)  : time = " << us_2
              << " µs  peak-ram-delta = " << mem_2 << " KB\n";
    std::cout << (all_ok ? "PASS : every round-trip reproduces the original tree."
                         : "FAIL : at least one round-trip diverged.")
              << "\n";

    destroyTree(t1); destroyTree(t3);
    for (int i = 0; i < 3; ++i) { destroyTree(back1[i]); destroyTree(back2[i]); }
    return 0;
}