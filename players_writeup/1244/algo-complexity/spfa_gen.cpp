#include <iostream>
#include <tuple>
#include <vector>
#include <random>
#include <algorithm>

// N * M grid
// Vertices: N * M
// Edges: (N - 1) * M + (M - 1) * N + (N - 1) * (M - 1)

const int N = 100, M = 20;
const int MAXW = 124000;
const int SEED = 40;

using Edge = std::tuple<int, int, int>;

int rand_num(void);

int main(void) {
    static int vertex_id[N + 1][M + 1];
    std::vector<Edge> edges;
    int n = 0;
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= M; j++) {
            vertex_id[i][j] = ++n;
        }
    }
    for (int i = 1; i <= N; i++)
        for (int j = 1; j < M; j++)
            edges.push_back({vertex_id[i][j], vertex_id[i][j + 1], 1});
    for (int i = 1; i < N; i++)
        for (int j = 1; j <= M; j++)
            edges.push_back({vertex_id[i][j], vertex_id[i + 1][j], rand_num() + 10000});
    for (int i = 1; i < N; i++)
        for (int j = 1; j < M; j++)
            edges.push_back({vertex_id[i][j], vertex_id[i + 1][j + 1], rand_num() + 10000});
    std::cout << n << " " << edges.size() << " " << vertex_id[1][1] << " " << vertex_id[N][M] << std::endl;
    for (auto e : edges) {
        std::cout << std::get<0>(e) << " " << std::get<1>(e) << " " << std::get<2>(e) << std::endl;
    }
    return 0;
}

int rand_num(void) {
    static std::mt19937 gen(SEED);
    static std::uniform_int_distribution<int> dist(1, MAXW);
    return dist(gen);
}
