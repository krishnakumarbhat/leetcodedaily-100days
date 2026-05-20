/* LeetCode 124: Binary Tree Maximum Path Sum - Hard */
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

class Solution { int res=INT_MIN; int dfs(TreeNode* n){ if(!n) return 0; int l=max(dfs(n->left),0),r=max(dfs(n->right),0); res=max(res,n->val+l+r); return n->val+max(l,r); }
public: int maxPathSum(TreeNode* r){ res=INT_MIN; dfs(r); return res; } };
int main(){ auto r=build({1,2,3}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().maxPathSum(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
