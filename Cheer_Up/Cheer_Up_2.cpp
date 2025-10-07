#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

bool is_prime(int n){
    if(n==1)return false;
    if(n==2)return true;
    if(n%2==0)return false;
    for(int i=3;i*i<=n;i+=2){
        if(n%i==0)return false;
    }
    return true;
}

int main(){macos;

    int q;
    cin >> q;
    for(int i=0;i<q;i++){
        int x;
        cin >> x;
        int num,sq = sqrt(x);
        if(sq*sq==x)num = sq;
        else num = x;
        bool chk = is_prime(num);
        if(chk)cout << "YES" << endll;
        else cout << "NO" << endll;
    }

    return 0;
}