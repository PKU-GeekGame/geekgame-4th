#include <stdio.h>
#include <stdlib.h>
void init()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
    puts("welcome to the rtree system!");
    puts("in this level, we consider when every node in the tree has not more than one child, the tree becomes a linked list");
    puts("It's time to construct your own tree!");
}

void backdoor()
{
    system("echo 'this is a fake backdoor'");
}
void edit(char *buffer, int size)
{
    puts("sry, but you can only edit 8 bytes at a time");
    puts("please enter the index of the data you want to edit:");
    int index;
    scanf("%d", &index);
    if (index >= size)
    {
        puts("invalid index");
        return;
    }
    puts("please enter the new data:");
    read(0, buffer + index, 8);
    puts("edit success!");
}
struct Node
{
    int key;
    char *data;
    int siz;
    size_t edit;
    struct Node *next;
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
struct Node *root;
int main()
{
    init();
    while (1)
    {
        print_info();
        int op;
        scanf("%d", &op);
        if (op == 1)
        {
            struct Node *new_node = (struct Node *)malloc(sizeof(struct Node));
            puts("please enter the node key:");
            scanf("%d", &new_node->key);
            puts("please enter the size of the data:");
            scanf("%d", &new_node->siz);
            if (new_node->siz <= 8)
            {
                printf("sry, but plz enter a bigger size\n");
            }
            new_node->data = (char *)malloc(new_node->siz);
            puts("please enter the data:");
            read(0, new_node->data, new_node->siz);
            new_node->edit = (size_t)edit;
            new_node->next = NULL;
            puts("insert success!");
            if (root == NULL)
            {
                root = new_node;
            }
            else
            {
                struct Node *cur = root;
                while (cur->next != NULL)
                {
                    cur = cur->next;
                }
                cur->next = new_node;
            }
        }
        else if (op == 2)
        {
            puts("please enter the key of the node you want to show:");
            int key;
            scanf("%d", &key);
            struct Node *cur = root;
            while (cur != NULL)
            {
                if (cur->key == key)
                {
                    print_node(cur);
                    break;
                }
                cur = cur->next;
            }
            if (cur == NULL)
            {
                puts("node not found :(");
            }
        }
        else if (op == 3)
        {
            puts("please enter the key of the node you want to edit:");
            int key;
            scanf("%d", &key);
            struct Node *cur = root;
            while (cur != NULL)
            {
                if (cur->key == key)
                {
                    if (cur->edit)
                    {
                        ((void (*)(char *, int))cur->edit)(cur->data, cur->siz);
                        cur->edit = 0;
                    }
                    break;
                }
                else
                {
                    cur = cur->next;
                }
            }
            if (cur == NULL)
            {
                puts("node not found");
            }
        }
        else if (op == 4)
        {
            break;
        }
        else
        {
            puts("invalid choice");
        }
    }
}