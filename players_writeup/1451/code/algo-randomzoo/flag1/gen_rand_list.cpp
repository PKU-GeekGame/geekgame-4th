#include <cstring>
#include <fstream>
#include <iostream>
#include <cstdio>
using namespace std;
unsigned int rand_init;
int main(){

    char flag[100] = "flag{114514}";
    int flag_len=strlen(flag);
    
    srand(424824872);
    for(int i=0;;i++){
        cout<<(long long)rand()<<endl;
        getchar();
    }
}