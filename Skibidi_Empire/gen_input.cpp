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

    uniform_int_distribution<ll> ranN, ranK;
    uniform_int_distribution<ll> prob(1,100);

    if(z<=2){
        ranN.param(uniform_int_distribution<ll>::param_type(1, ll(1e2)));
        ranK.param(uniform_int_distribution<ll>::param_type(3, ll(1e2)));
    }else if(z<=4){
        ranN.param(uniform_int_distribution<ll>::param_type(ll(1e2), ll(1e4)));
        ranK.param(uniform_int_distribution<ll>::param_type(ll(1e2), ll(1e3)));
    }else{
        ranN.param(uniform_int_distribution<ll>::param_type(ll(5e5), ll(2e6)));
        ranK.param(uniform_int_distribution<ll>::param_type(ll(1e4), ll(1e6)));
    }

    ll n = ranN(gen);
    fout << n << sp;
    ll k = LLONG_MAX;
    while(n<k)k = ranK(gen);
    fout << k << endll;
    forr(i,0,n)fout << (prob(gen)>75) << sp;

}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}