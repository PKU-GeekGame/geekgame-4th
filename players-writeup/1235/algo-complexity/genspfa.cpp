#include <bits/stdc++.h>
using namespace std;
mt19937 rng(114514);
int myrand(int l, int r) {
    return uniform_int_distribution<int>(l, r)(rng);
}
int main() {
    int n = 2000;
    vector<tuple<int, int, int>> edges;
    int R = 5, C = 400;
    for (int i = 1; i <= R; i++) {
        for (int j = 1; j <= C; j++) {
            if (i < R) {
                edges.emplace_back((i - 1)*C + j, i*C + j, 1);
            }
            if (j < C) {
                edges.emplace_back((i - 1)*C + j, (i - 1)*C + j + 1, myrand(10000, 100000));
            }
            if (i < R && j < C) {
                edges.emplace_back((i - 1)*C + j, i*C + j + 1, myrand(10000, 100000));
            }
        }
    }

    shuffle(edges.begin(), edges.end(), rng);
    printf("%d %d %d %d\n", n, (int)edges.size(), 1, n);
    for (auto [u, v, w] : edges) {
        printf("%d %d %d\n", u, v, w);
    }
    return 0;
}