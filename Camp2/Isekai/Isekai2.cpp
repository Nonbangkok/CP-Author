#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

int count_pairs(int n, int k){
    int count = 0;
    forr(a,1,n+1){
        int b = k - a;
        if(b>a &&b>=1&&b<=n)count++;
    }
    return (count?n-count+1:-1);
}

int main(){macos;

    int t;
    cin >> t;
    
    while(t--){
        int n, k;
        cin >> n >> k;
        cout << count_pairs(n,k) << endl;
    }

    return 0;
}