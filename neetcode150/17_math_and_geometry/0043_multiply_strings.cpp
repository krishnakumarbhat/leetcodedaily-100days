#include <bits/stdc++.h>
#include <chrono>
using namespace std;
int main(){
    string num1 = "123", num2 = "456";
    auto t=chrono::high_resolution_clock::now();
    if(num1 == "0" || num2 == "0") { cout<<"var1: 0"<<endl; return 0; }
    vector<int> res(num1.size() + num2.size(), 0);
    reverse(num1.begin(), num1.end()); reverse(num2.begin(), num2.end());
    for(int i=0; i<num1.size(); i++){
        for(int j=0; j<num2.size(); j++){
            int digit = (num1[i] - '0') * (num2[j] - '0');
            res[i + j] += digit;
            res[i + j + 1] += res[i + j] / 10;
            res[i + j] %= 10;
        }
    }
    reverse(res.begin(), res.end());
    int beg = 0; while(beg < res.size() && res[beg] == 0) beg++;
    string ans = ""; for(; beg < res.size(); beg++) ans += to_string(res[beg]);
    cout<<"var1: "<<ans<<endl;
    auto e=chrono::high_resolution_clock::now();
    cout<<"var1 time="<<chrono::duration_cast<chrono::nanoseconds>(e-t).count()/1000.0<<"us"<<endl;
}
// var1 mem = {} and time = {}
