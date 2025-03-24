#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

const int N = 5e6+10;
ll A[N] ,dpl[N] ,dpr[N];
stack<ll> s;

ll dis(ll l ,ll r ,ll i){
    if(l && r)return abs(l-r);
    else if(l)return abs(l-i);
    else if(r)return abs(i-r);
    return 0;
}

int main(){macos;

    ll n;
    cin >> n;
    for(ll i=1;i<=n;i++)cin >> A[i];

    for(ll i=1;i<=n;i++){
        while(!s.empty()&&A[i]<=A[s.top()])s.pop();
        if(!s.empty())dpl[i] = s.top();
        s.push(i);
    }
    while(!s.empty())s.pop();
    for(ll i=n;i>0;--i){
        while(!s.empty()&&A[i]<=A[s.top()])s.pop();
        if(!s.empty())dpr[i] = s.top();
        s.push(i);
    }
    for(int i=1;i<=n;i++){
        ll x = dis(dpl[i],dpr[i],i);
        cout << x << sp;
    }

    // forr(i,0,n)cout << dpl[i] << sp;cout << endll;
    // forr(i,0,n)cout << dpr[i] << sp;cout << endll;

    return 0;
}