#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

char flag_buf[64];
char p[0x104], buf[0x104];
char output_buf[0x104];
int size;


void* get_thread2_input(void *a1)
{
  puts("please enter the size to read to the buffer:");
  scanf("%d", &size);
  if ( size <= 49 )
  {
    memcpy(&buf, a1, size);
    puts("input success!\n");
  }
  else
  {
    puts("the size read to the buffer is too large");
  }
}

void* do_output(void* _)
{
  if ( size <= 4 )
  {
    if ( size > 0 )
    {
      if ( (int)strlen(flag_buf) <= 48 )
      {
        usleep(0);
        puts("copying the flag...");
        memcpy(output_buf, flag_buf, size);
        puts(output_buf);
      }
      else
      {
        puts("what happened?");
      }
    }
    else
    {
      puts("invalid output size!!");
    }
  }
  else
  {
    puts("output size is too large");
  }
}

int
main()
{
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);

  puts("for racecar drivers, there are two things to hope for: one is that you "
       "drive fast enough, and the other is that the "
       "opponent is slow enough.");
  puts("Brave and clever contestant,  win the race to get the flag!");
  int fd = open("flag", 0);
  read(fd, flag_buf, 0x30uLL);
  printf("please enter the size to output your flag: ");
  scanf("%d", &size);
  puts("please enter the content to read to buffer (max 0x100 bytes): ");
  read(0, &p, 0x104uLL);
  sleep(1u);
  pthread_t in, out;
  pthread_create(&out, NULL, do_output, NULL);
  pthread_create(&in, NULL, get_thread2_input, p);
  pthread_join(out, NULL);
  pthread_join(in, NULL);
  return 0;
}
