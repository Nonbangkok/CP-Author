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

    uniform_int_distribution<ll> ranT, ranD, ranV;
    uniform_int_distribution<ll> prob(1,100);

    if(z<=2){
        ranT.param(uniform_int_distribution<ll>::param_type(10, ll(1e2)));
        ranD.param(uniform_int_distribution<ll>::param_type(3, ll(1e2)));
        ranV.param(uniform_int_distribution<ll>::param_type(3, ll(1e2)));
    }else if(z<=4){
        ranT.param(uniform_int_distribution<ll>::param_type(ll(1e2), ll(1e3)));
        ranD.param(uniform_int_distribution<ll>::param_type(ll(1e5), ll(1e9)));
        ranV.param(uniform_int_distribution<ll>::param_type(ll(1e3), ll(1e5)));
    }else{
        ranT.param(uniform_int_distribution<ll>::param_type(ll(1e4), ll(1e5)));
        ranD.param(uniform_int_distribution<ll>::param_type(ll(1e11), ll(1e18)));
        ranV.param(uniform_int_distribution<ll>::param_type(ll(1e8), ll(1e12)));
    }

    ll t = ranT(gen);
    fout << t << endll;
    forr(i,0,t){
        fout << ranD(gen) << sp << ranD(gen) << sp;
        ll a = ranV(gen), b = ranV(gen);
        if(prob(gen)>50)fout << min(a,b) << sp << max(a,b);
        else fout << max(a,b) << sp << min(a,b);
        fout << endll;
    }

}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}