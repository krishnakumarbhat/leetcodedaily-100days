/*
 * =====================================================================
 * LeetCode 211 : Design Add and Search Words Data Structure       (Medium)
 * https://leetcode.com/problems/design-add-and-search-words-data-structure/
 * Category   : Tries
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Design a word dictionary with:
 *     addWord(word)  : store the word (lowercase letters only).
 *     search(word)   : true iff some stored word matches. The query
 *                      may contain the wildcard '.' which matches ANY
 *                      single letter (e.g. "b.." matches "bad").
 * ---------------------------------------------------------------------
 * INTUITION
 *   Words live in a trie (shared prefixes → O(L) walks). The twist is
 *   the '.' wildcard: at a '.' we do not know WHICH child to follow —
 *   we must branch into every child and let the rest of the pattern
 *   decide. Branching is "search" in the deep sense: either DFS
 *   (recurse, try one branch fully before the next) or BFS (advance
 *   every candidate one level in lockstep).
 * ---------------------------------------------------------------------
 * APPROACH 1 — Trie + recursive DFS (best)
 *   Walk the trie with a recursion index i into the pattern.
 *     pattern[i] == '.' → try EVERY child; true if any subtree matches.
 *     pattern[i] == 'c' → follow only child 'c'; missing ⇒ false.
 *     i == len(pattern) → answer = isEnd of the current node.
 *   The '.' branch is O(26) per level worst case; letters stay O(1).
 *   Time  Complexity : O(26^d) worst case, d = number of '.' in query;
 *                      O(L) with no wildcards. addWord is O(L).
 *   Space Complexity : O(26 · n · L) trie nodes worst case + O(L)
 *                      recursion depth.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Trie + iterative BFS (level-by-level frontier)
 *   Keep a FRONTIER of candidate nodes. For each pattern char:
 *     '.' → replace frontier with ALL children of every candidate.
 *     'c' → keep only the 'c'-child of every candidate.
 *   Any empty frontier ⇒ no match. At the end, true iff some
 *   frontier node has isEnd. Same complexity as DFS, but the call
 *   stack is gone (explicit vector) and every candidate advances in
 *   lockstep — the natural "wavefront" view of wildcard matching.
 *   Time  Complexity : O(26^d) worst case, O(L) without wildcards.
 *   Space Complexity : O(26^d) frontier size worst case.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — why a trie, and the wildcard cost
 *   Without '.' this is exactly LeetCode 208's trie: each node =
 *   26 children + isEnd. With '.', the search becomes a tree WALK
 *   with branching: every '.' multiplies the number of live paths by
 *   (up to) 26, so d wildcards cost up to 26^d node visits. DFS
 *   visits one path to its end before backtracking; BFS visits all
 *   paths one level at a time — identical work, different order.
 *   Python dict children (probing h(k,i) = (hash(k)+i) mod m) are the
 *   lean choice for '.'-scanning here: iterating only the children
 *   that EXIST beats scanning 26 fixed slots per branch.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — BFS frontier, test ops
#include <string>         // std::string — words and patterns
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak-RAM measurement

/* Shared trie node: 26 child pointers + end-of-word flag. */
struct TrieNode {
    TrieNode* children[26]; // letter → child (null = absent)
    bool isEnd;             // an inserted word terminates here
    TrieNode() : children(), isEnd(false) {}
};

/* =====================================================================
 * APPROACH 1 : trie + recursive DFS wildcard search
 * ===================================================================== */
class Solution_One {
private:
    TrieNode* root;

    static void freeNode(TrieNode* n) {
        for (int i = 0; i < 26; ++i) {
            if (n->children[i]) freeNode(n->children[i]);
        }
        delete n;
    }

    /* Purpose : Match pattern[i..] against the subtree of `n`.
     * Inputs  : n  — current trie node; w — the pattern; i — position.
     * Output  : true iff some root-to-descendant path spells w[i..]. */
    static bool dfs(TrieNode* n, const std::string& w, int i) {
        if (i == static_cast<int>(w.size())) return n->isEnd; // pattern spent
        char c = w[i];
        if (c == '.') {
            // Wildcard: ANY child may be the correct next step — try all.
            for (int k = 0; k < 26; ++k) {
                if (n->children[k] && dfs(n->children[k], w, i + 1)) return true;
            }
            return false;
        }
        TrieNode* child = n->children[c - 'a'];
        return child != nullptr && dfs(child, w, i + 1); // fixed letter: one path
    }

public:
    /* Purpose : Build an empty dictionary trie.
     * Inputs  : none.
     * Output  : a ready-to-use object. */
    Solution_One() : root(new TrieNode()) {}

    /* Purpose : Free every node allocated by the trie.
     * Inputs  : none.
     * Output  : nothing. */
    ~Solution_One() { freeNode(root); }

    /* Purpose : Store `word` in the trie (same walk as LeetCode 208).
     * Inputs  : word — lowercase string.
     * Output  : void. */
    void addWord(const std::string& word) {
        TrieNode* n = root;
        for (char c : word) {
            int k = c - 'a';
            if (!n->children[k]) n->children[k] = new TrieNode();
            n = n->children[k];
        }
        n->isEnd = true;
    }

    /* Purpose : Match a pattern containing '.' wildcards against the trie.
     * Inputs  : word — pattern; '.' matches any single letter.
     * Output  : true iff some inserted word matches the pattern. */
    bool search(const std::string& word) const {
        return dfs(root, word, 0);
    }
};

/* =====================================================================
 * APPROACH 2 : trie + iterative BFS wildcard search (frontier waves)
 * ===================================================================== */
class Solution_Two {
private:
    TrieNode* root;

    static void freeNode(TrieNode* n) {
        for (int i = 0; i < 26; ++i) {
            if (n->children[i]) freeNode(n->children[i]);
        }
        delete n;
    }

public:
    /* Purpose : Build an empty dictionary trie.
     * Inputs  : none.
     * Output  : a ready-to-use object. */
    Solution_Two() : root(new TrieNode()) {}

    /* Purpose : Free every node allocated by the trie.
     * Inputs  : none.
     * Output  : nothing. */
    ~Solution_Two() { freeNode(root); }

    /* Purpose : Store `word` in the trie.
     * Inputs  : word — lowercase string.
     * Output  : void. */
    void addWord(const std::string& word) {
        TrieNode* n = root;
        for (char c : word) {
            int k = c - 'a';
            if (!n->children[k]) n->children[k] = new TrieNode();
            n = n->children[k];
        }
        n->isEnd = true;
    }

    /* Purpose : Match a pattern with '.' wildcards using a frontier.
     * Inputs  : word — pattern; '.' matches any single letter.
     * Output  : true iff some inserted word matches. */
    bool search(const std::string& word) const {
        std::vector<TrieNode*> frontier; // nodes alive after the chars so far
        frontier.push_back(root);
        for (char c : word) {
            std::vector<TrieNode*> next; // candidates for the NEXT level
            if (c == '.') {
                // Wildcard: every candidate fans out into all its children.
                for (const TrieNode* n : frontier) {
                    for (int k = 0; k < 26; ++k) {
                        if (n->children[k]) next.push_back(n->children[k]);
                    }
                }
            } else {
                // Fixed letter: each candidate keeps only its c-child.
                for (const TrieNode* n : frontier) {
                    TrieNode* child = n->children[c - 'a'];
                    if (child) next.push_back(child);
                }
            }
            if (next.empty()) return false; // every branch died → no match
            frontier.swap(next);            // advance the wavefront
        }
        for (const TrieNode* n : frontier) {
            if (n->isEnd) return true; // some surviving path is a word
        }
        return false;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 batches, compare time + RAM
 * ===================================================================== */
namespace {
    /* One batch: "add X" stores; "search X" must equal `expect`'s entry. */
    struct TestCase {
        std::string name;
        std::vector<std::string> ops;
        std::vector<bool> expect;
    };
}

template <typename Solver>
bool runOps(Solver& s, const TestCase& tc) {
    size_t j = 0; // position inside tc.expect — only advances on checks
    for (size_t i = 0; i < tc.ops.size(); ++i) {
        const std::string& op = tc.ops[i];
        if (op.rfind("add ", 0) == 0) {
            s.addWord(op.substr(4)); // adds never fail — skip the check
            continue;
        }
        if (s.search(op.substr(7)) != tc.expect[j]) return false;
        ++j;
    }
    return true;
}

template <typename Solver>
bool bench(const std::string& label, const std::vector<TestCase>& tests) {
    bool allOk = true;
    for (const TestCase& tc : tests) {
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto start = std::chrono::high_resolution_clock::now();
        Solver solver;                              // fresh object per batch
        bool ok = runOps(solver, tc);
        auto end = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);

        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1000.0;
        long memKb = after.ru_maxrss - before.ru_maxrss; // ru_maxrss is in KB
        allOk = allOk && ok;
        std::cout << label << " | " << tc.name << " : "
                  << (ok ? "PASS" : "FAIL")
                  << "  time = " << us << " µs  peak-ram-delta = "
                  << memKb << " KB\n";
    }
    return allOk;
}

int main() {
    /* Three batches: the official example, wildcards in the middle/end,
       and an empty-word edge case. */
    const std::vector<TestCase> tests = {
        { "problem example",
          { "add bad", "add dad", "add mad",
            "search pad", "search .ad", "search b.." },
          { false, true, true } },
        { "middle + tail wildcards",
          { "add hello", "add world", "add help",
            "search h.llo", "search h.llx", "search ...lo",
            "search he..o", "search w.r.x", "search .....", "search help." },
          { true, false, true, true, false, true, false } },
        { "empty word edge",
          { "add ", "search ", "search .", "search a" },
          { true, false, false } }
    };

    bool ok1 = bench<Solution_One>("Approach 1 (trie + DFS)   ", tests);
    bool ok2 = bench<Solution_Two>("Approach 2 (trie + BFS)   ", tests);

    std::cout << (ok1 && ok2
        ? "PASS : both approaches return the expected answers on all batches."
        : "FAIL : at least one answer was wrong.") << "\n";
    return 0;
}
