#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

int t,n,k;

int main(){macos;

    cin >> t;

    while(t--){
        cin >> n >> k;
        if(n!=1 && 2<k && k<2*n)cout << n - (k-1)/2 + max(1,k-n);
        else cout << -1;
        cout << endll;
    }

    return 0;
}