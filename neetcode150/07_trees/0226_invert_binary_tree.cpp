/* LeetCode 226: Invert Binary Tree - Easy */
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

class Solution_v1 {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(!root) return nullptr;
        swap(root->left, root->right);
        invertTree(root->left); invertTree(root->right);
        return root;
    }
};
class Solution_v2 {
public:
    TreeNode* invertTree(TreeNode* root) {
        if(!root) return nullptr;
        queue<TreeNode*> q; q.push(root);
        while(!q.empty()){ auto n=q.front(); q.pop(); swap(n->left,n->right); if(n->left) q.push(n->left); if(n->right) q.push(n->right); }
        return root;
    }
};
int main(){
    auto r=build({4,2,7,1,3,6,9});
    auto s=chrono::high_resolution_clock::now(); Solution_v1().invertTree(r); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (DFS): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
