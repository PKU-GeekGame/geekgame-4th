#include <bits/stdc++.h>
using namespace std;
int main() {
    unsigned int seed = 2783496401u;
    srand(seed);
    freopen("data.txt", "r", stdin);
    for (int i = 0; i < 100; i++) {
        long long x;
        cin >> x;
        cout << (char)(x - rand());
    }
    return 0;
}