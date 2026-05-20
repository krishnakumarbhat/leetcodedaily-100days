/* LeetCode 206: Reverse Linked List - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *prev=nullptr, *cur=head;
        while(cur){ auto nxt=cur->next; cur->next=prev; prev=cur; cur=nxt; }
        return prev;
    }
};
class Solution_v2 {
public:
    ListNode* reverseList(ListNode* head) {
        if(!head||!head->next) return head;
        auto nh=reverseList(head->next);
        head->next->next=head; head->next=nullptr;
        return nh;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    { auto h=build({1,2,3,4,5}); auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().reverseList(h); auto e=chrono::high_resolution_clock::now(); cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    { auto h=build({1,2,3,4,5}); auto s=chrono::high_resolution_clock::now(); auto r=Solution_v2().reverseList(h); auto e=chrono::high_resolution_clock::now(); cout<<"var2: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl; }
    return 0;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
