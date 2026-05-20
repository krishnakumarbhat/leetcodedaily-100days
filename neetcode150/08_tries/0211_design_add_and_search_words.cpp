#include <bits/stdc++.h>
#include <chrono>
using namespace std;

/* LeetCode 211: Add and Search Words Data Structure - Medium */

struct TrieNode {
    unordered_map<char,TrieNode*> ch;
    bool end = false;
};

// var1: DFS recursive wildcard
class WordDictionary_v1 {
    TrieNode* root;
    bool dfs(TrieNode* n, const string& w, int i) {
        if (i == (int)w.size()) return n->end;
        if (w[i] == '.') {
            for (auto& [c,child] : n->ch) if (dfs(child, w, i+1)) return true;
            return false;
        }
        if (!n->ch.count(w[i])) return false;
        return dfs(n->ch[w[i]], w, i+1);
    }
public:
    WordDictionary_v1() : root(new TrieNode()) {}
    void addWord(string w) { auto n=root; for(char c:w){ if(!n->ch[c]) n->ch[c]=new TrieNode(); n=n->ch[c]; } n->end=true; }
    bool search(string w) { return dfs(root, w, 0); }
};

int main() {
    vector<string> add_words = {"bad","dad","mad","pad"};
    vector<string> search_words = {".ad","b..","ba.","pad","bad","xyz"};

    auto s1 = chrono::high_resolution_clock::now();
    WordDictionary_v1 wd;
    for (auto& w : add_words) wd.addWord(w);
    for (auto& s : search_words) cout << s << ":" << wd.search(s) << " ";
    cout << endl;
    auto e1 = chrono::high_resolution_clock::now();
    cout << "var1 time=" << chrono::duration_cast<chrono::nanoseconds>(e1-s1).count()/1000.0 << "us" << endl;
    return 0;
}
// var1 mem = {} and time = {}
