/*
 * =====================================================================
 * tree_node.h — SHARED TREE UTILITIES for every problem in section 07
 * ---------------------------------------------------------------------
 * WHAT A HEADER FILE IS
 *   A header (.h) is a text file whose contents are PASTED into any
 *   .cpp that `#include`s it — the C preprocessor literally copies the
 *   text before compilation. This lets every solution file share the
 *   same TreeNode struct + tree helpers without duplicating a single
 *   line. Fix a bug in buildTree once and all 17 problems get the fix.
 * ---------------------------------------------------------------------
 * WHAT AN INCLUDE GUARD IS (and why it matters)
 *   A .cpp may transitively include the same header twice (a.h includes
 *   tree_node.h AND b.h includes tree_node.h). Without a guard the
 *   struct TreeNode would be DEFINED twice → "redefinition" compile
 *   error. The guard is a preprocessor trick:
 *       #ifndef TREE_NODE_H   → if the macro is NOT yet defined...
 *       #define TREE_NODE_H   → ...define it now, then emit the body.
 *   The second time the header is seen, the macro EXISTS, so the whole
 *   body is skipped. One header, one definition, zero errors.
 * ---------------------------------------------------------------------
 * TreeNode FORMAT (identical to LeetCode's C++ tree questions)
 *   A node is a struct allocated on the HEAP (operator new). `left`
 *   and `right` are POINTERS to child nodes, or nullptr when the child
 *   is absent. The root pointer is the handle to the whole tree —
 *   every algorithm walks left/right pointers from it.
 * ---------------------------------------------------------------------
 * buildTree INPUT FORMAT
 *   A level-order (breadth-first) vector, where std::nullopt marks a
 *   MISSING child, exactly like LeetCode's "[3,9,20,null,null,15,7]".
 *   std::optional<int> is C++'s spelling of "int OR nothing" — needed
 *   because a valid tree may contain ANY int, so no sentinel value
 *   (e.g. -1) could safely mean "missing".
 * =====================================================================
 */

#ifndef TREE_NODE_H
#define TREE_NODE_H

#include <vector>    // std::vector — the level-order input container
#include <optional>  // std::optional — "int or missing" child marker
#include <queue>     // std::queue — FIFO used by buildTree / printTree
#include <iostream>  // std::cout — printTree output stream
#include <cstddef>   // std::size_t — index type for vector sizes

/* One binary-tree node: a value plus pointers to two children. */
struct TreeNode {
    int val;                // the data stored in this node
    TreeNode* left;         // pointer to left child  (nullptr = none)
    TreeNode* right;        // pointer to right child (nullptr = none)

    /* Constructor: value + optional children. Defaulting left/right to
       nullptr means `new TreeNode(5)` alone already builds a leaf. */
    explicit TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr)
        : val(v), left(l), right(r) {}
};

/* ---------------------------------------------------------------------
 * Purpose : Build a real binary tree from a level-order vector where
 *           std::nullopt means "no child here" (LeetCode's format).
 * Inputs  : vals — level-order values; index 0 is the root.
 * Output  : pointer to the root of the freshly allocated tree, or
 *           nullptr when vals is empty / starts with nullopt.
 * Why BFS: the input is *already* breadth-first, so we replay it with
 *           a FIFO queue holding parents whose children are not filled
 *           yet; each parent consumes the next two slots (left, right).
 * ------------------------------------------------------------------ */
TreeNode* buildTree(const std::vector<std::optional<int>>& vals) {
    // Empty input (or null root) → empty tree → allocate nothing.
    if (vals.empty() || !vals[0].has_value()) {
        return nullptr;
    }

    // Slot 0 is the root; allocate it on the heap, like LeetCode does.
    TreeNode* root = new TreeNode(vals[0].value());

    // FIFO of parents still waiting for their children to be attached.
    std::queue<TreeNode*> pending;
    pending.push(root);

    // Read the remaining level-order slots left → right.
    std::size_t i = 1;
    while (!pending.empty() && i < vals.size()) {
        // The oldest unfilled parent receives the next two slots.
        TreeNode* cur = pending.front();
        pending.pop();

        // Slot i = left child; nullopt → the child simply does not exist.
        if (i < vals.size() && vals[i].has_value()) {
            cur->left = new TreeNode(vals[i].value());
            pending.push(cur->left);   // this child will need children too
        }
        ++i;                           // consume the left slot

        // Slot i = right child of the SAME parent.
        if (i < vals.size() && vals[i].has_value()) {
            cur->right = new TreeNode(vals[i].value());
            pending.push(cur->right);
        }
        ++i;                           // consume the right slot
    }
    return root;                       // handle to the whole tree
}

/* ---------------------------------------------------------------------
 * Purpose : Print a tree as a level-order list (LeetCode's format),
 *           so benchmark output is human-readable and comparable.
 * Inputs  : root — pointer to the tree's root (may be nullptr).
 * Output  : prints "[3,9,20,null,null,15,7]" to std::cout.
 * Why BFS: printed order must be the SAME order buildTree consumes —
 *           print and build are inverse operations, so round-trips can
 *           be verified by eye.
 * ------------------------------------------------------------------ */
void printTree(const TreeNode* root) {
    // Empty tree prints as an empty list.
    if (root == nullptr) {
        std::cout << "[]";
        return;
    }

    // BFS through every node; missing children are printed as "null".
    std::queue<const TreeNode*> q;
    q.push(root);
    std::cout << "[";
    bool first = true;                 // comma placement: avoid leading ", "
    while (!q.empty()) {
        const TreeNode* cur = q.front();
        q.pop();

        // Comma before every entry except the very first one.
        if (!first) { std::cout << ","; }
        first = false;

        // nullptr means "missing child" — printed, not expanded.
        if (cur == nullptr) {
            std::cout << "null";
            continue;
        }
        std::cout << cur->val;

        // Enqueue BOTH children regardless of presence: missing children
        // are represented by nullptr queue entries, matching buildTree's
        // input format exactly.
        q.push(cur->left);
        q.push(cur->right);
    }
    std::cout << "]";
}

/* ---------------------------------------------------------------------
 * Purpose : Free every node of the tree (post-order: children first).
 * Inputs  : root — pointer to the tree's root (may be nullptr).
 * Output  : nothing; deallocates all heap nodes (no memory leaks).
 * Why post-order: a node's children must be deleted BEFORE the node
 *           itself, otherwise the parent dies first and the pointers
 *           needed to reach the children are lost forever.
 * ------------------------------------------------------------------ */
void destroyTree(TreeNode* root) {
    // Nothing to free — the empty tree needs no cleanup.
    if (root == nullptr) {
        return;
    }
    destroyTree(root->left);           // delete the whole left subtree
    destroyTree(root->right);          // delete the whole right subtree
    delete root;                       // children gone → safe to free node
}

#endif /* TREE_NODE_H */
