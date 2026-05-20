/* LeetCode 981: Time Based Key-Value Store - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
// ============= Variation 1: Binary Search =============
// Algorithm: Uses an unordered_map to store vectors of pairs. Retrieves values
// using manual binary search on descending timestamp matches.
// Time: O(log n) per get  Space: O(n)
class TimeMap {
    unordered_map<string, vector<pair<int,string>>> store;
public:
    void set(string key, string value, int timestamp) { store[key].push_back({timestamp, value}); }
    string get(string key, int timestamp) {
        auto& vals = store[key];
        int l=0, r=vals.size()-1; string res="";
        while(l<=r){ int m=(l+r)/2; if(vals[m].first<=timestamp){res=vals[m].second;l=m+1;} else r=m-1; }
        return res;
    }
};
int main(){
    auto s=chrono::high_resolution_clock::now();
    TimeMap tm; tm.set("foo","bar",1); tm.set("foo","bar2",4);
    cout<<tm.get("foo",1)<<" "<<tm.get("foo",3)<<" "<<tm.get("foo",5)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 (BS): "<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = N/A and time = N/A
