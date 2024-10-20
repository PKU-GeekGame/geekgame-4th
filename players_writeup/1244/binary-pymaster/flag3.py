# This script should be placed with the extracted pycs
from stdlibs import random as fixed_random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"
reference = base64.b64decode(
        "7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
reference_ptr = 0

class Node:
    def __init__(self, priority: float, val: int):
        """priority is a (random) float and val is an char"""
        self.priority = priority
        self.val = val
        """parent is the parent of the node"""
        self.parent = None
        """lch and rch are the left and right children of the node"""
        self.lch = None
        self.rch = None


class Splay:
    def __init__(self):
        self.root = None

    def splay(self, node: Node):
        while node.parent != None:
            if node.parent.parent == None:
                if node == node.parent.lch:
                    self.r_rotate(node.parent)
                else:
                    self.l_rotate(node.parent)
            elif (
                node == node.parent.lch
                and node.parent == node.parent.parent.lch
            ):
                self.r_rotate(node.parent.parent)
                self.r_rotate(node.parent)
            elif (
                node == node.parent.rch
                and node.parent == node.parent.parent.rch
            ):
                self.l_rotate(node.parent.parent)
                self.l_rotate(node.parent)
            elif (
                node == node.parent.rch
                and node.parent == node.parent.parent.lch
            ):
                self.l_rotate(node.parent)
                self.r_rotate(node.parent)
            else:
                self.r_rotate(node.parent)
                self.l_rotate(node.parent)

    def l_rotate(self, cur_parent):
        y = cur_parent.rch
        cur_parent.rch = y.lch
        if y.lch != None:
            y.lch.parent = cur_parent
        y.parent = cur_parent.parent
        if cur_parent.parent == None:
            self.root = y
        elif cur_parent == cur_parent.parent.lch:
            cur_parent.parent.lch = y
        else:
            cur_parent.parent.rch = y
        y.lch = cur_parent
        cur_parent.parent = y

    def r_rotate(self, cur_parent):
        y = cur_parent.lch
        cur_parent.lch = y.rch
        if y.rch != None:
            y.rch.parent = cur_parent
        y.parent = cur_parent.parent
        if cur_parent.parent == None:
            self.root = y
        elif cur_parent == cur_parent.parent.rch:
            cur_parent.parent.rch = y
        else:
            cur_parent.parent.lch = y
        y.rch = cur_parent
        cur_parent.parent = y

    def insert(self, priority: float, val: int):
        new_node = Node(priority, val)
        cur_root = self.root
        parent = None
        while cur_root != None:
            parent = cur_root
            if priority < cur_root.priority:
                cur_root = cur_root.lch
            else:
                cur_root = cur_root.rch
        new_node.parent = parent
        if parent == None:
            self.root = new_node
        elif priority < parent.priority:
            parent.lch = new_node
        else:
            parent.rch = new_node
        self.splay(new_node)


def root_first_traversal(node: Node):
    global reference_ptr
    s = b""
    if node != None:
        r_value = fixed_random.randint(0, 0xFF)
        print(node.val, reference[reference_ptr] ^ r_value)
        reference_ptr += 1
        s += bytes([node.val ^ r_value])
        s += root_first_traversal(node.lch)
        s += root_first_traversal(node.rch)
    return s


def mutate_tree(tree: Splay):
    """
    Randomly walk to a node in the tree and splay it
    """
    cur_node = tree.root
    parent = None
    while cur_node != None:
        parent = cur_node
        if fixed_random.randint(0, 1) == 0:
            cur_node = cur_node.lch
        else:
            cur_node = cur_node.rch
    tree.splay(parent)


def solve():
    # This map is found using input "01234... to main"
    maps = [(55, 95), (53, 114), (108, 108), (73, 116), (57, 114), (48, 89), (84, 89), (123, 123), (81, 80), (68, 89), (75, 82), (79, 95), (78, 70), (50, 85), (66, 51), (49, 79), (103, 103), (77, 111), (83, 65), (82, 76), (125, 125), (71, 64), (80, 115), (51, 95), (72, 83), (76, 95), (74, 101), (102, 102), (97, 97), (52, 65), (56, 55), (67, 108), (69, 95), (65, 117), (54, 69), (70, 109)]
    keys = set(map(lambda x: x[0], maps))
    assert len(keys) == len(maps)
    filtered_maps = [x for x in maps if chr(x[0]) not in "flag{}"]
    filtered_maps.sort(key=lambda x: x[0])
    print("".join(map(lambda x: chr(x[1]), filtered_maps)))

def main():
    assert fixed_random.randint(0, 65535) == 54830

    tree = Splay()

    flag_input = input("Please enter the flag: ")

    if len(flag_input) != 36:
        print("Try again!")
        return
    if flag_input[:5] != "flag{" or flag_input[-1] != "}":
        print("Try again!")
        return

    for input_char in flag_input:
        tree.insert(fixed_random.random(), ord(input_char))

    for _ in range(0x100):
        mutate_tree(tree)

    actual = root_first_traversal(tree.root)
    
    print(actual.hex())
    print(reference.hex())
    if actual == reference:
        print("You got the flag3!")
    else:
        print("Try again!")


if __name__ == "__main__":
    # main()
    solve()
