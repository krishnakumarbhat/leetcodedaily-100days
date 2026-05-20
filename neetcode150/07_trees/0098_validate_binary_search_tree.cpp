/* LeetCode 98: Validate BST - Medium */
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

class Solution { bool valid(TreeNode* n, long lo, long hi){ if(!n) return true; if(n->val<=lo||n->val>=hi) return false; return valid(n->left,lo,n->val)&&valid(n->right,n->val,hi); }
public: bool isValidBST(TreeNode* r){ return valid(r,LONG_MIN,LONG_MAX); } };
int main(){ auto r=build({2,1,3}); auto s=chrono::high_resolution_clock::now(); cout<<Solution().isValidBST(r); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
