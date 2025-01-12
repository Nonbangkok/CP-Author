#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

void solve(string in, string out){
    cout << in << '\n';

    ifstream fin;
    ofstream fout;

    fin.open(in);
    fout.open(out);

    ll n,x1,y1,x2,y2;
    fin >> n >> x1 >> y1 >> x2 >> y2;
    ll d = sqrt(pow(x1-x2,2)+pow(y1-y2,2));
    ll k = pow(n+1,d) + ll(log(n+1)) + 5;
   
    fout << k;
}

int main(){

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",
            "./output/output" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt");
    }

    return 0;
}