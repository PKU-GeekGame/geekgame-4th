# import random
random = __import__('random2') # use modified random module
# seems that the modified random.random() returns the same value every time the program is run
# anyway, use the modified random module to solve the challenge

# copy random.pyc to ./random2.pyc before running this prog

import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"


class node:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.f = None
        self.l = None
        self.r = None

keys = []

class Tree:
    def __init__(self):
        self.root = None

    def splay(self, u):
        while u.f != None:
            if u.f.f == None:
                if u == u.f.l:
                    self.rightRotate(u.f)
                else:
                    self.leftRotate(u.f)
            elif (u == u.f.l and u.f == u.f.f.l):
                self.rightRotate(u.f.f)
                self.rightRotate(u.f)
            elif (u == u.f.r and u.f == u.f.f.r):
                self.leftRotate(u.f.f)
                self.leftRotate(u.f)
            elif (u == u.f.r and u.f == u.f.f.l):
                self.leftRotate(u.f)
                self.rightRotate(u.f)
            else:
                self.rightRotate(u.f)
                self.leftRotate(u.f)

    def leftRotate(self, x):
        y = x.r
        x.r = y.l
        if y.l != None:
            y.l.f = x
        y.f = x.f
        if x.f == None:
            self.root = y
        elif x == x.f.l:
            x.f.l = y
        else:
            x.f.r = y
        y.l = x
        x.f = y

    def rightRotate(self, x):
        y = x.l
        x.l = y.r
        if y.r != None:
            y.r.f = x
        y.f = x.f
        if x.f == None:
            self.root = y
        elif x == x.f.r:
            x.f.r = y
        else:
            x.f.l = y
        y.r = x
        x.f = y

    def insert(self, a, b):
        v = node(a, b)
        u = self.root
        f = None
        while u != None:
            f = u
            if a < u.a:
                u = u.l
            else:
                u = u.r
        v.f = f
        if f == None:
            self.root = v
        elif a < f.a:
            f.l = v
        else:
            f.r = v
        self.splay(v)


def getDfsSequence(u):
    ids, rands = [], b""
    if u != None:
        ids.append(u.b)
        rands += bytes([random.randint(0, 255)])
        il, rl = getDfsSequence(u.l)
        ir, rr = getDfsSequence(u.r)
        ids += il + ir
        rands += rl + rr
    return ids, rands


def shuffle(tree):
    u = tree.root
    v = None
    while u != None:
        v = u
        if random.randint(0, 1) == 0:
            u = u.l
        else:
            u = u.r
    tree.splay(v)


def main():
    if (random.randint(0, 65535) == 54830):
        print("It behave right")
    else:
        print("It behave wrong")

    tree = Tree()

    # input_flag = input("Please enter the flag: ")

    # if len(input_flag) != 36:
    #     print("Try again!")
    #     return
    # if input_flag[:5] != "flag{" or input_flag[-1] != "}":
    #     print("Try again!")
    #     return

    input_flag = "".join(chr(i) for i in range(36))

    for c in input_flag:
        tree.insert(random.random(), ord(c))

    for _ in range(0x100):
        shuffle(tree)

    # bin_out = getDfsSequence(tree.root)
    ids, rand_out = getDfsSequence(tree.root)
    bin_ans = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    assert(len(rand_out) == len(bin_ans))

    bin_xor = bytes([rand_out[i] ^ bin_ans[i] for i in range(len(rand_out))])
    # rearrange the xor-ed bytes by ids
    bin_out = bytes([bin_xor[ids.index(i)] for i in range(36)])
    print(bin_out)

    # if bin_out == bin_ans:
    #     print("You got the flag3!")
    # else:
    #     print("Try again!")


if __name__ == "__main__":
    main()
