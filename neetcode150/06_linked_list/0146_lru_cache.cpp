/* LeetCode 146: LRU Cache - Medium */
#include <bits/stdc++.h>
#include <chrono>
using namespace std;
class LRUCache {
    int cap; list<pair<int,int>> dl; unordered_map<int,list<pair<int,int>>::iterator> mp;
public:
    LRUCache(int capacity):cap(capacity){}
    int get(int key){
        if(!mp.count(key)) return -1;
        dl.splice(dl.end(),dl,mp[key]); return mp[key]->second;
    }
    void put(int key, int value){
        if(mp.count(key)){mp[key]->second=value;dl.splice(dl.end(),dl,mp[key]);return;}
        if((int)dl.size()==cap){auto f=dl.front();mp.erase(f.first);dl.pop_front();}
        dl.push_back({key,value}); mp[key]=prev(dl.end());
    }
};
int main(){
    auto s=chrono::high_resolution_clock::now();
    LRUCache c(2); c.put(1,1); c.put(2,2); cout<<c.get(1)<<" "; c.put(3,3); cout<<c.get(2)<<" ";
    auto e=chrono::high_resolution_clock::now();
    cout<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<" us"<<endl;
    return 0;
}
// var1 mem = {} and time = {}
