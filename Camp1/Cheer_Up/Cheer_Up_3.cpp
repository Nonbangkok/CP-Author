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

    int q;
    cin >> q;
    for(int i=0;i<q;i++){
        int x;
        cin >> x;
        ll divisor = 1LL;
        for(int i=2;i<=x/2;i++){
            if(x%i==0)divisor *= i;
            if(divisor>=x)break;
        }
        if(divisor<x)cout << "YES" << endll;
        else cout << "NO" << endll;
    }

    return 0;
}