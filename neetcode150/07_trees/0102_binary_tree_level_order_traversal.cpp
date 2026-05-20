/* LeetCode 102: Binary Tree Level Order Traversal - Medium */
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

class Solution { public: vector<vector<int>> levelOrder(TreeNode* root) { vector<vector<int>> res; if(!root) return res; queue<TreeNode*> q; q.push(root); while(!q.empty()){ int sz=q.size(); vector<int> lv; for(int i=0;i<sz;i++){ auto n=q.front();q.pop();lv.push_back(n->val); if(n->left)q.push(n->left); if(n->right)q.push(n->right); } res.push_back(lv); } return res; } };
int main(){ auto r=build({3,9,20,-1,-1,15,7}); auto s=chrono::high_resolution_clock::now(); auto res=Solution().levelOrder(r); auto e=chrono::high_resolution_clock::now(); cout<<"var1: levels="<<res.size()<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
