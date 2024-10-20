#include <cstring>
#include <fstream>
#include <iostream>
#include <cstdio>
using namespace std;
char flag[100];
int flag_len;
unsigned int rand_init;
int main(){
    ifstream fin("flag.txt");
    fin>>flag;
    flag_len=strlen(flag);
    ifstream urandom("/dev/urandom", ios::in|ios::binary);
    urandom.read(reinterpret_cast<char*>(&rand_init), sizeof(rand_init));
    srand(rand_init);
    for(int i=0;;i++){
        cout<<(long long)rand()+(long long)flag[i%flag_len]<<endl;
        getchar();
    }
}