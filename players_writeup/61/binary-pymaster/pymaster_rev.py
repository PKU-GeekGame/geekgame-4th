import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None


class splay:
    def __init__(self):
        self.root = None

    def splay(self, now):
        while now.parent != None:
            if now.parent.parent == None:
                if now == now.parent.left_child:
                    self.right_rotate(now.parent)
                else:
                    self.left_rotate(now.parent)
            elif (
                now == now.parent.left_child
                and now.parent == now.parent.parent.left_child
            ):
                self.right_rotate(now.parent.parent)
                self.right_rotate(now.parent)
            elif (
                now == now.parent.right_child
                and now.parent == now.parent.parent.right_child
            ):
                self.left_rotate(now.parent.parent)
                self.left_rotate(now.parent)
            elif (
                now == now.parent.right_child
                and now.parent == now.parent.parent.left_child
            ):
                self.left_rotate(now.parent)
                self.right_rotate(now.parent)
            else:
                self.right_rotate(now.parent)
                self.left_rotate(now.parent)

    def left_rotate(self, x):
        y = x.right_child
        x.right_child = y.left_child
        if y.left_child != None:
            y.left_child.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y
        y.left_child = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left_child
        x.left_child = y.right_child
        if y.right_child != None:
            y.right_child.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right_child:
            x.parent.right_child = y
        else:
            x.parent.left_child = y
        y.right_child = x
        x.parent = y

    def insert(self, key, value):
        now = Node(key, value)
        current = self.root
        parent = None
        while current != None:
            parent = current
            if key < current.key:
                current = current.left_child
            else:
                current = current.right_child
        now.parent = parent
        if parent == None:
            self.root = now
        elif key < parent.key:
            parent.left_child = now
        else:
            parent.right_child = now
        self.splay(now)


def first_order(now):
    s = b""
    if now != None:
        s += bytes([random.randint(0, 0xFF)])
        s += first_order(now.left_child)
        s += first_order(now.right_child)
    return s

def first_order_2(now):
    s = b""
    if now != None:
        s += bytes([now.value])
        s += first_order_2(now.left_child)
        s += first_order_2(now.right_child)
    return s


def random_splay(tree):
    current = tree.root
    parent = None
    while current != None:
        parent = current
        if random.randint(0, 1) == 0:
            current = current.left_child
        else:
            current = current.right_child
    tree.splay(parent)


def run():
    random.seed("flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}")

    print(random.randint(0, 65535))

    tree = splay()

    for i in range(36):
        tree.insert(random.random(), i)

    for _ in range(0x100):
        random_splay(tree)

    mask = first_order(tree.root)
    order = first_order_2(tree.root)
    ans = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")

    ans = bytes(bytearray(x ^ y for x, y in zip(ans, mask)))
    answer = b"?" * 36

    for i in range(36):
        print(order[i])
        answer = answer[:order[i]]+ans[i:i+1]+answer[order[i]+1:]
        
    print(answer)

if __name__ == "__main__":
    run()