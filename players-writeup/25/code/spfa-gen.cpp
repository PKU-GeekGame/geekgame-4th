#include <iostream>
using namespace std;

void make_edge(int u, int v, int w) {
    printf("%d %d %d\n", u, v, w);
}
int main(){
	freopen("spfa.in", "w", stdout);
	int n = 2000, m = 3997;
    int maxw = 1e5;
	cout << n << " " << m << " " << 2 << " " << n << endl;
    for (int i = n; i >= 2; i--) {
        make_edge(i, 1, maxw - i * 2);
        if (i != n) {
            make_edge(i, i + 1, 1);
        }
    }
}