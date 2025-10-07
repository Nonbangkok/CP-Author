#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;
int main(){macos;

    ll q;
    cin >> q;
    for(ll i=0;i<q;i++){
        ll x;
        cin >> x;
        ll divisor = 1LL;
        for(ll j=2;j<=x/2;j++){
            if(x%j==0)divisor *= j;
            if(divisor>=x)break;
        }
        if(divisor<x)cout << "YES" << endll;
        else cout << "NO" << endll;
    }

    return 0;
}