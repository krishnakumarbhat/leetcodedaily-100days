/* LeetCode 138: Copy List with Random Pointer - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct Node { int val; Node* next; Node* random; Node(int x):val(x),next(nullptr),random(nullptr){} };
class Solution_v1 {
public:
    Node* copyRandomList(Node* head) {
        if(!head) return nullptr;
        unordered_map<Node*,Node*> mp;
        auto cur=head; while(cur){mp[cur]=new Node(cur->val);cur=cur->next;}
        cur=head; while(cur){mp[cur]->next=mp[cur->next];mp[cur]->random=mp[cur->random];cur=cur->next;}
        return mp[head];
    }
};
int main(){
    auto n1=new Node(7), n2=new Node(13), n3=new Node(11);
    n1->next=n2; n2->next=n3; n2->random=n1; n3->random=n1;
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().copyRandomList(n1); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
