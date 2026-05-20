#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string s="(*)";
    auto t=chrono::high_resolution_clock::now();
    int lo=0,hi=0;
    for(char c:s){if(c=='('){lo++;hi++;}else if(c==')'){lo--;hi--;}else{lo--;hi++;}if(hi<0){cout<<"var1: false"<<endl;return 0;}lo=max(lo,0);}
    cout<<"var1: "<<(lo==0)<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
