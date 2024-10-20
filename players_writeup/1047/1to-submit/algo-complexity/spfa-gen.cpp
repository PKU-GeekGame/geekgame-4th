#include<bits/stdc++.h>
using namespace std;
struct Edge {
	int f, t, c;
};

int main(){
	int n = 2000, m = 8000;
	printf("%d %d %d %d\n", n, m, 1, n);
	vector<Edge> es;
	for (int i = n; i >= 2; --i) {
		es.push_back({i, i-1, 1});
		es.push_back({1, i, (n-i+1)*2+1});
	}
	while (es.size() != m) {
		int f = rand() % n + 1;
		int t = rand() % n + 1;
		if (f == t) continue;
		es.push_back({f,t,rand()%100000+100000});
	}
	random_shuffle(es.begin(),es.end());
	for(auto e:es) printf("%d %d %d\n",e.f,e.t,e.c);
}

