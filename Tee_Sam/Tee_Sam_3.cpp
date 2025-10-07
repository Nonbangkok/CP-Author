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
    forr(i,1,n+1)cin >> A[i];

    int mx = 0,st=-1,dest=-1;
    forr(i,1,n+1){
        forr(j,i,n+1){
            ll sum = 0;
            forr(k,i,j+1)sum += A[k];
            if(sum>m)break;
            if(mx<j-i+1){
                mx = j-i+1;
                st = i;
                dest = j;
            }
        }
    }

    cout << mx << endll << st << sp << dest;

    return 0;
}