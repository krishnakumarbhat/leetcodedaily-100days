/* LeetCode 143: Reorder List - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    void reorderList(ListNode* head) {
        if(!head||!head->next) return;
        auto slow=head, fast=head;
        while(fast->next&&fast->next->next){slow=slow->next;fast=fast->next;}
        ListNode *prev=nullptr, *cur=slow->next; slow->next=nullptr;
        while(cur){auto n=cur->next;cur->next=prev;prev=cur;cur=n;}
        auto f=head, s=prev;
        while(s){auto t1=f->next,t2=s->next;f->next=s;s->next=t1;f=t1;s=t2;}
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto h=build({1,2,3,4,5});
    auto s=chrono::high_resolution_clock::now(); Solution_v1().reorderList(h); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
