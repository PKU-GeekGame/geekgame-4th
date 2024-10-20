#include <stdio.h>
#include <stdlib.h>
void init()
{
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    setbuf(stderr, 0);
}
struct Node
{
    int key;
    char *data;
    int siz;
    struct Node *left, *right, *parent, *same_vals;
} *root;
void insert()
{
    struct Node *new_node = (struct Node *)malloc(sizeof(struct Node));
    new_node->left = new_node->right = new_node->parent = new_node->same_vals = 0;
    puts("please enter the node key");
    scanf("%d", &new_node->key);
    puts("please enter the size of the data");
    scanf("%d", &new_node->siz);
    puts("please enter the data");
    new_node->data = (char *)malloc(new_node->siz);
    read(0, new_node->data, new_node->siz);
    if (root == 0)
    {
        root = new_node;
        return;
    }
    struct Node *cur = root;
    while (1)
    {
        if (cur->key == new_node->key)
        {
            if (cur->same_vals == NULL)
            {
                cur->same_vals = new_node;
                return;
            }
            cur = cur->same_vals;
        }
        else if (cur->key > new_node->key)
        {
            if (cur->left == NULL)
            {
                cur->left = new_node;
                new_node->parent = cur;
                return;
            }
            cur = cur->left;
        }
        else
        {
            if (cur->right == NULL)
            {
                cur->right = new_node;
                new_node->parent = cur;
                return;
            }
            cur = cur->right;
        }
    }
}
void show()
{
    printf("please enter the key of the node you want to show\n");
    int key;
    scanf("%d", &key);
    struct Node *cur = root;
    while (cur != NULL)
    {
        if (cur->key == key)
        {
            puts("the data of the node is: ");
            write(1, cur->data, cur->siz);
            return;
        }
        else if (cur->key > key)
        {
            cur = cur->left;
        }
        else
        {
            cur = cur->right;
        }
    }
    printf("oops! the key is not found\n");
}
void remove_tree()
{
    printf("please enter the key of the node you want to remove\n");
    int key;
    scanf("%d", &key);
    struct Node *cur = root;
    while (cur != NULL)
    {
        if (cur->key == key)
        {
            if (cur->same_vals != NULL)
            {
                // free the first one
                struct Node *temp = cur->same_vals;
                temp->left = cur->left;
                temp->right = cur->right;
                free(cur->data);
                free(cur);
                return;
            }
            if (cur->left == NULL && cur->right == NULL)
            {
                if (cur->parent == NULL)
                {
                    root = NULL;
                    free(cur->data);
                    free(cur);
                    return;
                }
                if (cur->parent->left == cur)
                {
                    cur->parent->left = NULL;
                }
                else
                {
                    cur->parent->right = NULL;
                }
                free(cur->data);
                free(cur);
                return;
            }
            if (cur->left == NULL)
            {
                if (cur->parent == NULL)
                {
                    root = cur->right;
                    free(cur->data);
                    free(cur);
                    return;
                }
                if (cur->parent->left == cur)
                {
                    cur->parent->left = cur->right;
                }
                else
                {
                    cur->parent->right = cur->right;
                }
                free(cur->data);
                free(cur);
                return;
            }
            if (cur->right == NULL)
            {
                if (cur->parent == NULL)
                {
                    root = cur->left;
                    free(cur->data);
                    free(cur);
                    return;
                }
                if (cur->parent->left == cur)
                {
                    cur->parent->left = cur->left;
                }
                else
                {
                    cur->parent->right = cur->left;
                }
                free(cur->data);
                free(cur);
                return;
            }
            struct Node *temp = cur->right;
            while (temp->left != NULL)
            {
                temp = temp->left;
            }
            cur->key = temp->key;
            void *old_data = cur->data;
            cur->data = temp->data;
            cur->siz = temp->siz;
            if (temp->parent->left == temp)
            {
                temp->parent->left = temp->right;
            }
            else
            {
                temp->parent->right = temp->right;
            }
            free(old_data);
            free(temp);
            return;
        }
        else if (cur->key > key)
        {
            cur = cur->left;
        }
        else
        {
            cur = cur->right;
        }
    }
    printf("oops! the key is not found\n");
}
void change_data()
{
    printf("please enter the key of the node you want to change its data\n");
    int key;
    scanf("%d", &key);
    struct Node *cur = root;
    while (cur != NULL)
    {
        if (cur->key == key)
        {
            puts("please enter the new data");
            read(0, cur->data, cur->siz);
            return;
        }
        else if (cur->key > key)
        {
            cur = cur->left;
        }
        else
        {
            cur = cur->right;
        }
    }
    printf("oops! the key is not found\n");
}
void caidan()
{
    puts("welcome to the Tree of Pwn, please choose the operation you want to do to this tree");
    puts("1. insert a node");
    puts("2. show the data of a node");
    puts("3. remove a node");
    puts("4. change the data of a node");
    puts("5. exit");
    printf(">> ");
}
int main()
{
    init();
    while (1)
    {
        caidan();
        int op;
        scanf("%d", &op);
        switch (op)
        {
        case 1:
            insert();
            break;
        case 2:
            show();
            break;
        case 3:
            remove_tree();
            break;
        case 4:
            change_data();
            break;
        case 5:
            puts("bye bye");
            return 0;
        default:
            puts("invalid operation");
        }
    }
}