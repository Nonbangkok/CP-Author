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
bool table[N];
ll prime[N];
ll prime_square[N];

int main(){macos;

    int idx = 0;
    for(ll i=2;i<N;i++){
        if(table[i])continue;
        prime[idx] = i;
        prime_square[idx] = i*i;
        idx++; 
        for(ll j=i*i;j<N;j+=i)table[j] = true;
    }
    
    int q;
    cin >> q;
    for(int i=0;i<q;i++){
        ll x;
        cin >> x;
        if(binary_search(prime,prime+idx,x)||binary_search(prime_square,prime_square+idx,x))
        cout << "YES" << endll;
        else cout << "NO" << endll;
    }

    return 0;
}