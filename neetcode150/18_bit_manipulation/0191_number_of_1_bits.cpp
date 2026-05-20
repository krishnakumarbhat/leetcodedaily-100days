#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    uint32_t n = 11;
    auto t=chrono::high_resolution_clock::now();
    int res = 0; while(n){ n &= (n - 1); res++; }
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
