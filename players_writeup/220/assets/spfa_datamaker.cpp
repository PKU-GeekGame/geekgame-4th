#include <bits/stdc++.h>
using namespace std;
struct edge {
  int u, v, w;
};
vector<edge> v;
int id[5000][5000], n = 10, tp, m = 1700 / n, a[1000000];
int r() {
  return rand();
  // return rand()<<13|rand();
}
int main() {
  freopen("in.txt", "w", stdout);
  srand(time(0));
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j) id[i][j] = ++tp, a[tp] = tp;
  //	random_shuffle(a+1,a+tp+1);
  int SIZE = 29989;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j) {
      if (i < n) {
        v.push_back(edge{id[i][j], id[i + 1][j], 1});
        v.push_back(edge{id[i + 1][j], id[i][j], 1});
        if (j < m) {
          if (1)
            v.push_back(edge{id[i][j], id[i + 1][j + 1], r() % SIZE + 10});
          else
            v.push_back(edge{id[i + 1][j + 1], id[i][j], r() % SIZE + 10});
        }
      }
      if (j < m) {
        v.push_back(edge{id[i][j], id[i][j + 1], r() % SIZE + 10});
        v.push_back(edge{id[i][j + 1], id[i][j], r() % SIZE + 10});
      }
    }
  fprintf(stderr, "[%d,%d,%d]", v.size(), n, m);
  random_shuffle(v.begin(), v.end());
  printf("%d %d 1 2000\n", tp, v.size());
  for (int i = 0; i < v.size(); ++i)
    printf("%d %d %d\n", a[v[i].u], a[v[i].v], v[i].w);
}