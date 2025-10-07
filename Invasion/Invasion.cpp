#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

const int N = 1e6+10;
ll A[N];
ll n,k,sum,cnt;

bool chk(ll m){
    ll cnt = 1, sum = 0;
    forr(i,0,n){
        if(A[i]>m)return true;
        if(sum+A[i]>m)sum = 0,cnt++;
        sum += A[i];
    }
    return cnt > k;
}

int main(){macos;

    cin >> n >> k;
    forr(i,0,n)cin >> A[i],sum += A[i];

    ll l=0,r=sum,m;
    while(l<r){
        m = (l+r) >> 1;

        if(chk(m))l = m + 1;
        else r = m;
    }
    cout << l;

    return 0;
}