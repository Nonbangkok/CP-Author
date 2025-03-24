#include <bits/stdc++.h>
#define coutf(n, m) cout << fixed << setprecision(n) << m
#define forr(i, a, n) for (int i = a; i < n; i++)
#define forl(i, a, n) for (int i = a; i > n; i--)
#define macos ios::sync_with_stdio(0);cin.tie(0);cout.tie(0)
#define endll "\n"
#define sp " "
typedef long long ll;
using namespace std;

void solve(string in,int z){
    cout << in << '\n';

    ofstream fout;
    fout.open(in);

    random_device rd;
    mt19937 gen(rd());

    uniform_int_distribution<int> ranN, ran_rand(0,1), ran_tor(0,3);

    char operator1[] = {'d','e','n','g'};
    char operand[] = {'m','o'};

    if(z<=2){
        ranN.param(uniform_int_distribution<int>::param_type(10, 50));
    }else if(z<=4){
        ranN.param(uniform_int_distribution<int>::param_type(80, 100));
    }else{
        ranN.param(uniform_int_distribution<int>::param_type(160, 200));
    }

    int n = ranN(gen);
    if(!(n&1))n--;
    forr(i,0,n){
        if(!(i&1))fout << operand[ran_rand(gen)];
        else fout << operator1[ran_tor(gen)];
    }
}

int main() {

    for(int i = 1; i <= 10; i++){
        solve("./input/input" + (i == 10 ? "10" : "0" + to_string(i)) + ".txt",i);
    }

    return 0;
}