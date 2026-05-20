/* LeetCode 1448: Count Good Nodes - Medium */
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

class Solution { int dfs(TreeNode* n, int mx){ if(!n) return 0; int r=(n->val>=mx)?1:0; mx=max(mx,n->val); return r+dfs(n->left,mx)+dfs(n->right,mx); }
public: int goodNodes(TreeNode* r){ return dfs(r,r->val); } };
int main(){ auto r=build({3,1,4,3,-1,1,5}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().goodNodes(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
