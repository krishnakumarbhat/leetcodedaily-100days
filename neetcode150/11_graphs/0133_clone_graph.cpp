#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 133: Clone Graph - Medium */
struct Node { int val; vector<Node*> neighbors; Node(int v):val(v){} };
// var1: DFS with map
unordered_map<Node*,Node*> mp;
Node* dfs(Node* n){ if(!n) return nullptr; if(mp.count(n)) return mp[n]; mp[n]=new Node(n->val); for(auto nb:n->neighbors) mp[n]->neighbors.push_back(dfs(nb)); return mp[n]; }
int main(){
    Node *n1=new Node(1),*n2=new Node(2),*n3=new Node(3),*n4=new Node(4);
    n1->neighbors={n2,n4}; n2->neighbors={n1,n3}; n3->neighbors={n2,n4}; n4->neighbors={n1,n3};
    auto s=chrono::high_resolution_clock::now();
    auto clone=dfs(n1); cout<<"var1: clone.val="<<clone->val<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
