/* LeetCode 23: Merge k Sorted Lists - Hard */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
struct ListNode { int val; ListNode* next; ListNode(int x):val(x),next(nullptr){} };
class Solution_v1 {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp=[](ListNode* a, ListNode* b){return a->val>b->val;};
        priority_queue<ListNode*,vector<ListNode*>,decltype(cmp)> pq(cmp);
        for(auto l:lists) if(l) pq.push(l);
        ListNode d(0); auto c=&d;
        while(!pq.empty()){ auto n=pq.top(); pq.pop(); c->next=n; c=c->next; if(n->next) pq.push(n->next); }
        return d.next;
    }
};
int main(){
    auto build=[](vector<int> v){ ListNode* d=new ListNode(0); auto c=d; for(int x:v){c->next=new ListNode(x);c=c->next;} return d->next; };
    vector<ListNode*> lists={build({1,4,5}),build({1,3,4}),build({2,6})};
    auto s=chrono::high_resolution_clock::now(); auto r=Solution_v1().mergeKLists(lists); auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (Heap): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
