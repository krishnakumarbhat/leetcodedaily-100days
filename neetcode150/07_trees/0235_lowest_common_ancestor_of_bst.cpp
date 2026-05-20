/* LeetCode 235: LCA of BST - Medium */
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

class Solution { public: TreeNode* lowestCommonAncestor(TreeNode* r, TreeNode* p, TreeNode* q) { while(r){ if(p->val<r->val&&q->val<r->val) r=r->left; else if(p->val>r->val&&q->val>r->val) r=r->right; else return r; } return nullptr; } };
int main(){ auto r=build({6,2,8,0,4,7,9}); auto p=r->left; auto q=r->right; auto s=chrono::high_resolution_clock::now(); auto a=Solution().lowestCommonAncestor(r,p,q); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<a->val<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
