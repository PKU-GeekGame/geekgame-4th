import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"

class Node:
    def __init__(self, order, val):
        self.order = order
        self.val = val
        self.parent = None
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def move_to_root(self, node):
        # print("node is: ", node)
        while node.parent != None:
            if node.parent.parent == None: # 如果父节点是根节点，跟父节点交换位置
                if node == node.parent.left:
                    self.swap_with_left_child(node.parent)
                else:
                    self.swap_with_right_child(node.parent)
            elif (
                node == node.parent.left
                and node.parent == node.parent.parent.left
            ):
                # '''
                #     x                   y
                #    /                   /   
                #   y   .      ->       z   .
                #  /                   /   
                # z   .               x   .
                # '''
                self.swap_with_left_child(node.parent.parent)
                self.swap_with_left_child(node.parent)
            elif (
                node == node.parent.right
                and node.parent == node.parent.parent.right
            ):
                self.swap_with_right_child(node.parent.parent)
                self.swap_with_right_child(node.parent)
            elif (
                node == node.parent.right
                and node.parent == node.parent.parent.left
            ):
                # '''
                #     x                   z
                #    /                   /   
                #   y   .      ->       x   .
                #  /                   /   
                # .   z               .   y
                # '''
                self.swap_with_right_child(node.parent)
                self.swap_with_left_child(node.parent)
            else:
                self.swap_with_left_child(node.parent)
                self.swap_with_right_child(node.parent)
    
    '''
       x                y
      /        ->      /  
     .   y            .   x
    '''
    def swap_with_right_child(self, x):
        y = x.right
        x.right = y.left   # x.right = x.right.left
        if y.left != None:
            y.left.parent = x   # x.right.left.parent = x
        y.parent = x.parent   # x.right.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def swap_with_left_child(self, x):
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

    def add_node(self, order, val):
        new_node = Node(order, val)
        node = self.root
        parent = None
        while node != None:
            parent = node
            if order < node.order:
                node = node.left
            else:
                node = node.right
        new_node.parent = parent
        if parent == None:
            self.root = new_node
        elif order < parent.order:
            parent.left = new_node
        else:
            parent.right = new_node
        self.move_to_root(new_node)


# 先序遍历获取整个树上的数据（每次 xor 随机值）
def cal_bytes(node):
    s = b""
    if node != None:
        s += bytes([node.val ^ random.randint(0, 0xFF)])
        s += cal_bytes(node.left)
        s += cal_bytes(node.right)
    return s

def shuffle(tree):
    node = tree.root
    leaf = None
    # 随机找到一个叶子节点
    while node != None:
        leaf = node
        if random.randint(0, 1) == 0:
            node = node.left
        else:
            node = node.right
    tree.move_to_root(leaf)


def main_function():
    tree = Tree()

    user_input = input("Please enter the flag: ")

    if len(user_input) != 36:
        print("Try again! length error.")
        return
    if user_input[:5] != "flag{" or user_input[-1] != "}":
        print("Try again! syntax error.")
        return

    for ch in user_input:
        tree.add_node(random.random(), ord(ch))

    for _ in range(0x100):
        shuffle(tree)

    bytes = cal_bytes(tree.root)
    ans = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    if bytes == ans:
        print("You got the flag3!")
    else:
        print("Try again! result error.")


if __name__ == "__main__":
    main_function()