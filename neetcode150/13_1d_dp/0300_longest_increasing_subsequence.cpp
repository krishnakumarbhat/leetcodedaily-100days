#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 300: LIS - Medium */
int main(){
    vector<int> nums={10,9,2,5,3,7,101,18};
    auto t=chrono::high_resolution_clock::now();
    // Patience sort O(n log n)
    vector<int> tails;
    for(int x:nums){ auto it=lower_bound(tails.begin(),tails.end(),x); if(it==tails.end()) tails.push_back(x); else *it=x; }
    cout<<"var1 (patience): "<<tails.size()<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
