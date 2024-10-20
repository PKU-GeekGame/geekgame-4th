#include <stdio.h>

void init() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
	puts("welcome to the rtree system");
}

void print_info() {
	puts("1. insert a node");
	puts("2. show a node");
	puts("3. edit a node");
	puts("4. quit");
	puts(">>");
}

void edit(void* data, int size) {
	char* s = (char*)data;
	// size in var_1ch
	puts("sorry, but you can only edit 8 bytes at a time");
	puts("please enter the index of the data you want to edit");
	int index;	// var_ch
	scanf("%d", &index);
	if (index < size) {	// negative ?
		puts("please enter the new data");
		read(0, s+index, 8);
		puts("edit success");
	} else {
		puts("invalid index");
	}
}

struct Node {
	int key;
	void* data;	// +0x8
	int size;	// +0x10
	void* edit_func_ptr;	// +0x18
	Node* next;		// +0x20
};

Node* root = NULL;

int main() {
	init();
	while (true) {
		int op;
		scanf("%d", &op);
		if (op == 1) {
			// Insert
			Node* cur_node = (Node*)malloc(0x28);	// var_10h
			puts("please enter the node key");
			scanf("%d", &cur_node->key);
			puts("please enter the size of the data");
			scanf("%d", &cur_node->size);
			if (cur_node->size <= 8) {
				puts("sry, but plz enter a bigger size");
				// didn't reject
			}
			void* data = malloc(cur_node->size);	// var_18h
			cur_node->data = data;
			puts("please enter the data");
			read(0, cur_node->data, cur_node->size);
			// set edit_func_ptr to edit
			cur_node->t = NULL;
			puts("insert success");

			if (root == NULL) {
				root = cur_node;
			} else {
				Node* cur = root;	// 0x28
				while (cur->next) {
					cur = cur->next;
				}
				cur->next = cur_node;
			}
		} else if (op == 2) {
			// show
			puts("please enter the key of the node you want to show");
			int key;	// var_2ch
			scanf("%d", &key);
			Node* cur = root;	// var_20h
			while (cur) {
				if (cur->key == key) {
					print_node(cur);
					break;
				}
				cur = cur->next;
			}
			if (!cur) {
				puts("node not found");
			}
		} else if (op == 3) {
			// edit
			puts("please enter the key of the node you want to edit");
			int key;	// var_2ch
			scanf("%d", &key);
			Node* cur = root;	// var_18h
			while (cur) {
				if (cur->key == key) {
					if (cur->edit_func_ptr != NULL) {
						// call edit_func_ptr with %rdi = cur->data, %esi = cur->size
						break;
					}
					cur->edit_func_ptr = NULL;
					break;
				}
				cur = cur->next;
			}
			if (!cur) {
				puts("node not found");
			}
		} else if (op == 4) {
			// Check stack
			return 0;
		} else {
			puts("invalid choice");
		}
	}
}