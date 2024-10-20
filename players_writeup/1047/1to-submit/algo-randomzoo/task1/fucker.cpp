#include <bits/stdc++.h>
#include <limits.h>
#include <unistd.h>

long long get_first_rand_number(unsigned int seed) {
	srand(seed);
	return (long long)rand()+(long long)'f';
}

long long vs[50];

int main() {
	for (int i = 0; i < 50; ++i)
		std::cin >> vs[i];

	int NUM_WORKERS = 16;
	int my_worker_id = -1;
	for (int worker_id = 0; worker_id < NUM_WORKERS; ++worker_id) {
		pid_t pid = fork();
		if (pid == 0) {
			// Father
		} else {
			my_worker_id = worker_id;
			break;
		}
	}
	if (my_worker_id == -1)
		usleep(1000000000);
	
	long long lower_l = my_worker_id * ((long long)UINT_MAX/NUM_WORKERS);
	long long upper_l = my_worker_id == NUM_WORKERS-1 ? UINT_MAX : (my_worker_id+1) * ((long long)UINT_MAX/NUM_WORKERS);
	unsigned int lower = lower_l;
	unsigned int upper = upper_l;
	printf("Worker %d: %u %u\n", my_worker_id, lower, upper);

	unsigned int seed = 0;
	for (unsigned int i = lower; i < upper; ++i) {
		long long cur_rand = get_first_rand_number(i);
		if (cur_rand == vs[0]) {
			printf("Random seed: %u\n", i);
			seed = i;

			srand(seed);
			for (int i = 0; i < 50; ++i) {
				std::cout << (char)(vs[i]-(long long)rand());
			}
			std::cout << std::endl;
		}
	}
}