#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> n={-2,1,-3,4,-1,2,1,-5,4};
    auto t=chrono::high_resolution_clock::now();
    int cur=n[0],mx=n[0];
    for(int i=1;i<(int)n.size();i++){cur=max(n[i],cur+n[i]);mx=max(mx,cur);}
    cout<<"var1: "<<mx<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
