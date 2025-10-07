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

    uniform_int_distribution<ll> ranN, ranM, ranPi;

    if(z <= 2){
        ranN.param(uniform_int_distribution<ll>::param_type(20, ll(1e2)));
        ranM.param(uniform_int_distribution<ll>::param_type(ll(1e4), ll(2e4)));
        ranPi.param(uniform_int_distribution<ll>::param_type(1, ll(1e3)));
    }else if(z <= 4){
        ranN.param(uniform_int_distribution<ll>::param_type(ll(8e3), ll(1e4)));
        ranM.param(uniform_int_distribution<ll>::param_type(ll(5e10), ll(5e11)));
        ranPi.param(uniform_int_distribution<ll>::param_type(ll(5e7 + 10), ll(1e8)));
    }else{
        ranN.param(uniform_int_distribution<ll>::param_type(ll(4e5), ll(5e5)));
        ranM.param(uniform_int_distribution<ll>::param_type(ll(1e13), ll(5e13)));
        ranPi.param(uniform_int_distribution<ll>::param_type(ll(1), ll(5e8)));
    }

    ll n,m;
    ll A[int(5e5+10)];
    while(1){
        n = ranN(gen), m = ranM(gen);
        forr(i,1,n+1){
            A[i] = ranPi(gen);
        }
        ll l=1,mx=0,sum=0;
        bool same = false;
        forr(r,1,n+1){
            sum += A[r];
            while(sum>m)sum -= A[l++];
            if(mx==r-l+1)same = true;
            if(mx<r-l+1)mx=r-l+1,same = false;
        }
        if(!same)break;
    }

    fout << n << sp << m << endll;
    forr(i,1,n+1)fout << A[i] << sp;
}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}