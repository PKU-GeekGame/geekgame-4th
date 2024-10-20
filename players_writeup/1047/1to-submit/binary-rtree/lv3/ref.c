#include <stdio.h>

void init() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

void print_info() {
	puts("welcome to the Tree of Pwn, please choose the operation you want to do to this tree");
	puts("1. insert a node");
	puts("2. show the data of a node");
	puts("3. remove a node");
	puts("4. change the data of a node");
	puts("5. exit");
	puts(">>");
}

struct Node {
	int key;	// +0
	void* data;
	int size;	// +0x10
	Node* l;	// +0x18
	Node* r;	// +0x20
	Node* fa;	// +0x28
	Node* eq;	// +0x30
};

Node* root = NULL;

void insert() {
	// NOTE. No canary
	Node* new_node = (Node*)malloc(0x38);	// var_8h
	new_node->l = new_node->r = new_node->fa = new_node->eq = NULL;

	puts("please enter the node key");
	scanf("%d", &new_node->key);

	puts("please enter the size of the data");
	scanf("%d", &new_node->size);

	puts("please enter the data");
	void* data_buf = malloc(new_node->size);
	new_node->data = data_buf;
	read(0, data_buf, new_node->size);

	if (root == NULL) {
		root = new_node;
		return;
	}

	Node* cur = root;	// var_10h
	while(1) {
		if (new_node->key == cur->key) {
			if (cur->eq == NULL) {
				cur->eq = new_node;
				// NOTE `fa` not set!
				return;
			} else {
				cur = cur->eq;
			}
		} else {
			if (new_node->key < cur->key) {
				if (cur->l == NULL) {
					cur->l = new_node;
					new_node->fa = cur;
					return;
				} else {
					cur = cur->l;
				}
			} else {
				if (cur->r == NULL) {
					cur->r = new_node;
					new_node->fa = cur;
					return;
				} else {
					cur = cur->r;
				}
			}
		}
	}
}

void show() {
	// NOTE. Have canary
	puts("please enter the key of the node you want to show");
	int key;	// var_14h
	scanf("%d", &key);
	Node* cur = root;	// var_10h
	while(cur) {
		if (cur->key != key) {
			if (key < cur->key) {
				cur = cur->l;
			} else {
				cur = cur->r;
			}
		} else {
			puts("the data of the node is");
			write(1, cur->data, cur->size);
			return;
		}
	}
	puts("oops, the key is not found");
}

void edit() {
	// NOTE Have canary
	puts("please enter the key of the node you want to change its data");
	int key;	// var_14h
	scanf("%d", &key);
	Node* cur = root;	// var_10h
	while(cur) {
		if (cur->key == key) {
			puts("please enter the new data");
			read(0, cur->data, cur->size);
			return;
		} else {
			if (key < cur->key) {
				cur = cur->l;
			} else {
				cur = cur->r;
			}
		}
	}
	puts("oops, the key is not found");
}

void remove() {
	// NOTE Have canary
	puts("please enter the key of the node you want to remove");
	int key;	// var_2ch
	scanf("%d", &key);
	Node* cur = root;	// var_28h
	while(cur) {
		if (cur->key == key) {
			if (cur->eq != NULL) {
				// TODO
				Node* nxt = cur->eq;	// var_10h
				nxt->l = cur->l;
				nxt->r = cur->r;
				// NOTE Did not set `fa` of cur->l and cur->r
				// NOTE Did not set `l` or `r` of cur->fa
				free(cur->data);
				free(cur);
			} else if (cur->l == NULL && cur->r == NULL) {
				if (cur->fa == NULL) {
					root = NULL;
				} else {
					if (cur->fa->l == cur) {
						cur->fa->l = NULL;
					} else {
						cur->fa->r = NULL;
					}
				}
				free(cur->data);
				free(cur);
			} else {
				// 16a2
				if (cur->l == NULL) {
					if (cur->fa == NULL) {
						root = cur->r;
					} else {
						// 16f0
						if (cur->fa->l == cur) {
							cur->fa->l = cur->r;
						} else {
							cur->fa->r = cur->r;
						}
					}
					free(cur->data);
					free(cur);
				} else if (cur->r == NULL) {
					// 174d
					if (cur->fa == NULL) {
						root = cur->l;
					} else {
						if (cur->fa->l == cur) {
							cur->fa->l = cur->l;
						} else {
							cur->fa->r = cur->l;
						}
					}
					free(cur->data);
					free(cur);
				} else {
					// 17f8
					Node* t = cur->r;	// var_20h
					while(t->l) {
						t = t->l;
					}
					cur->key = t->key;
					int old_data = cur->data;	// var_18h
					cur->data = t->data;
					cur->size = t->size;
					if (t->fa->l == t) {
						t->fa->l = t->r;
					} else {
						t->fa->r = t->r;
					}
					free(old_data);
					free(t);
				}
			}
			return;
		} else {
			if (key < cur->key) {
				cur = cur->l;
			} else {
				cur = cur->r;
			}
		}
	}
	puts("oops, the key is not found");
}

int main() {
	init();
	while (true) {
		int op;
		scanf("%d", &op);
		if (op == 1) {
			// Insert
			insert();
		} else if (op == 2) {
			// show
			show();
		} else if (op == 3) {
			// delete
			delete();
		} else if (op == 4) {
			edit();
		} else if (op == 5) {
			break;
		} else {
			puts("invalid choice");
		}
	}
}