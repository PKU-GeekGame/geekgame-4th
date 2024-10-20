import base64
import random


class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def balance(self, current_node):
        while current_node.parent is not None:
            if current_node.parent.parent is None:
                if current_node == current_node.parent.left:
                    self.rotate_right(current_node.parent)
                else:
                    self.rotate_left(current_node.parent)
            elif (
                current_node == current_node.parent.left
                and current_node.parent == current_node.parent.parent.left
            ):
                self.rotate_right(current_node.parent.parent)
                self.rotate_right(current_node.parent)
            elif (
                current_node == current_node.parent.right
                and current_node.parent == current_node.parent.parent.right
            ):
                self.rotate_left(current_node.parent.parent)
                self.rotate_left(current_node.parent)
            elif (
                current_node == current_node.parent.right
                and current_node.parent == current_node.parent.parent.left
            ):
                self.rotate_left(current_node.parent)
                self.rotate_right(current_node.parent)
            else:
                self.rotate_right(current_node.parent)
                self.rotate_left(current_node.parent)

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def add_node(self, key, value):
        new_node = TreeNode(key, value)
        current = self.root
        parent = None
        while current is not None:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self.balance(new_node)


def traverse_and_xor(node):
    result = b""
    if node is not None:
        result += bytes([node.value ^ random.randint(0, 0xFF)])
        result += traverse_and_xor(node.left)
        result += traverse_and_xor(node.right)
    return result


def random_balance(tree):
    current = tree.root
    parent = None
    while current is not None:
        parent = current
        if random.randint(0, 1) == 0:
            current = current.left
        else:
            current = current.right
    tree.balance(parent)


def main():
    tree = BinaryTree()

    flag_input = input("Please enter the flag: ")
    # flag_input = "flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"

    if len(flag_input) != 36:
        print("Try again!")
        return
    if flag_input[:5] != "flag{" or flag_input[-1] != "}":
        print("Try again!")
        return

    for char in flag_input:
        tree.add_node(random.random(), ord(char))

    for _ in range(0x100):
        random_balance(tree)

    encoded_tree = traverse_and_xor(tree.root)
    expected_result = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    if encoded_tree == expected_result:
        print("You got the flag!")
    else:
        print("Try again!")


if __name__ == "__main__":
    main()
