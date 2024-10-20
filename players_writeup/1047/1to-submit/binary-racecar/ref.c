#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <pthread.h>

char flag_buf[100];
volatile int size;
char p[0x200];
int usleep_time = 0;
char output_buf[100];

void* do_output(void* arg) {
	if (size > 4) {
		puts("output_size_is_too_large,");
		return NULL;
	}
	if (size < 0) {
		puts("inavlid output size");
		return NULL;
	}
	int len = strlen(flag_buf);
	if (len > 0x30) {
		puts("what happened");
		return 0;
	}
	usleep(usleep_time);
	puts("copying the flag...");
	memcpy(output_buf, flag_buf, size);
	puts(output_buf);
	return NULL;
}

void* get_thread2_input(void* s) {
	puts("please_enter_the_size_to_read_to_the_buffer:");
	scanf("%d", &size);
	if (size > 0x31) {
		puts("the_size_read_to_the_buffer_is_too_large");
		return 0;
	}
	memcpy(buf, s, size);
	puts("input success!");
	return NULL;
}

int main(int argc, char* argv[]) {
	// Do not buffer input and output
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);

	puts("for racecar drivers, there are two things to hope for: one is that you drive fast enough, and the other is that the opponent is slow enough.");
	puts("Brave and clever contestant,  win the race to get the flag!");

	strcpy(flag_buf, "flag{this_is_a_fake_flag}");

	printf("please enter the size to output your flag:\n");
	scanf("%d", &size);

	puts("please enter the content to read to buffer (max 0x100 bytes):");
	read(0, p, 0x104);

	sleep(1);

	pthread_t t1, t2;
	pthread_create(&t1, NULL, do_output, NULL);
	pthread_create(&t2, NULL, get_thread2_input, p);

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);
	
	return 0;
}
