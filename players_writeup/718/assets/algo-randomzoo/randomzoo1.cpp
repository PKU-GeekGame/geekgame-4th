#include <iostream>
using namespace std;
int main() {
  int first = 0;
  cin >> first;
  for (int i = -__INT_MAX__; i < __INT_MAX__; i++) {
    cout << i << "\r";
    srand(i);
    if (rand() == first - 'f') {
      cout << "Seed: " << i << endl;
    }
  }
}
