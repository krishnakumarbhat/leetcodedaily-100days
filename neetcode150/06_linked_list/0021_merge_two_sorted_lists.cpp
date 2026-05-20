/* LeetCode 21: Merge Two Sorted Lists - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode d(0); auto c=&d;
        while(l1&&l2){ if(l1->val<=l2->val){c->next=l1;l1=l1->next;} else{c->next=l2;l2=l2->next;} c=c->next; }
        c->next=l1?l1:l2; return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto l1=build({1,2,4}), l2=build({1,3,4});
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().mergeTwoLists(l1,l2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
