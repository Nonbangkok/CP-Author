#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;
const int M = 1e9+7;

ll power(ll n, ll d){
    ll ans = 1;
    n %= M;
    forr(i,0,d){
        ans *= n;
        ans %= M;
    }
    return ans;
}

int main(){macos;

    ll n,x1,y1,x2,y2;
    cin >> n >> x1 >> y1 >> x2 >> y2;
    ll d = sqrt(pow(x1-x2,2)+pow(y1-y2,2));
    ll k = (power(n,d) + ll(log(n)) + 5) % M;
    cout << k;

    return 0;
}