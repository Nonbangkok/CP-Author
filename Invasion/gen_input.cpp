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

    uniform_int_distribution<ll> ranN, ranK, ranX;

    if(z<=2){
        ranN.param(uniform_int_distribution<ll>::param_type(10, ll(50)));
        ranK.param(uniform_int_distribution<ll>::param_type(1,1));
        ranX.param(uniform_int_distribution<ll>::param_type(3, ll(1e2)));
    }else if(z<=4){
        ranN.param(uniform_int_distribution<ll>::param_type(60, ll(100)));
        ranK.param(uniform_int_distribution<ll>::param_type(2,10));
        ranX.param(uniform_int_distribution<ll>::param_type(100, 500));
    }else if(z<=6){
        ranN.param(uniform_int_distribution<ll>::param_type(ll(5e2), ll(1e3)));
        ranK.param(uniform_int_distribution<ll>::param_type(4, ll(1e2)));
        ranX.param(uniform_int_distribution<ll>::param_type(ll(1e3), ll(1e6)));
    }else{
        ranN.param(uniform_int_distribution<ll>::param_type(ll(1e4), ll(1e5)));
        ranK.param(uniform_int_distribution<ll>::param_type(5, ll(1e2)));
        ranX.param(uniform_int_distribution<ll>::param_type(ll(5e6), ll(1e9)));
    }

    ll n = ranN(gen);
    fout << n << sp << ranK(gen) << endll;
    ll x = ranX(gen);
    forr(i,0,n){
        if(z==3 || z==4){
            fout << x << sp;
        }else{
            fout << ranX(gen) << sp;
        }
    }
}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}