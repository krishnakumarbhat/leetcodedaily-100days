/* LeetCode 100: Same Tree - Easy */
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

class Solution { public: bool isSameTree(TreeNode* p, TreeNode* q) { if(!p&&!q) return true; if(!p||!q||p->val!=q->val) return false; return isSameTree(p->left,q->left)&&isSameTree(p->right,q->right); } };
int main(){ auto s=chrono::high_resolution_clock::now(); cout<<Solution().isSameTree(build({1,2,3}),build({1,2,3})); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
