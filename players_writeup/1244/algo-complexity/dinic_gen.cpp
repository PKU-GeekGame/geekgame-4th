#include <iostream>
#include <tuple>
#include <vector>
#include <random>
#include <algorithm>

const int N = 50;
// const int MAXW = 124000;
// const int SEED = 40;

using Edge = std::tuple<int, int, int>;

int main(void) {
    std::vector<Edge> edges;
    int n = N * 2;
    for (int i = 1; i <= N; i++) {
        for (int j = N + 1; j <= N * 2; j++) {
            edges.push_back({i, j, 1});
            if (i < N)
                edges.push_back({i, j, 1});
        }
        edges.push_back({i, i + 1, n});
    }
    std::cout << n << " " << edges.size() << " " << 1 << " " << n << std::endl;
    for (auto e : edges) {
        std::cout << std::get<0>(e) << " " << std::get<1>(e) << " " << std::get<2>(e) << std::endl;
    }
    return 0;
}
