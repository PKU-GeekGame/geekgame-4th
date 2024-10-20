#include <bits/stdc++.h>

const int N = 100;
long long data[N];
int main() {
	std::freopen("result", "r", stdin);
	std::ios::sync_with_stdio(0), std::cin.tie(0);
	for (int i = 0; i < N; ++i) {
		std::cin >> data[i];
	}

	for (unsigned seed = 0; ; ++seed) {
		srand(seed);
		if ((seed & 0xfffff) == 0)
			std::cout << seed << std::endl;
		bool fail = 0;
		for (int i = 0; i < N; ++i) {
			long long diff = data[i] - (long long) rand();
			if (diff < 128) {
				std::cout << (char) diff;
			} else {
				fail = 1; break;
			}
		}
		if (!fail) break;
		if (seed == (unsigned)-1) break;
	}

	return 0;
}