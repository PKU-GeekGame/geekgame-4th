# import random
import random as rnd

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"

random = rnd.Random('flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}')

random.randint(0, 65535)

class Node:
    def __init__(self, key: float, value: int):
        self.key = key
        self.value: int = value
        self.parent: Node | None = None
        self.left: Node | None = None
        self.right: Node | None = None


class Tree:
    def __init__(self):
        self.root: Node | None = None

    def balance(self, node: Node):
        while node.parent != None:
            if node.parent.parent == None:
                if node == node.parent.left:
                    self.zag(node.parent)
                else:
                    self.zig(node.parent)
            elif (
                node == node.parent.left
                and node.parent == node.parent.parent.left
            ):
                self.zag(node.parent.parent)
                self.zag(node.parent)
            elif (
                node == node.parent.right
                and node.parent == node.parent.parent.right
            ):
                self.zig(node.parent.parent)
                self.zig(node.parent)
            elif (
                node == node.parent.right
                and node.parent == node.parent.parent.left
            ):
                self.zig(node.parent)
                self.zag(node.parent)
            else:
                self.zag(node.parent)
                self.zig(node.parent)

    def zig(self, x: Node):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def zag(self, x: Node):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key: float, value: int):
        new = Node(key, value)
        node = self.root
        new_parent = None
        while node != None:
            new_parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        new.parent = new_parent
        if new_parent == None:
            self.root = new
        elif key < new_parent.key:
            new_parent.left = new
        else:
            new_parent.right = new
        self.balance(new)

retr_random_list = []

def retrieve(node: Node) -> list[int]:
    l = []
    if node != None:
        rand_v = random.randint(0, 0xFF)
        retr_random_list.append(rand_v)
        l.append(node.value)
        l += retrieve(node.left)
        l += retrieve(node.right)
    return l


def shake(tree: Tree):
    node = tree.root
    new = None
    while node != None:
        new = node
        if random.randint(0, 1) == 0:
            node = node.left
        else:
            node = node.right
    tree.balance(new)


def main():
    tree = Tree()

    """
    flag = input("Please enter the flag: ")

    if len(flag) != 36:
        print("Try again!")
        return
    if flag[:5] != "flag{" or flag[-1] != "}":
        print("Try again!")
        return
    """

    flag = list(range(36))
        
    key_pool = [random.random() for _ in range(len(flag))]

    for key, char in zip(key_pool, flag):
        # tree.insert(key, ord(char))
        tree.insert(key, char)

    for _ in range(0x100):
        shake(tree)

    rearrange_index = retrieve(tree.root)
    # flag_checksum = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    flag_checksum = b"\xec\x47\x25\x45\x83\xc8\x3a\xc0\xef\x2e\xe6\x0a\x0c\xf2\xcf\x66\x2d\x09\x6c\xb6\x01\xf5\xb4\x28\xf0\x26\x43\x94\x5b\xf0\x05\x8d\x3b\x72\xce\x88"
    flag_chars = ['0'] * 36
    for index, b, salt in zip(rearrange_index, flag_checksum, retr_random_list):
        flag_chars[index] = (b ^ salt)
    print(flag_chars)


if __name__ == "__main__":
    main()
