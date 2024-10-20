#include <stdio.h>
#include <stdlib.h>
#include <memory.h>

int main() {
	int N = 0x100;
	void* ptr0 = malloc(N);
	memset(ptr0, 0x55, N);
	void* ptr1 = malloc(N);
	memset(ptr1, 0x66, N);
	void* ptr2 = malloc(N);
	memset(ptr2, 0x77, N);
	free(ptr0);
	free(ptr1);
	free(ptr2);
	printf("ptr0: %p\n", ptr0);
	printf("ptr1: %p\n", ptr1);
	printf("ptr2: %p\n", ptr1);
	for (int i = 0; i < N; ++i) {
		printf("%02x ", (unsigned char)((char*)ptr0)[i]);
	}
	printf("\n");
	for (int i = 0; i < N; ++i) {
		printf("%02x ", (unsigned char)((char*)ptr1)[i]);
	}
	printf("\n");
	for (int i = 0; i < N; ++i) {
		printf("%02x ", (unsigned char)((char*)ptr2)[i]);
	}
	printf("\n");
	return 0;
}