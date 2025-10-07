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

    uniform_int_distribution<ll> ranN, ranXi ,prob;

    if(z <= 3){
        ranN.param(uniform_int_distribution<ll>::param_type(3, ll(1e4)));
        ranXi.param(uniform_int_distribution<ll>::param_type(1, ll(1e4)));

        ll n = ranN(gen);
        fout << n << endll;
        forr(i,0,n){
            fout << ranXi(gen) << sp;
        }
    }else{
        ranN.param(uniform_int_distribution<ll>::param_type(ll(3e6), ll(5e6)));
        ranXi.param(uniform_int_distribution<ll>::param_type(ll(1e5), ll(1e6)));
        prob.param(uniform_int_distribution<ll>::param_type(1,100));
        if(z<=5){
            ll n = ranN(gen);
            fout << n << endll;
            forr(i,0,n){
                if(prob(gen)>=99)fout << ranXi(gen) << sp;
                else fout << ll(1e6+1) << sp;
            }
        }else if(z<=8){
            ll n = ranN(gen);
            fout << n << endll;
            forr(i,0,n){
                if(i<=n/2)fout << i << sp;
                else fout << ll(1e6)-i << sp;
            }
        }else if(z<=10){
            ll n = ranN(gen);
            fout << n << endll;
            forr(i,0,n){
                if(prob(gen)>=99)fout << ranXi(gen) << sp;
                else fout << i+1 << sp;
            }
        }
    }

    

}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}