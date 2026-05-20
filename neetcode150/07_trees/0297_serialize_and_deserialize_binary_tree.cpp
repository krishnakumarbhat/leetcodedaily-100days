/* LeetCode 297: Serialize and Deserialize Binary Tree - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int x):val(x),left(nullptr),right(nullptr){} };
TreeNode* build(vector<int> v) {
    if(v.empty()) return nullptr;
    auto root=new TreeNode(v[0]); queue<TreeNode*> q; q.push(root);
    for(int i=1;i<v.size();i+=2){
        auto n=q.front(); q.pop();
        if(i<v.size()&&v[i]!=-1){n->left=new TreeNode(v[i]);q.push(n->left);}
        if(i+1<v.size()&&v[i+1]!=-1){n->right=new TreeNode(v[i+1]);q.push(n->right);}
    }
    return root;
}

class Codec {
public:
    string serialize(TreeNode* root) { if(!root) return "N"; return to_string(root->val)+","+serialize(root->left)+","+serialize(root->right); }
    TreeNode* deserialize(string data) { istringstream ss(data); return dfs(ss); }
    TreeNode* dfs(istringstream& ss) { string v; getline(ss,v,','); if(v=="N") return nullptr; auto n=new TreeNode(stoi(v)); n->left=dfs(ss); n->right=dfs(ss); return n; }
};
int main(){ auto r=build({1,2,3,-1,-1,4,5}); Codec c; auto s=chrono::high_resolution_clock::now(); auto ser=c.serialize(r); c.deserialize(ser); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
