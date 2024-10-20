#include <stdio.h>
#include <stdlib.h>
void init()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    puts("welcome to the rtree system!");
}
void backdoor()
{
    puts("congratulations! you reach the backdoor!");
    system("/bin/sh");
}
struct Node
{
    int key;
    char *data;
    int siz;
};
void print_node(struct Node *node)
{
    printf("key: %d\n", node->key);
    printf("size: %d\n", node->siz);
    printf("data: %s\n", node->data);
}
void print_info()
{
    puts("1. insert a node");
    puts("2. show a node");
    puts("3. edit a node");
    puts("4. quit");
    puts(">> ");
}
int node_tops[0x20];
int node_cnt;
void insert(char *stack_buf)
{
    puts("please enter the node key:");
    int key;
    scanf("%d", &key);
    puts("please enter the size of the data:");
    int siz;
    scanf("%d", &siz);
    int cur_top = (node_cnt == 0 ? 0 : node_tops[node_cnt - 1]);
    if (cur_top + siz + sizeof(struct Node) > 0x200)
    {
        puts("no enough space");
        return;
    }
    node_tops[node_cnt++] = siz + sizeof(struct Node) + cur_top;
    struct Node *new_node = (struct Node *)(stack_buf + cur_top);
    new_node->key = key;
    new_node->siz = siz + sizeof(struct Node);
    new_node->data = (char *)(new_node + 1);
    puts("please enter the data:");
    read(0, new_node->data, new_node->siz);
    puts("insert success!");
}
void show(char *stack_buf)
{
    puts("please enter the key of the node you want to show:");
    int key;
    scanf("%d", &key);
    if (node_cnt > 0)
    {
        print_node(stack_buf);
    }
    for (int i = 1; i < node_cnt; i++)
    {
        struct Node *cur = (struct Node *)(stack_buf + node_tops[i - 1]);
        if (cur->key == key)
        {
            print_node(cur);
            return;
        }
    }
}
void edit()
{
    puts("sorry, not implemented :(");
}
int main()
{
    init();
    char stack_buf[0x200];
    node_cnt = 0;
    while (1)
    {
        print_info();
        int choice;
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            insert(stack_buf);
            break;
        case 2:
            show(stack_buf);
            break;
        case 3:
            edit();
            break;
        default:
            break;
        }
        if (choice == 4)
        {
            break;
        }
    }
    return 0;
}