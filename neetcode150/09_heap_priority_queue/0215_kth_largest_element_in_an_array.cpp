#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 215: Kth Largest Element in an Array - Medium */
// var1: sort
int v1(vector<int> n, int k){ sort(n.rbegin(),n.rend()); return n[k-1]; }
// var2: min-heap
int v2(vector<int>& n, int k){ priority_queue<int,vector<int>,greater<int>> pq; for(int x:n){pq.push(x);if((int)pq.size()>k)pq.pop();} return pq.top(); }
// var3: nth_element (QuickSelect in STL)
int v3(vector<int> n, int k){ nth_element(n.begin(),n.begin()+n.size()-k,n.end()); return n[n.size()-k]; }
int main(){
    vector<int> nums={3,2,1,5,6,4};
    auto t1=chrono::high_resolution_clock::now(); cout<<"var1: "<<v1(nums,2)<<endl;
    auto t2=chrono::high_resolution_clock::now(); cout<<"v1 time="<<chrono::duration_cast<chrono::nanoseconds>(t2-t1).count()/1000.0<<"us"<<endl;
    auto t3=chrono::high_resolution_clock::now(); cout<<"var2: "<<v2(nums,2)<<endl;
    auto t4=chrono::high_resolution_clock::now(); cout<<"v2 time="<<chrono::duration_cast<chrono::nanoseconds>(t4-t3).count()/1000.0<<"us"<<endl;
    auto t5=chrono::high_resolution_clock::now(); cout<<"var3: "<<v3(nums,2)<<endl;
    auto t6=chrono::high_resolution_clock::now(); cout<<"v3 time="<<chrono::duration_cast<chrono::nanoseconds>(t6-t5).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
// var3 mem = {} and time = {}
