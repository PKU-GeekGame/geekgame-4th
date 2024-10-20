import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"


class Node:
    def __init__(self, rnd, ord_ch):
        self.rnd = rnd
        self.ord_ch = ord_ch
        self.par = None
        self.L = None
        self.R = None

# Splay
class Tree:
    def __init__(self):
        self.root = None

    def Tree(self, node):
        while node.par != None:
            if node.par.par == None:
                if node == node.par.L:
                    self.Node(node.par)
                else:
                    self.Node_2(node.par)
            elif (
                node == node.par.L
                and node.par == node.par.par.L
            ):
                self.Node(node.par.par)
                self.Node(node.par)
            elif (
                node == node.par.R
                and node.par == node.par.par.R
            ):
                self.Node_2(node.par.par)
                self.Node_2(node.par)
            elif (
                node == node.par.R
                and node.par == node.par.par.L
            ):
                self.Node_2(node.par)
                self.Node(node.par)
            else:
                self.Node(node.par)
                self.Node_2(node.par)

    def Node_2(self, x):
        y = x.R
        x.R = y.L
        if y.L != None:
            y.L.par = x
        y.par = x.par
        if x.par == None:
            self.root = y
        elif x == x.par.L:
            x.par.L = y
        else:
            x.par.R = y
        y.L = x
        x.par = y

    def Node(self, x):
        y = x.L
        x.L = y.R
        if y.R != None:
            y.R.par = x
        y.par = x.par
        if x.par == None:
            self.root = y
        elif x == x.par.R:
            x.par.R = y
        else:
            x.par.L = y
        y.R = x
        x.par = y

    def Insert(self, rnd, ord_ch):
        new_node = Node(rnd, ord_ch)
        cur_node = self.root
        par = None
        while cur_node != None:
            par = cur_node
            if rnd < cur_node.rnd:
                cur_node = cur_node.L
            else:
                cur_node = cur_node.R
        new_node.par = par
        if par == None:
            self.root = new_node
        elif rnd < par.rnd:
            par.L = new_node
        else:
            par.R = new_node
        self.Tree(new_node)


def FrontOrder(node):
    s = []
    if node != None:
        s.append((node.ord_ch, random.randint(0, 0xFF)))
        s += FrontOrder(node.L)
        s += FrontOrder(node.R)
    return s


def Rand_Splay(tr):
    cur_node = tr.root
    par = None
    while cur_node != None:
        par = cur_node
        if random.randint(0, 1) == 0:
            cur_node = cur_node.L
        else:
            cur_node = cur_node.R
    tr.Tree(par)


def Mian():
    tr = Tree()

    """
    flag = input("Please enter the flag: ")

    if len(flag) != 36:
        print("Try again!")
        return
    if flag[:5] != "flag{" or flag[-1] != "}":
        print("Try again!")
        return
    """

    for i in range(36):
        tr.Insert(random.random(), i)

    for _ in range(0x100):
        Rand_Splay(tr)

    res = FrontOrder(tr.root)
    cur_node = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")

    answer = [0] * 36
    for i in range(36):
        answer[res[i][0]] = cur_node[i] ^ res[i][1]
    for i in range(36):
        print(chr(answer[i]), end="")


if __name__ == "__main__":
    random.seed('flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}')
    assert random.randint(0, 65535) == 54830
    Mian()
