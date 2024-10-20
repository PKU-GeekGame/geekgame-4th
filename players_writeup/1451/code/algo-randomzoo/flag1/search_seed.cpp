#include <iostream>
#include <fstream>
#include <climits>
#include <cstdlib>

int main() {
    std::ofstream output("out.txt");
    if (!output.is_open()) {
        std::cerr << "Failed to open output file" << std::endl;
        return 1;
    }

    for (unsigned int i = 0; i < UINT_MAX; ++i) {
        // 每过一千万次打印一次 i
        if (i % 10000000 == 0) {
            std::cout << "Current i: " << i << std::endl;
        }
        srand(i);
        
        int t = rand();
        if (t == 1220556798 - 102) {
            output << i << "\n";
            std::cout << "!!" << std::endl;
        }
    }
    output.close();
    return 0;
}