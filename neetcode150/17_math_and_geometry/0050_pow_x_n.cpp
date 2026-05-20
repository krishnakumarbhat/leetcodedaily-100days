#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    double x = 2.0; long long n = 10;
    auto t=chrono::high_resolution_clock::now();
    if(n < 0){ x = 1 / x; n = -n; }
    double res = 1;
    while(n){ if(n % 2) res *= x; x *= x; n /= 2; }
    cout<<"var1: "<<res<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
