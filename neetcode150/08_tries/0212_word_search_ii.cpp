#include <bits/stdc++.h>
#include <chrono>
using namespace std;

/* LeetCode 212: Word Search II - Hard */

struct TrieNode {
    unordered_map<char,TrieNode*> ch;
    string word;
    int refs = 0;
};

// var1: Trie + DFS backtracking
class Solution_v1 {
    void dfs(vector<vector<char>>& b, int r, int c, TrieNode* n, vector<string>& res) {
        if (r<0||r>=(int)b.size()||c<0||c>=(int)b[0].size()||b[r][c]=='#') return;
        char ch = b[r][c];
        if (!n->ch.count(ch)) return;
        n = n->ch[ch];
        if (!n->word.empty()) { res.push_back(n->word); n->word = ""; }
        b[r][c] = '#';
        dfs(b,r+1,c,n,res); dfs(b,r-1,c,n,res); dfs(b,r,c+1,n,res); dfs(b,r,c-1,n,res);
        b[r][c] = ch;
    }
public:
    vector<string> findWords(vector<vector<char>>& b, vector<string>& words) {
        auto root = new TrieNode();
        for (auto& s : words) { auto n=root; for(char c:s){ if(!n->ch[c]) n->ch[c]=new TrieNode(); n=n->ch[c]; } n->word=s; }
        vector<string> res;
        for (int r=0; r<(int)b.size(); r++) for (int c=0; c<(int)b[0].size(); c++) dfs(b,r,c,root,res);
        return res;
    }
};

int main() {
    vector<vector<char>> board = {{'o','a','a','n'},{'e','t','a','e'},{'i','h','k','r'},{'i','f','l','v'}};
    vector<string> words = {"oath","pea","eat","rain"};
    auto s1 = chrono::high_resolution_clock::now();
    auto res = Solution_v1().findWords(board, words);
    auto e1 = chrono::high_resolution_clock::now();
    cout << "var1: found=" << res.size() << " words" << endl;
    cout << "var1 time=" << chrono::duration_cast<chrono::nanoseconds>(e1-s1).count()/1000.0 << "us" << endl;
    return 0;
}
// var1 mem = {} and time = {}
