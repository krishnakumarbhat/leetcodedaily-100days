/* LeetCode 2: Add Two Numbers - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode d(0); auto c=&d; int carry=0;
        while(l1||l2||carry){
            int s=(l1?l1->val:0)+(l2?l2->val:0)+carry;
            carry=s/10; c->next=new ListNode(s%10); c=c->next;
            if(l1) l1=l1->next; if(l2) l2=l2->next;
        }
        return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().addTwoNumbers(build({2,4,3}),build({5,6,4})); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
