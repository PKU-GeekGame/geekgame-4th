# import random
import random as rnd
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"

random = rnd.Random('flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}')

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


def retrieve(node: Node) -> bytes:
    s: bytes = b""
    if node != None:
        s += bytes([node.value ^ random.randint(0, 0xFF)])
        s += retrieve(node.left)
        s += retrieve(node.right)
    return s


def shake(tree: Tree):
    node = tree.root
    OO0O = None
    while node != None:
        OO0O = node
        if random.randint(0, 1) == 0:
            node = node.left
        else:
            node = node.right
    tree.balance(OO0O)


def main():
    tree = Tree()

    flag = input("Please enter the flag: ")

    if len(flag) != 36:
        print("Try again!")
        return
    if flag[:5] != "flag{" or flag[-1] != "}":
        print("Try again!")
        return

    for byte in flag:
        tree.insert(random.random(), ord(byte))

    for _ in range(0x100):
        shake(tree)

    rearranged_flag = retrieve(tree.root)
    flag_checksum = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    if rearranged_flag == flag_checksum:
        print("You got the flag3!")
    else:
        print("Try again!")


if __name__ == "__main__":
    main()
