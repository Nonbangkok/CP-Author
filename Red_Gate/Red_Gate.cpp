#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

int t;
double dl,dw,vl,vw;

double f(double x){
    return (x/vl) + sqrt((dl-x)*(dl-x)+dw*dw)/vw;
}

int main(){macos;

    cin >> t;
    cout << fixed << setprecision(3);
    while(t--){
        cin >> dl >> dw >> vl >> vw;
        double x = dl-sqrt((dw*dw*vw*vw)/(vl*vl-vw*vw));
        if(vw>=vl||x<0)cout << f(0);
        else cout << f(x);
        cout << endll;
    }

    return 0;
}