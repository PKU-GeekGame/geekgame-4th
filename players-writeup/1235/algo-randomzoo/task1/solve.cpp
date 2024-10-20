#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<long long> data;
    freopen("data.txt", "r", stdin);
    for (int i = 0; i < 5; i++) {
        long long x;
        cin >> x;
        data.push_back(x);
    }
    data[0] -= 'f';
    data[1] -= 'l';
    data[2] -= 'a';
    data[3] -= 'g';
    data[4] -= '{';
    for (long long x = 0; x < 4294967296ll; x++) {
        srand((unsigned int)x);
        bool ok = true;
        for (int i = 0; i < 5; i++) {
            if ((long long)rand() != data[i]) {
                ok = false;
                break;
            }
        }
        if (ok) {
            cout << x << endl;
        }
        if (x % 10000000 == 0) {
            cerr << "Progress: " << x << endl;
        }
    }
    cout << "Finished" << endl;
    return 0;
}