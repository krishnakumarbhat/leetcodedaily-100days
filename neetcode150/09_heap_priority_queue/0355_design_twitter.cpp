#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 355: Design Twitter - Medium */
class Twitter {
    int ts=0;
    unordered_map<int,vector<pair<int,int>>> tweets; // user->(ts,tid)
    unordered_map<int,unordered_set<int>> following;
public:
    void postTweet(int u, int t){ tweets[u].push_back({ts++,t}); }
    vector<int> getNewsFeed(int u){
        auto cmp=[](pair<int,int>& a,pair<int,int>& b){ return a.first<b.first; };
        priority_queue<pair<int,int>,vector<pair<int,int>>,decltype(cmp)> pq(cmp);
        auto users=following[u]; users.insert(u);
        for(int fu:users) for(auto& t:tweets[fu]) pq.push(t);
        vector<int> res;
        for(int i=0;i<10&&!pq.empty();i++){ res.push_back(pq.top().second); pq.pop(); }
        return res;
    }
    void follow(int a, int b){ following[a].insert(b); }
    void unfollow(int a, int b){ following[a].erase(b); }
};
int main(){
    auto s=chrono::high_resolution_clock::now();
    Twitter tw; tw.postTweet(1,5); tw.postTweet(1,3);
    tw.follow(1,2); tw.postTweet(2,6);
    auto f=tw.getNewsFeed(1);
    cout<<"var1 feed size="<<f.size()<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
