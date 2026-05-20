/* LeetCode 141: Linked List Cycle - Easy */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    bool hasCycle(ListNode* head) {
        auto slow=head, fast=head;
        while(fast&&fast->next){ slow=slow->next; fast=fast->next->next; if(slow==fast) return true; }
        return false;
    }
};
int main(){
    auto n1=new ListNode(3), n2=new ListNode(2), n3=new ListNode(0), n4=new ListNode(-4);
    n1->next=n2; n2->next=n3; n3->next=n4; n4->next=n2;
    auto s=chrono::high_resolution_clock::now(); bool r=Solution_v1().hasCycle(n1); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Floyd): "<<r<<", "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
