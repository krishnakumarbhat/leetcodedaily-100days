/* LeetCode 572: Subtree of Another Tree - Easy */
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

class Solution { bool same(TreeNode*p,TreeNode*q){ if(!p&&!q) return true; if(!p||!q||p->val!=q->val) return false; return same(p->left,q->left)&&same(p->right,q->right); }
public: bool isSubtree(TreeNode*r,TreeNode*s){ if(!r) return false; if(same(r,s)) return true; return isSubtree(r->left,s)||isSubtree(r->right,s); } };
int main(){ auto s=chrono::high_resolution_clock::now(); cout<<Solution().isSubtree(build({3,4,5,1,2}),build({4,1,2})); auto e=chrono::high_resolution_clock::now(); cout<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
