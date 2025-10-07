#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

void solve(string in,int z){
    cout << in << '\n';

    ofstream fout;
    fout.open(in);

    random_device rd;
    mt19937 gen(rd());

    uniform_int_distribution<ll> ran;

    if(z <= 2){
        ran.param(uniform_int_distribution<ll>::param_type(20, ll(1e2)));
    }else if(z <= 4){
        ran.param(uniform_int_distribution<ll>::param_type(ll(8e3), ll(1e6)));
    }else{
        ran.param(uniform_int_distribution<ll>::param_type(ll(4e10), ll(1e12)));
    }

    fout << ran(gen) << sp << ran(gen) << endll;
}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("testcases/input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}