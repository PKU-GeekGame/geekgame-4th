#include <bits/stdc++.h>
using namespace std;
int main() {
    vector<long long> vec(2000);
    freopen("data.txt", "r", stdin);
    for (int i = 0; i < 2000; i++) {
        cin >> vec[i];
    }
    for (int len = 53; len <= 53; len++) { // found 53
        map<tuple<int, int, int>, set<long long>> mp;
        for (int i = 607; i < 2000; i++) {
            int p1 = i % len, p2 = (i - 607) % len, p3 = (i - 273) % len;
            if (p2 > p3) swap(p2, p3);
            long long val = vec[i] - vec[i - 273] - vec[i - 607];
            val %= (1ll << 32);
            if (val < 0) val += (1ll << 32);
            mp[make_tuple(p1, p2, p3)].insert(val);
        }
        bool good = true;
        for (auto &it : mp) {
            if (it.second.size() > 2) {
                good = false;
                break;
            }
        }
        if (good) printf("Good len %d\n", len);
        else continue;
        vector<vector<double>> mat;
        vector<int> cnt(len, 0);
        for (auto &it : mp) {
            vector<double> row(len + 1, 0);
            assert(it.second.size() == 2);
            cnt[get<0>(it.first)]++;
            cnt[get<1>(it.first)]--;
            cnt[get<2>(it.first)]--;
            //printf("%lld %lld\n", *it.second.begin() - (1ll << 32), *it.second.rbegin() - (1ll << 32));
            row[len] = *it.second.begin() - (1ll << 32);
            row[get<0>(it.first)] = 1;
            row[get<1>(it.first)] = -1;
            row[get<2>(it.first)] = -1;
            mat.push_back(row);
        }
        for (int i = 0; i < len; i++) assert(cnt[i] == -1);
        for (int i = 0, j, k; i < (int)mat.size(); i++) {
            for (j = i; j < (int)mat.size(); j++) {
                if (fabs(mat[j][i]) > 1e-8) break;
            }
            if (j == (int)mat.size()) {
                printf("BAD %d\n", i);
                continue;
            }
            if (i != j) swap(mat[i], mat[j]);
            for (j = i + 1; j < (int)mat.size(); j++) {
                double ratio = mat[j][i] / mat[i][i];
                for (k = i; k <= len; k++) {
                    mat[j][k] -= ratio * mat[i][k];
                }
            }
        }
        for (int i = len - 1; i >= 0; i--) {
            for (int j = i + 1; j < len; j++) {
                mat[i][len] -= mat[j][len] * mat[i][j];
            }
            mat[i][len] /= mat[i][i];
        }
        for (int i = 0; i < len; i++) {
            printf("%c", (char)(int)round(mat[i][len]));
        }
    }
    return 0;
}