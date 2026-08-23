/*
 * =====================================================================
 * LeetCode 212 : Word Search II                                        (Hard)
 * https://leetcode.com/problems/word-search-ii/
 * Category   : Tries
 * ---------------------------------------------------------------------
 * PROBLEM
 *   Given an m×n board of letters and a list of words, return EVERY
 *   word that can be spelled by moving between ADJACENT cells (up/
 *   down/left/right, diagonals excluded). A cell may be used at most
 *   once per word.
 * ---------------------------------------------------------------------
 * INTUITION
 *   N words on one board → run ONE shared search instead of N
 *   independent ones. Insert all words into a trie, then walk the
 *   board with grid-DFS; at every cell, check whether the letter
 *   continues the current trie path. A path that reaches a word-end
 *   is a hit. Because many words share prefixes, a single DFS tree
 *   serves all of them — this is the "why trie" moment.
 * ---------------------------------------------------------------------
 * APPROACH 1 — Trie + grid DFS backtracking (foundation)
 *   Build the trie (each terminal node stores its full word, which
 *   doubles as a "found" marker). For every cell, DFS: prune when the
 *   letter has no trie child; mark cells '#' while visiting to stop
 *   re-use, restore on backtrack. When a node's stored word is found,
 *   record it and CLEAR the stored word so it is never reported again.
 *   Time  Complexity : O(m·n·4^L) worst case — L = max word length,
 *                      but the trie prunes dead prefixes early.
 *   Space Complexity : O(26·n·L) trie + O(L) recursion depth.
 * ---------------------------------------------------------------------
 * APPROACH 2 — Trie + grid DFS with branch pruning (BEST)
 *   Same walk, plus a refs counter on every node = number of words
 *   still reachable through it. When a node's last remaining word is
 *   found, its refs drops to 0 and the whole dead branch is DELETED
 *   from the trie — future DFS never re-explores it. This removes
 *   the classic "found word still costs DFS time on every later
 *   cell" waste.
 *   Time  Complexity : O(m·n·4^L) worst case, faster in practice.
 *   Space Complexity : O(26·n·L) trie + O(L) recursion depth.
 * ---------------------------------------------------------------------
 * DATA STRUCTURE DEEP DIVE — pruning + shared prefixes
 *   A plain hash set of words cannot guide the walk: from cell (r,c)
 *   you would have to ask "which words start with the letters I have
 *   spelled so far?" — a PREFIX query, exactly what hash maps cannot
 *   answer (probe h(k,i) = (hash(k)+i) mod m only finds exact keys).
 *   The trie answers it in O(1) per letter: one child lookup decides
 *   whether to descend or prune. Deleting used words (A2) turns the
 *   trie into a live accumulator — each word is discovered exactly
 *   once and its branch dies afterwards, so later cells stop paying
 *   for it. Memory math: n words of avg length L share prefix nodes,
 *   worst case n·L nodes × 26 pointers.
 * =====================================================================
 */

#include <iostream>       // std::cout — printing benchmark results
#include <vector>         // std::vector — board, words, results
#include <string>         // std::string — words
#include <chrono>         // std::chrono — high-resolution timing
#include <sys/resource.h> // getrusage — peak-RAM measurement

namespace {
    /* Trie node for Word Search II: 26 children, stored word, refs. */
    struct TrieNode {
        TrieNode* children[26];
        std::string word; // non-empty ⇒ this node ENDS a not-yet-found word
        int refs;         // words still reachable through this node
        TrieNode() : children(), word(), refs(0) {}
    };

    /* Shared builder: insert `w`, bumping refs along the path. */
    void insertWord(TrieNode* root, const std::string& w) {
        TrieNode* n = root;
        ++n->refs;
        for (char c : w) {
            int k = c - 'a';
            if (!n->children[k]) n->children[k] = new TrieNode();
            n = n->children[k];
            ++n->refs;
        }
        n->word = w; // terminal node remembers its own word
    }

    void freeNode(TrieNode* n) {
        for (int i = 0; i < 26; ++i) {
            if (n->children[i]) freeNode(n->children[i]);
        }
        delete n;
    }

    /* Does `words` contain `w`? (order-free result check) */
    bool contains(const std::vector<std::string>& words, const std::string& w) {
        for (const std::string& s : words) {
            if (s == w) return true;
        }
        return false;
    }
}

/* =====================================================================
 * APPROACH 1 : trie + grid DFS backtracking (foundation)
 * ===================================================================== */
class Solution_One {
private:
    TrieNode* root;
    std::vector<std::string> found;
    int rows, cols;

    /* Purpose : Walk the board from (r,c), extending the trie path `n`.
     * Inputs  : board — mutable grid; '#' marks a cell in use.
     *           r, c  — current cell; n — trie node for the path so far.
     * Output  : found gains every word completed on this descent. */
    void dfs(std::vector<std::vector<char>>& board, int r, int c, TrieNode* n) {
        if (r < 0 || r >= rows || c < 0 || c >= cols) return; // off the grid
        if (board[r][c] == '#') return;                       // cell in use
        int k = board[r][c] - 'a';
        if (!n->children[k]) return;        // no word continues this way — prune
        TrieNode* child = n->children[k];
        if (!child->word.empty()) {         // this path spells a full word
            found.push_back(child->word);   // report it…
            child->word.clear();            // …and never report it again
        }
        char save = board[r][c];
        board[r][c] = '#';                  // claim the cell (no re-use)
        dfs(board, r + 1, c, child);        // four adjacent neighbours
        dfs(board, r - 1, c, child);
        dfs(board, r, c + 1, child);
        dfs(board, r, c - 1, child);
        board[r][c] = save;                 // backtrack: release the cell
    }

public:
    /* Purpose : Find all words spellable on the board via the trie.
     * Inputs  : board — m×n grid of letters; words — search list.
     * Output  : every word in `words` found on the board. */
    std::vector<std::string> findWords(std::vector<std::vector<char>>& board,
                                       const std::vector<std::string>& words) {
        root = new TrieNode();
        for (const std::string& w : words) insertWord(root, w);
        found.clear();
        rows = static_cast<int>(board.size());
        cols = rows ? static_cast<int>(board[0].size()) : 0;
        for (int r = 0; r < rows; ++r) {          // start DFS at every cell
            for (int c = 0; c < cols; ++c) {
                dfs(board, r, c, root);
            }
        }
        std::vector<std::string> result = found;
        freeNode(root);
        return result;
    }
};

/* =====================================================================
 * APPROACH 2 : trie + grid DFS with branch pruning (best)
 * ===================================================================== */
class Solution_Two {
private:
    TrieNode* root;
    std::vector<std::string> found;
    int rows, cols;

    /* Purpose : Walk the board from (r,c), then DELETE dead branches.
     * Inputs  : board — mutable grid; '#' marks a cell in use.
     *           r, c  — current cell; n — trie node for the path so far.
     * Output  : found gains every word completed on this descent. */
    void dfs(std::vector<std::vector<char>>& board, int r, int c, TrieNode* n) {
        if (r < 0 || r >= rows || c < 0 || c >= cols) return;
        if (board[r][c] == '#') return;
        int k = board[r][c] - 'a';
        TrieNode* child = n->children[k];
        if (!child || child->refs <= 0) return; // branch already exhausted
        if (!child->word.empty()) {             // word completed here
            found.push_back(child->word);
            child->word.clear();
            --child->refs;                      // one fewer word in this branch
        }
        char save = board[r][c];
        board[r][c] = '#';
        dfs(board, r + 1, c, child);
        dfs(board, r - 1, c, child);
        dfs(board, r, c + 1, child);
        dfs(board, r, c - 1, child);
        board[r][c] = save;
        if (child->refs <= 0) {                 // no words left below → prune
            freeNode(child);
            n->children[k] = nullptr;           // cut the dead branch
        }
    }

public:
    /* Purpose : Find all words spellable on the board, pruning spent
     *           trie branches so later cells skip them.
     * Inputs  : board — m×n grid of letters; words — search list.
     * Output  : every word in `words` found on the board. */
    std::vector<std::string> findWords(std::vector<std::vector<char>>& board,
                                       const std::vector<std::string>& words) {
        root = new TrieNode();
        for (const std::string& w : words) insertWord(root, w);
        found.clear();
        rows = static_cast<int>(board.size());
        cols = rows ? static_cast<int>(board[0].size()) : 0;
        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                dfs(board, r, c, root);
            }
        }
        std::vector<std::string> result = found;
        freeNode(root);
        return result;
    }
};

/* =====================================================================
 * BENCHMARK — run both approaches on 3 boards, compare time + RAM
 * ===================================================================== */
template <typename Solver>
bool bench(const std::string& label,
           const std::vector<std::vector<std::vector<char>>>& boards,
           const std::vector<std::vector<std::string>>& wordLists,
           const std::vector<std::vector<std::string>>& expected) {
    bool allOk = true;
    for (size_t t = 0; t < boards.size(); ++t) {
        std::vector<std::vector<char>> board = boards[t]; // fresh copy: '#'
        struct rusage before, after;
        getrusage(RUSAGE_SELF, &before);
        auto start = std::chrono::high_resolution_clock::now();
        std::vector<std::string> got = Solver().findWords(board, wordLists[t]);
        auto end = std::chrono::high_resolution_clock::now();
        getrusage(RUSAGE_SELF, &after);

        double us = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start).count() / 1000.0;
        long memKb = after.ru_maxrss - before.ru_maxrss; // ru_maxrss is in KB

        // Order-free comparison: same size, every expected word present.
        bool ok = got.size() == expected[t].size();
        for (const std::string& w : expected[t]) {
            if (!contains(got, w)) { ok = false; break; }
        }
        allOk = allOk && ok;
        std::cout << label << " | test " << (t + 1) << " : "
                  << (ok ? "PASS" : "FAIL")
                  << "  found " << got.size() << " word(s)  time = " << us
                  << " µs  peak-ram-delta = " << memKb << " KB\n";
    }
    return allOk;
}

int main() {
    // Board 1: the official example → oath, eat.
    const std::vector<std::vector<char>> b1 = {
        {'o', 'a', 'a', 'n'}, {'e', 't', 'a', 'e'},
        {'i', 'h', 'k', 'r'}, {'i', 'f', 'l', 'v'}};
    // Board 2: every word is a short diagonal path.
    const std::vector<std::vector<char>> b2 = {
        {'a', 'b'}, {'c', 'd'}};
    // Board 3: single-cell board — only "a" is findable.
    const std::vector<std::vector<char>> b3 = {{'a'}};

    const std::vector<std::vector<std::vector<char>>> boards = {b1, b2, b3};
    const std::vector<std::vector<std::string>> wordLists = {
        {"oath", "pea", "eat", "rain"},
        {"ab", "cb", "ad", "abcd", "ac", "bd"},
        {"a", "b", "aa", "abc"}};
    // Only ADJACENT cells count: on the 2×2 board ab (right), ac (down)
    // and bd (down) are findable; cb/ad are diagonal and cannot be built.
    const std::vector<std::vector<std::string>> expected = {
        {"oath", "eat"},
        {"ab", "ac", "bd"},
        {"a"}};

    bool ok1 = bench<Solution_One>("Approach 1 (DFS basic)     ", boards, wordLists, expected);
    bool ok2 = bench<Solution_Two>("Approach 2 (DFS + pruning) ", boards, wordLists, expected);

    std::cout << (ok1 && ok2
        ? "PASS : both approaches find exactly the expected words on every board."
        : "FAIL : at least one answer was wrong.") << "\n";
    return 0;
}
