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

double df(double x){
    return (1/v) + (x-a)/(w*sqrt((a-x)*(a-x)+b*b));
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
        
        double l=0,r=a,m;
        while(abs(r-l)/abs(l)>1e-15){
        // forr(i,0,100){
            m = (l+r)/2.0;

            if(df(m)>0)r=m;
            else l=m;
        }
        cout << f(l) << endll;
    }

    return 0;
}