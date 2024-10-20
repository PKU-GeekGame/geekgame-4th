/* https://codeforces.com/blog/entry/3730 */
#include <bits/stdc++.h>

int N = 2000;
std::vector<std::tuple<int, int, int>> edges;


int main() {
	const int W = 100000000;
	for (int i = 2; i <= N; ++i)
		edges.emplace_back(1, i, W / (i + 1));
	for (int i = 2; i < N; ++i)
		edges.emplace_back(i, i + 1, 1);
	std::cout << N << ' ' << edges.size() << ' ' << 1 << ' ' << N << '\n';
	for (auto [u, v, w] : edges) {
		std::cout << u << ' ' << v << ' ' << w << '\n';
	}
	return 0;
}