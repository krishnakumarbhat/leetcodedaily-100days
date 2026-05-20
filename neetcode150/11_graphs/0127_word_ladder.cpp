#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 127: Word Ladder - Hard */
int main(){
    string begin="hit",end_w="cog";
    unordered_set<string> ws={"hot","dot","dog","lot","log","cog"};
    auto s=chrono::high_resolution_clock::now();
    if(!ws.count(end_w)){cout<<"var1: 0"<<endl;return 0;}
    queue<pair<string,int>> q; q.push({begin,1});
    while(!q.empty()){
        auto[word,steps]=q.front();q.pop();
        for(int i=0;i<(int)word.size();i++){
            string nw=word;
            for(char c='a';c<='z';c++){
                nw[i]=c;
                if(nw==end_w){cout<<"var1: "<<steps+1<<endl; auto e=chrono::high_resolution_clock::now(); cout<<"v1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl; return 0;}
                if(ws.count(nw)){ws.erase(nw);q.push({nw,steps+1});}
            }
        }
    }
    cout<<"var1: 0"<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
