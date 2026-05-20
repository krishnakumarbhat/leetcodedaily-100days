/* LeetCode 105: Build Tree from Preorder & Inorder - Medium */
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

class Solution { unordered_map<int,int> mp; int idx=0;
    TreeNode* helper(vector<int>& pre, int l, int r){ if(l>r) return nullptr; int val=pre[idx++]; auto n=new TreeNode(val); n->left=helper(pre,l,mp[val]-1); n->right=helper(pre,mp[val]+1,r); return n; }
public: TreeNode* buildTree(vector<int>& pre, vector<int>& in){ for(int i=0;i<in.size();i++) mp[in[i]]=i; idx=0; return helper(pre,0,in.size()-1); } };
int main(){ vector<int> pre={3,9,20,15,7},in={9,3,15,20,7}; auto s=chrono::high_resolution_clock::now(); Solution().buildTree(pre,in); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
// var1 mem = {} and time = {}
