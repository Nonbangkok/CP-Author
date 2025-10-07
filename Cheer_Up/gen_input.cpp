#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

const int N = 2e6+10;
vector<ll> prime;
bitset<N> table;

void solve(string in,int i){
    cout << in << '\n';

    ofstream fout;
    fout.open(in);

    random_device rd;
    mt19937 gen(rd());

    uniform_int_distribution<ll> ranN, ranprime_idx, ranfactor, prob(1,100);


    if(i <= 2){
        ranN.param(uniform_int_distribution<ll>::param_type(1, ll(1e3)));
        ranprime_idx.param(uniform_int_distribution<ll>::param_type(0, 102));
        ranfactor.param(uniform_int_distribution<ll>::param_type(3, ll(5e2)));
    }else if(i <= 4){
        ranN.param(uniform_int_distribution<ll>::param_type(ll(5e4), ll(1e5)));
        ranprime_idx.param(uniform_int_distribution<ll>::param_type(1253, 41662));
        ranfactor.param(uniform_int_distribution<ll>::param_type(ll(4e5), ll(5e5)));
    }else{
        ranN.param(uniform_int_distribution<ll>::param_type(ll(5e5), ll(1e6)));
        ranprime_idx.param(uniform_int_distribution<ll>::param_type(41663, 149154));
        ranfactor.param(uniform_int_distribution<ll>::param_type(ll(1e5), ll(2e6)));
    }

    ll N = ranN(gen);
    fout << N << endll;
    forr(i,0,N){
        if(prob(gen)<75)fout << prime[ranprime_idx(gen)] << endll;
        else fout << ranfactor(gen) << endll;
    }

}

int main() {

    prime.push_back(2);
    for(ll i=3;i<N;i+=2){
        if(table[i])continue;
        prime.push_back(i);
        if(i*i<N)prime.push_back(i*i);
        for(ll j=i*i;j<N;j+=i*2)table[j] = true;
    }
    sort(prime.begin(),prime.end());
    // cout << prime.size() << sp; //size = 149156
    // forr(i,0,prime.size())if(prime[i]>ll(5e2)){cout << i << sp;break;} // i = 102
    // forr(i,0,prime.size())if(prime[i]>ll(1e4)){cout << i << sp;break;} // i = 1253
    // forr(i,0,prime.size())if(prime[i]>ll(5e5)){cout << i << sp;break;} // i = 41663

    for(int i = 1; i <= 10; i++){
        solve("testcases/input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}