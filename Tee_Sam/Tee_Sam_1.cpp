#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

const int N = 5e5+10;
ll A[N];

int main(){macos;

    ll n,m;
    cin >> n >> m;
    forr(i,1,n+1){
        cin >> A[i];
    }

    ll l=1,mx=0,sum=0,st=-1,dest=-1;
    for(ll r=1;r<=n;r++){
        sum += A[r];
        while(sum>m)sum -= A[l++];
        if(mx<r-l+1){
            mx = r-l+1;
            st = l;
            dest = r;
        }
    }
    cout << mx << endll << st << sp << dest;

    return 0;
}
