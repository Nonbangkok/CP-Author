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
double a,b,v,w;

double f(double x){
    return (x/v) + sqrt((a-x)*(a-x)+b*b)/w;
}

int main(){macos;

    cin >> t;
    cout << fixed << setprecision(3);
    while(t--){
        cin >> a >> b >> v >> w;
        if(w>=v){
            cout << f(0) << endll;
            continue;
        }

        double mn = f(0),fx;
        for(double x=0.001;x<=a;x+=0.001){
            fx = f(x);
            if(mn>fx)mn = fx;
            else{
                // cout << x << sp << mn << endll;
                cout << mn << endll;
                break;
            }
        }
    }

    return 0;
}