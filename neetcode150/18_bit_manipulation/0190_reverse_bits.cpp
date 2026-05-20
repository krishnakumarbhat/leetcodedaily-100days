#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    uint32_t n = 43261596;
    auto t=chrono::high_resolution_clock::now();
    uint32_t res = 0;
    for(int i=0; i<32; i++){
        uint32_t bit = (n >> i) & 1;
        res = res | (bit << (31 - i));
    }
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
