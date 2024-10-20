import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OFselfY7h0n}"


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.parent = None
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def bubble(self, node):
        #   while node.parent != None:
        #       if node == node.parent.left:
        #           self.rotate_right(node.parent)
        #       else:
        #           self.rotate_left(node.parent)
        while node.parent != None:
            if node.parent.parent == None:
                if node == node.parent.left:
                    self.rotate_right(node.parent)
                else:
                    self.rotate_left(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self.rotate_right(node.parent.parent)
                self.rotate_right(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self.rotate_left(node.parent.parent)
                self.rotate_left(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.left:
                self.rotate_left(node.parent)
                self.rotate_right(node.parent)
            else:
                self.rotate_right(node.parent)
                self.rotate_left(node.parent)

    #       x               y
    #      / \             / \
    #     L   y     ->    x   R
    #        / \         / \
    #       C   R       L   C
    def rotate_left(self, x):
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

    #       x             y
    #      / \           / \
    #     y   R    ->   L   x
    #    / \               / \
    #   L   C             C   R
    def rotate_right(self, x):
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

    def insert(self, key, val):
        new_node = Node(key, val)
        iter = self.root
        temp = None
        while iter != None:
            temp = iter
            if key < iter.key:
                iter = iter.left
            else:
                iter = iter.right
        new_node.parent = temp
        if temp == None:
            self.root = new_node    # tree empty, insert directly
        elif key < temp.key:
            temp.left = new_node
        else:
            temp.right = new_node
        self.bubble(new_node)


def preorder(node):
    s = b""
    if node != None:
        s += bytes([node.val ^ random.randint(0, 0xFF)])
        s += preorder(node.left)
        s += preorder(node.right)
    return s


def poke(tree):
    iter = tree.root
    temp = None
    while iter != None:
        temp = iter
        if random.randint(0, 1) == 0:
            iter = iter.left
        else:
            iter = iter.right
    tree.bubble(temp)

def main(userinput):
    random.randint(0,65535)
    tree = Tree()

    if len(userinput) != 36:
        #print("Try again!")
        return
    # if userinput[:5] != "flag{" or userinput[-1] != "}":
    #     #print("Try again!")
    #     return

    for ch in userinput:
        tree.insert(random.random(), ord(ch))

    for _ in range(0x100):
        poke(tree)

    print(' '.join(f'{c:02x}' for c in preorder(tree.root)))

    if preorder(tree.root) == base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I"):
        pass #print("You got the flag3!")
    else:
        pass #print("Try again!")

    return preorder(tree.root)


if __name__ == "__main__":
    main(input())
