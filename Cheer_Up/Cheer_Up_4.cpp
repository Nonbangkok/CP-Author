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
int table[N];

int main(){macos;

    table[1] = 1;
    for(ll i=2;i<N;i++){
        if(table[i])continue;
        for(ll j=i*i;j<N;j+=i)table[j] = 1;
        if(i*i<N)table[i*i] = 2;
    }

    int n,q;
    cin >> q;

    while(q--){
        cin >> n;
        cout << (table[n]^1?"YES":"NO") << endll;
    }

    return 0;
}