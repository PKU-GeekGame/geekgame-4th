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

int node_cnt = 0;	// 0x404120
int node_tops[0x80];

void insert(char *l) {
	puts("please enter the node key");
	int key;	// var_14h
	scanf("%d", &key);
	puts("please enter the size of the data");
	int size;	// var_18h
	scanf("%d", &size);

	int last_top;	// var_4h
	if (node_cnt == 0) {
		last_top = 0;
	} else {
		last_top = node_tops[obj.node_cnt-1];
	}

	int new_top = 0x18 + size + last_top;
	if (new_top > 0x200) {
		puts("no enough space");
		return;
	}

	node_tops[obj.node_cnt] = new_top;
	node_cnt = 1 + node_cnt;

	char* var_10h = l + last_top;
	*var_10h = key;
	*(var_10h+0x10) = 0x18 + size;
	*(var_10h+8) = var_10h + 0x18;

	puts("please enter the data");
	read(0, *(var_10h+8), *(var_10h+0x10));
}

void show(char* l) {
	puts("please enter the key of the node you want to show:");
	int key;	// var_14h
	scanf("%d", &key);
	if (node_cnt > 0) {
		print_node(l);
	}
	int i = 1;	// var_4h
	while (i < node_cnt) {
		int rdx = node_tops[i-1];
		char* var_10h = l + rdx;
		if (key == *var_10h) {
			print_node(var_10h);
			return;
		} else {
			i++;
		}
	}
}

int main() {
	init();
	char l[0x200];
	while (1) {
		print_info();
		int op;
		scanf("%d", &op);
		if (op == 1) {
			insert(l);
		} else if (op == 2) {
			show(l);
		} else if (op == 3) {
			// edit();
			puts("sorry not implemented");
		} else {
			return 0;
		}
	}
}