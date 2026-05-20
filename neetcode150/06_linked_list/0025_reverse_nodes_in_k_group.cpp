/* LeetCode 25: Reverse Nodes in k-Group - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode d(0); d.next=head; auto gp=&d;
        while(true){
            auto kth=gp;
            for(int i=0;i<k;i++){kth=kth->next;if(!kth) return d.next;}
            auto gn=kth->next; auto prev=gn; auto cur=gp->next;
            while(cur!=gn){auto n=cur->next;cur->next=prev;prev=cur;cur=n;}
            auto tmp=gp->next; gp->next=kth; gp=tmp;
        }
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    auto h=build({1,2,3,4,5});
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().reverseKGroup(h,2); auto e=chrono::high_resolution_clock::now();
    cout<<"var1: "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
