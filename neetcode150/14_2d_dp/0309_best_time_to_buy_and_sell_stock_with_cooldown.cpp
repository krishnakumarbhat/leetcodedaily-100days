#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    vector<int> p={1,2,3,0,2};
    auto t=chrono::high_resolution_clock::now();
    int hold=INT_MIN,sold=0,rest=0;
    for(int x:p){int h=max(hold,rest-x),s=hold+x,r=max(rest,sold);hold=h;sold=s;rest=r;}
    cout<<"var1: "<<max(sold,rest)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
