import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"
# flag3 = "flag{YOU_ArE_7ru3lY_m@SteR_oF_sPLAY}"


class Node:
    def __init__(self, value, key):
        self.value = value
        self.key = key
        self.fa = None
        self.left = None
        self.right = None


class Splay:
    def __init__(self):
        self.root = None

    def splay(self, node):
        while node.fa != None:
            if node.fa.fa == None:
                if node == node.fa.left:
                    self.rotate_right(node.fa)
                else:
                    self.rotate_left(node.fa)
            elif node == node.fa.left and node.fa == node.fa.fa.left:
                self.rotate_right(node.fa.fa)
                self.rotate_right(node.fa)
            elif node == node.fa.right and node.fa == node.fa.fa.right:
                self.rotate_left(node.fa.fa)
                self.rotate_left(node.fa)
            elif node == node.fa.right and node.fa == node.fa.fa.left:
                self.rotate_left(node.fa)
                self.rotate_right(node.fa)
            else:
                self.rotate_right(node.fa)
                self.rotate_left(node.fa)

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.fa = x
        y.fa = x.fa
        if x.fa == None:
            self.root = y
        elif x == x.fa.left:
            x.fa.left = y
        else:
            x.fa.right = y
        y.left = x
        x.fa = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.fa = x
        y.fa = x.fa
        if x.fa == None:
            self.root = y
        elif x == x.fa.right:
            x.fa.right = y
        else:
            x.fa.left = y
        y.right = x
        x.fa = y

    def insert(self, value, key):
        node = Node(value, key)
        cur = self.root
        fa = None
        while cur != None:
            fa = cur
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        node.fa = fa
        if fa == None:
            self.root = node
        elif value < fa.value:
            fa.left = node
        else:
            fa.right = node
        self.splay(node)


def get(node):
    s = b""
    if node != None:
        s += bytes([node.key ^ random.randint(0, 0xFF)])
        s += get(node.left)
        s += get(node.right)
    return s


def random_splay(tree):
    cur = tree.root
    fa = None
    while cur != None:
        fa = cur
        if random.randint(0, 1) == 0:
            cur = cur.left
        else:
            cur = cur.right
    tree.splay(fa)


def check_the_flag():
    tree = Splay()

    flag = input("Please enter the flag: ")

    if len(flag) != 36:
        print("Try again!")
        return
    if flag[:5] != "flag{" or flag[-1] != "}":
        print("Try again!")
        return

    for chr in flag:
        tree.insert(random.random(), ord(chr))

    for _ in range(0x100):
        random_splay(tree)

    tmp = get(tree.root)
    print(base64.b64encode(tmp))


if __name__ == "__main__":
    print(random.randint(0, 0xFFFF))
    check_the_flag()
