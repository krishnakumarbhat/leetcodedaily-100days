/* LeetCode 19: Remove Nth Node From End - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode d(0); d.next=head; auto fast=&d, slow=&d;
        for(int i=0;i<=n;i++) fast=fast->next;
        while(fast){fast=fast->next;slow=slow->next;}
        slow->next=slow->next->next;
        return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto h=build({1,2,3,4,5});
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().removeNthFromEnd(h,2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
