#include <bits/stdc++.h>

const int LINE = 624;
const int N = LINE * 10;
const int DATA_NUM = 5000;

using formula = std::bitset<N + 1>;
// formula : F = \sum_i{a_ix_i} + c
//	[0, varN - 1]	: a_i
//  [varN, N)		: nothing
//	N				: c

using number = formula[32];
// number: 32 bits of formula

unsigned data[DATA_NUM];
number mt[LINE];

unsigned varN;

formula equations[N];

void reverse_extract(number y) {
	// R: y = y ^ y >> 18
	for (int i = 31 - 18; i >= 0; --i)
		y[i] ^= y[i + 18];
	// R: y = y ^ y << 15 & 4022730752
	for (int i = 15; i < 32; ++i)
		if (4022730752u >> i & 1)
			y[i] ^= y[i - 15];
    // R: y = y ^ y << 7 & 2636928640
	for (int i = 7; i < 32; ++i)
		if (2636928640u >> i & 1)
			y[i] ^= y[i - 7];
    // R: y = y ^ y >> 11
	for (int i = 31 - 11; i >= 0; --i)
		y[i] ^= y[i + 11];
}
void extract(number y) {
	// y = y ^ y >> 11
	for (int i = 0; i < 32 - 11; ++i)
		y[i] ^= y[i + 11];
	// y = y ^ y << 7 & 2636928640
	for (int i = 31; i >= 7; --i)
		if (2636928640u >> i & 1)
			y[i] ^= y[i - 7];
    // y = y ^ y << 15 & 4022730752
	for (int i = 31; i >= 15; --i)
		if (4022730752u >> i & 1)
			y[i] ^= y[i - 15];
    // y = y ^ y >> 18
	for (int i = 0; i < 32 - 18; ++i)
		y[i] ^= y[i + 18];
}

std::pair<int, int> pos[N];

void twist(int i) {
	static number y;
	// y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
	y[31] = mt[i][31];
	for (int j = 0; j < 31; ++j)
		y[j] = mt[(i + 1) % 624][j];
	// self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]
	for (int j = 0; j < 32; ++j) {
		mt[i][j] = mt[(i + 397) % 624][j];
		if (j < 31)
			mt[i][j] ^= y[j + 1];
	}
	// if y % 2 != 0: self.mt[i] = self.mt[i] ^ 0x9908b0df
	for (int j = 0; j < 32; ++j)
		if (0x9908b0dfu >> j & 1)
			mt[i][j] ^= y[0];
}

// add Equation: F(x) = 0
int base_num = 0;
formula bases[N];

unsigned mt_data[LINE];
void get_answer() {
	for (int i = 0; i < LINE; ++i)
		mt_data[i] = data[i];
	for (int i = 0; i < varN; ++i) {
		int x, y; std::tie(x, y) = pos[i];
		mt_data[x] &= ~(1u << y);
		mt_data[x] |= (unsigned)bases[i].test(N) << y;
	}
	for (int i = 0; i < LINE; ++i) {
		std::cout << (char)(data[i] - mt_data[i]);
	}
	std::exit(0);
}


void add_equation(formula eq) {
	// Gaussian Elimination
	// Eliminated by Bases
	// std::cout << "Insert Equation: " << eq << std::endl;
	for (int i = eq._Find_first(); i < varN; i = eq._Find_next(i))
		if (bases[i].test(i))
			eq ^= bases[i];
	// Unuseful
	if (eq.none())
		return;
	// Set `eq` as Base(idx)
	int idx = eq._Find_first();
	// Conflict in Equations
	assert(idx < N);
	// Eliminate other Bases
	for (int j = 0; j < idx; ++j)
		if (bases[j].test(idx))
			bases[j] ^= eq;
	bases[idx] = eq;

	if (++base_num == varN) {
		for (int i = 0; i < varN; ++i) {
			assert(bases[i].count() == 1 && bases[i].test(i));
		}
		get_answer();
	}
}

int main() {
	std::freopen("data.txt", "r", stdin);
	std::ios::sync_with_stdio(0), std::cin.tie(0);
	for (int i = 0; i < LINE; ++i) {
		std::cin >> data[i];
		int lb = __builtin_ctz(data[i] >> 7) + 8;
		// assert(lb < 32);
		// [0, lb) unreliable
		for (int j = 0; j < lb; ++j) {
			mt[i][j].set(varN);
			pos[varN++] = {i, j};
		}
		for (int j = lb; j < 32; ++j)
			if (data[i] >> j & 1)
				mt[i][j].set(N);
	}
	std::cout << "Unreliable bits: " << varN << std::endl;
	assert(varN <= N);

	for (int i = 0; i < LINE; ++i)
		reverse_extract(mt[i]);
	
	for (int i = LINE; i < DATA_NUM; ++i) {
		twist(i % LINE);

		static number num;
		for (int j = 0; j < 32; ++j)
			num[j] = mt[i % LINE][j];
		extract(num);

		std::cin >> data[i];
		int lb = __builtin_ctz(data[i] >> 7) + 8;
		// [lb, 32): Reliable
		for (int j = lb; j < 32; ++j) {
			formula f = num[j];
			if (data[i] >> j & 1)
				f.flip(N);
			add_equation(f);
		}
	}
	std::cout << "base_num : " << base_num << std::endl;
	std::cout << "varN: " << varN << std::endl;
	get_answer();
	return 0;
}