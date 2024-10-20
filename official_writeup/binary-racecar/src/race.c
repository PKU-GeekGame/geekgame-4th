#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
char p[0x100];
int usleep_time;
char flag_buf[0x30];
char output_buf[0x30];
char buf[0x30];
int size;
void *do_output(void *arg)
{
    if (size > 4)
    {
        printf("output size is too large\n");
        return 0;
    }
    if (size <= 0)
    {
        printf("invalid output size!!\n");
        return 0;
    }
    int len = strlen(flag_buf);
    if (len > 0x30)
    {
        printf("what happened?\n");
        return 0;
    }
    usleep(usleep_time);
    printf("copying the flag...\n");
    memcpy(output_buf, flag_buf, size);
    printf("%s\n", output_buf);
    return 0;
}
void *get_thread2_input(void *arg)
{
    puts("please enter the size to read to the buffer:");
    scanf("%d", &size);
    if (size > 0x31)
    {
        printf("the size read to the buffer is too large\n");
        return 0;
    }
    memcpy(buf, arg, size);
    puts("input success!\n");
    return 0;
}
int main()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    
    puts("for racecar drivers, there are two things to hope for: one is that you drive fast enough, and the other is that the opponent is slow enough.");
    puts("Brave and clever contestant,  win the race to get the flag!");
    int fd = open("/flag", 0);
    read(fd, flag_buf, 0x30);
    pthread_t thread1, thread2;
    printf("please enter the size to output your flag: ");
    scanf("%d", &size);

    puts("please enter the content to read to buffer (max 0x100 bytes): ");
    read(0, p, 0x104);
    sleep(1);
    // Create two threads that run different functions
    pthread_create(&thread1, NULL, do_output, NULL);
    pthread_create(&thread2, NULL, get_thread2_input, p);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    return 0;
}