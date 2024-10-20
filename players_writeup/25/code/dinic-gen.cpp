#include <iostream>
using namespace std;

int edge_count = 0;
void make_edge(int u, int v, int w) {
    printf("%d %d %d\n", u, v, w);
    edge_count++;
}
int main(){
	freopen("dinic.in", "w", stdout);
	int n = 100, m = 1682;
    int k = 33, p = 16;
    int maxw = 1e5;
	cout << n << " " << m << " " << 1 << " " << 100 << endl;
    for (int i = 2; i <= k + 1; i++) {
        make_edge(1, i, k);
    }
    for (int i = 100 - k; i <= 99; i++) {
        make_edge(i, 100, k);
    }
    for (int i = 2; i <= k + 1; i++) {
        for (int j = 100 - k; j <= 99; j++) {
            make_edge(i, j, 1);
        }
    }
    int inf = 1e7;
    make_edge(1, k + 2, inf);
    make_edge(99 - k, 100, inf);
    for (int i = k + 2; i <= 49; i++) {
        make_edge(i, i + 1, inf);
    }
    for (int i = 51; i <= 98 - k; i++) {
        make_edge(i, i + 1, inf);
    }
    int cnt = 0;
    for (int i = k + 3; i <= 50; i += 2) {
        if (cnt % 2 == 1) {
            for (int j = 2; j <= k + 1; j++) {
                make_edge(i, j, k);
            }
        } else {
            for (int j = 100 - k; j <= 99; j++) {
                make_edge(i, j, k);
            }
        }
        cnt++;
    }
    cnt = 0;
    for (int i = 97 - k; i >= 51; i -= 2) {
        if (cnt % 2 == 0) {
            for (int j = 2; j <= k + 1; j++) {
                make_edge(j, i, k);
            }
        } else {
            for (int j = 100 - k; j <= 99; j++) {
                make_edge(j, i, k);
            }
        }
        cnt++;
    }
    cerr << edge_count;
}