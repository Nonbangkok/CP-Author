#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

const int N = 200, M = 1e9+7;
ll dp[N][N][2];
int n;
string s;

int solve(int a, int b, int k){
    if(s[k]=='d')return a&b;
    if(s[k]=='e')return !(a&b);
    if(s[k]=='n')return a|b;
    return a^b;
}

int main(){macos;

    cin >> s;
    n = s.size();

    forr(i,0,n)forr(j,0,n)dp[i][j][0]=dp[i][j][1]=0;
    forr(i,0,n){
        if(s[i]=='m')dp[i][i][1] = 1;
        if(s[i]=='o')dp[i][i][0] = 1;
    }
    for(int sz = 2;sz<n;sz+=2)
        for(int l=0;l<n-sz;l+=2){
        int r = l+sz;
        for(int k=l+1;k<r;k+=2)forr(a,0,2)forr(b,0,2)
            if(dp[l][k-1][a]&&dp[k+1][r][b])dp[l][r][solve(a,b,k)] = (dp[l][r][solve(a,b,k)]+(dp[l][k-1][a]*dp[k+1][r][b])%M)%M;
    }

    cout << dp[0][n-1][1];

    return 0;
}