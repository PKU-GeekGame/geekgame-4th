#include <bits/stdc++.h>
using namespace std;
#define N 624
#define M 397
#define MATRIX_A 0x9908b0dfU    /* constant vector a */
#define UPPER_MASK 0x80000000U  /* most significant w-r bits */
#define LOWER_MASK 0x7fffffffU  /* least significant r bits */
array<bitset<N*32>, 32> mt[N];
int index;
array<bitset<N*32>, 32> e_xor(const array<bitset<N*32>, 32>& a, const array<bitset<N*32>, 32>& b) {
    static array<bitset<N*32>, 32> res;
    for (int i = 0; i < 32; i++) {
        res[i] = a[i] ^ b[i];
    }
    return res;
}
array<bitset<N*32>, 32> e_rsft(const array<bitset<N*32>, 32>& a, int b) {
    static array<bitset<N*32>, 32> res;
    for (int i = 0; i < 32 - b; i++) {
        res[i] = a[i + b];
    }
    for (int i = 32 - b; i < 32; i++) {
        res[i].reset();
    }
    return res;
}
array<bitset<N*32>, 32> e_lsft(const array<bitset<N*32>, 32>& a, int b) {
    static array<bitset<N*32>, 32> res;
    for (int i = 0; i < 32 - b; i++) {
        res[i + b] = a[i];
    }
    for (int i = 0; i < b; i++) {
        res[i].reset();
    }
    return res;
}
array<bitset<N*32>, 32> e_and(const array<bitset<N*32>, 32>& a, uint32_t b) {
    static array<bitset<N*32>, 32> res;
    for (int i = 0; i < 32; i++) {
        if (b >> i & 1)
            res[i] = a[i];
        else
            res[i].reset();
    }
    return res;
}
array<bitset<N*32>, 32> genrand_uint32() {
    static array<bitset<N*32>, 32> y, tmp;
    if (index >= N) { /* generate N words at one time */
        int kk;

        for (kk=0;kk<N;kk++) {
            for (int i = 0; i <= 30; i++) y[i] = mt[(kk+1)%N][i];
            y[31] = mt[kk][31];
            for (int i = 0; i < 32; i++) {
                if (MATRIX_A >> i & 1)
                    tmp[i] = y[0];
                else
                    tmp[i].reset();
            }
            mt[kk] = e_xor(mt[(kk+M)%N], e_xor(e_rsft(y, 1), tmp));
        }

        index = 0;
    }

    for (int i = 0; i < 32; i++) y[i] = mt[index][i];
    y = e_xor(y, e_rsft(y, 11));
    y = e_xor(y, e_and(e_lsft(y, 7), 0x9d2c5680U));
    y = e_xor(y, e_and(e_lsft(y, 15), 0xefc60000U));
    y = e_xor(y, e_rsft(y, 18));
    index++;
    return y;
}
void init_rand() {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 32; j++) {
            mt[i][j].reset();
            mt[i][j].set(32 * i + j);
        }
    }
    index = 0;
}
bitset<N*32> eq[N*32], val, has;
void add_eq(bitset<N*32> a, int v) {
    for (int i = 0; i < N*32; i++) if (a[i]) {
        if (has[i]) {
            a ^= eq[i];
            v ^= val[i];
        } else {
            eq[i] = a;
            val[i] = v;
            has[i] = 1;
            return;
        }
    }
    assert(v == 0);
}
namespace MT {
uint32_t state[N];
int index;
uint32_t genrand_uint32() {
    uint32_t y;
    static const uint32_t mag01[2] = {0x0U, MATRIX_A};
    /* mag01[x] = x * MATRIX_A  for x=0,1 */
    uint32_t *mt;

    mt = state;
    if (index >= N) { /* generate N words at one time */
        int kk;

        for (kk=0;kk<N-M;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        for (;kk<N-1;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1U];
        }
        y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
        mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1U];

        index = 0;
    }

    y = mt[index++];
    y ^= (y >> 11);
    y ^= (y << 7) & 0x9d2c5680U;
    y ^= (y << 15) & 0xefc60000U;
    y ^= (y >> 18);
    return y;
}
}
int main() {
    init_rand();
    has.reset();
    freopen("data.txt", "r", stdin);
    vector<long long> vec;
    for (int i = 0; i < 3000; i++) {
        auto x = genrand_uint32();
        long long y;
        cin >> y;
        vec.push_back(y);
        long long z = y - 127;
        if (i == 0) {
            z = y - 'f'; y = z;
        } else if (i == 1) {
            z = y - 'l'; y = z;
        } else if (i == 2) {
            z = y - 'a'; y = z;
        } else if (i == 3) {
            z = y - 'g'; y = z;
        } else if (i == 4) {
            z = y - '{'; y = z;
        }
        int j;
        for (j = 31; j >= 0; j--) {
            if ((y >> j & 1) != (z >> j & 1)) {
                break;
            }
        }
        for (int k = 31; k > j; k--) {
            add_eq(x[k], y >> k & 1);
        }
    }
    int cnt = 0;
    for (int i = 0; i < N*32; i++) if (has[i]) cnt++;
    assert(cnt == N*32);
    for (int i = N*32 - 1; i >= 0; i--) {
        if (val[i]) {
            for (int j = 0; j < i; j++) if (eq[j][i]) {
                val[j].flip();
            }
        }
    }
    for (int i = 0; i < N; i++) {
        uint32_t x = 0;
        for (int j = 0; j < 32; j++) {
            if (val[32 * i + j]) {
                x |= 1u << j;
            }
        }
        MT::state[i] = x;
    }
    MT::index = 0;
    for (int i = 0; i < 100; i++) {
        putchar(vec[i] - MT::genrand_uint32());
    }
    return 0;
}