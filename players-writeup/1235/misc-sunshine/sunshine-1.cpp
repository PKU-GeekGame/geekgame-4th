#include <bits/stdc++.h>
using namespace std;
int main() {
    freopen("sunshine.log", "r", stdin);
    char ch;
    string s;
    while ((ch = getchar()) != EOF) s += ch;
    freopen("keycode.txt", "r", stdin);
    string dat;
    map<int, string> mp;
    while (getline(cin, dat)) {
        if (dat.find("0x") != string::npos) {
            int x;
            sscanf(dat.substr(dat.find("0x"), 4).c_str(), "0x%x", &x);
            char tmp[100];
            sscanf(dat.substr(47).c_str(), " %s", tmp);
            mp[x] = tmp;
        }
    }
    int lstpos = 0;
    while (true) {
        int curpos = s.find("--begin keyboard packet--", lstpos);
        if (curpos == string::npos) break;
        int keyactionpos = s.find("keyAction", curpos);
        int type;
        if (s.substr(keyactionpos, 20) == "keyAction [00000003]") {
            type = 0;
        } else {
            type = 1;
        }
        int keycodepos = s.find("keyCode", curpos);
        int keycode;
        sscanf(s.substr(keycodepos, 14).c_str(), "keyCode [%x]", &keycode);
        keycode -= 0x8000;
        if (type == 0) printf("%x: %s\n", keycode, mp[keycode].c_str());
        else printf("               %x: %s\n", keycode, mp[keycode].c_str());
        lstpos = s.find("--end keyboard packet--", curpos) + 1;
    }
    return 0;
}
/*
flag{onlyapplecando}
keycode from https://github.com/LizardByte/Sunshine/blob/6fa6a7d515b672041a9090b7f2357a0f0e2900d1/src/platform/macos/input.cpp#L58
*/