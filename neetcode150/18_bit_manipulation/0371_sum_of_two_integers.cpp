#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    int a = 1, b = 2;
    auto t=chrono::high_resolution_clock::now();
    while(b != 0){
        int tmp = (a & b) << 1;
        a = a ^ b;
        b = tmp;
    }
    cout<<"var1: "<<a<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
