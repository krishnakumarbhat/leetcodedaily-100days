#include <bits/stdc++.h>
#include <chrono>
using namespace std;

/* LeetCode 208: Implement Trie - Medium */

// Variation 1: unordered_map based
struct TrieNode_v1 {
    unordered_map<char, TrieNode_v1*> ch;
    bool end = false;
};
class Trie_v1 {
    TrieNode_v1* root;
public:
    Trie_v1() : root(new TrieNode_v1()) {}
    void insert(string w) { auto n=root; for(char c:w){ if(!n->ch[c]) n->ch[c]=new TrieNode_v1(); n=n->ch[c]; } n->end=true; }
    bool search(string w) { auto n=root; for(char c:w){ if(!n->ch.count(c)) return false; n=n->ch[c]; } return n->end; }
    bool startsWith(string p) { auto n=root; for(char c:p){ if(!n->ch.count(c)) return false; n=n->ch[c]; } return true; }
};

// Variation 2: array[26] based (faster for lowercase)
struct TrieNode_v2 {
    TrieNode_v2* ch[26] = {};
    bool end = false;
};
class Trie_v2 {
    TrieNode_v2* root;
public:
    Trie_v2() : root(new TrieNode_v2()) {}
    void insert(string w) { auto n=root; for(char c:w){ int i=c-'a'; if(!n->ch[i]) n->ch[i]=new TrieNode_v2(); n=n->ch[i]; } n->end=true; }
    bool search(string w) { auto n=root; for(char c:w){ int i=c-'a'; if(!n->ch[i]) return false; n=n->ch[i]; } return n->end; }
    bool startsWith(string p) { auto n=root; for(char c:p){ int i=c-'a'; if(!n->ch[i]) return false; n=n->ch[i]; } return true; }
};

int main() {
    vector<string> words = {"apple","app","application","apply","banana"};
    // var1
    auto s1 = chrono::high_resolution_clock::now();
    Trie_v1 t1; for(auto& w:words) t1.insert(w);
    cout<<"var1: "<<t1.search("apple")<<" "<<t1.search("app")<<" "<<t1.startsWith("app")<<endl;
    auto e1 = chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e1-s1).count()/1000.0<<"us"<<endl;
    // var2
    auto s2 = chrono::high_resolution_clock::now();
    Trie_v2 t2; for(auto& w:words) t2.insert(w);
    cout<<"var2: "<<t2.search("apple")<<" "<<t2.search("app")<<" "<<t2.startsWith("app")<<endl;
    auto e2 = chrono::high_resolution_clock::now();
    cout<<"var2 time="<<chrono::duration_cast<chrono::nanoseconds>(e2-s2).count()/1000.0<<"us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
