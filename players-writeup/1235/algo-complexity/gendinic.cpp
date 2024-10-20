#include <bits/stdc++.h>
using namespace std;
mt19937 rng(114514);
int myrand(int l, int r) {
    return uniform_int_distribution<int>(l, r)(rng);
}
int main() {
    int k = 33, p = 16;
    int n = 2 + k * 2 + p * 2;
    vector<tuple<int, int, int>> edges;
    for (int i = 1; i <= k; i++) {
        edges.emplace_back(1, 2 + i, k);
        edges.emplace_back(2 + k + i, 2, k);
        for (int j = 1; j <= k; j++) {
            edges.emplace_back(2 + i, 2 + k + j, 1);
        }
    }
    edges.emplace_back(1, 2 + k + k + 1, 1e6);
    edges.emplace_back(2 + k + k + p + 1, 2, 1e6);
    for (int i = 1; i < p; i++) {
        edges.emplace_back(2 + k + k + i, 2 + k + k + i + 1, 1e6);
        edges.emplace_back(2 + k + k + p + i + 1, 2 + k + k + p + i, 1e6);
    }
    for (int i = 2; i <= p; i += 2) {
        for (int j = 1; j <= k; j++) {
            edges.emplace_back(2 + k + k + i, 2 + ((i / 2) % 2 == 1 ? k : 0) + j, k);
            edges.emplace_back(2 + ((i / 2) % 2 == 0 ? k : 0) + j, 2 + k + k + p + i, k);
        }
    }
    printf("%d %d %d %d\n", n, (int)edges.size(), 1, 2);
    for (auto [u, v, w] : edges) {
        printf("%d %d %d\n", u, v, w);
    }
    return 0;
}