#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 621: Task Scheduler - Medium */
// var1: Math formula
int v1(vector<char>& tasks, int n) {
    int cnt[26]={};
    for(char c:tasks) cnt[c-'A']++;
    sort(cnt,cnt+26,greater<int>());
    int mx=cnt[0], idle=(mx-1)*n;
    for(int i=1;i<26;i++) idle-=min(cnt[i],mx-1);
    return max((int)tasks.size(),(int)tasks.size()+idle);
}
// var2: max-count formula
int v2(vector<char>& tasks, int n) {
    int cnt[26]={};
    for(char c:tasks) cnt[c-'A']++;
    int mx=*max_element(cnt,cnt+26);
    int mx_cnt=count(cnt,cnt+26,mx);
    return max((int)tasks.size(),(mx-1)*(n+1)+mx_cnt);
}
int main(){
    vector<char> tasks={'A','A','A','B','B','B'};
    auto t1=chrono::high_resolution_clock::now(); cout<<"var1: "<<v1(tasks,2)<<endl;
    auto t2=chrono::high_resolution_clock::now(); cout<<"v1 time="<<chrono::duration_cast<chrono::nanoseconds>(t2-t1).count()/1000.0<<"us"<<endl;
    auto t3=chrono::high_resolution_clock::now(); cout<<"var2: "<<v2(tasks,2)<<endl;
    auto t4=chrono::high_resolution_clock::now(); cout<<"v2 time="<<chrono::duration_cast<chrono::nanoseconds>(t4-t3).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
// var2 mem = {} and time = {}
