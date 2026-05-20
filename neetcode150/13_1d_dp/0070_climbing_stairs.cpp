#include <bits/stdc++.h>
#include <chrono>
using namespace std;
/* LeetCode 70: Climbing Stairs - Easy */
int main(){
    int n=10;
    auto s=chrono::high_resolution_clock::now();
    int a=1,b=2;
    for(int i=3;i<=n;i++){int c=a+b;a=b;b=c;}
    cout<<"var1: "<<b<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-s).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
