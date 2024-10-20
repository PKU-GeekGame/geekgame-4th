import random
import base64
from typing import Tuple

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"


class Node:
    a: float
    b: int
    c: "Node"
    d: "Node"
    e: "Node"

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = None
        self.d = None
        self.e = None

class Splay:
    root: Node

    def __init__(self):
        self.root = None

    def splay(self, rhs):
        while rhs.c != None:
            if rhs.c.c == None:
                if rhs == rhs.c.d:
                    self.turn_r(rhs.c)
                else:
                    self.turn_l(rhs.c)
            elif (
                rhs == rhs.c.d
                and rhs.c == rhs.c.c.d
            ):
                self.turn_r(rhs.c.c)
                self.turn_r(rhs.c)
            elif (
                rhs == rhs.c.e
                and rhs.c == rhs.c.c.e
            ):
                self.turn_l(rhs.c.c)
                self.turn_l(rhs.c)
            elif (
                rhs == rhs.c.e
                and rhs.c == rhs.c.c.d
            ):
                self.turn_l(rhs.c)
                self.turn_r(rhs.c)
            else:
                self.turn_r(rhs.c)
                self.turn_l(rhs.c)

    def turn_l(self, x):
        y = x.e
        x.e = y.d
        if y.d != None:
            y.d.c = x
        y.c = x.c
        if x.c == None:
            self.root = y
        elif x == x.c.d:
            x.c.d = y
        else:
            x.c.e = y
        y.d = x
        x.c = y

    def turn_r(self, x):
        y = x.d
        x.d = y.e
        if y.e != None:
            y.e.c = x
        y.c = x.c
        if x.c == None:
            self.root = y
        elif x == x.c.e:
            x.c.e = y
        else:
            x.c.d = y
        y.e = x
        x.c = y

    def insert(self, a, b):
        class_a = Node(a, b)
        cur = self.root
        c = None
        while cur != None:
            c = cur
            if a < cur.a:
                cur = cur.d
            else:
                cur = cur.e
        class_a.c = c
        if c == None:
            self.root = class_a
        elif a < c.a:
            c.d = class_a
        else:
            c.e = class_a
        self.splay(class_a)

def random_splay(class_b: Splay):
    cur: Node = class_b.root
    c = None
    while cur != None:
        c = cur
        if random.randint(0, 1) == 0:
            cur = cur.d
        else:
            cur = cur.e
    class_b.splay(c)

answer = "?" * 36
def trace(cur: Node, truth: bytes, pos: int, depth: int) -> int:
    global answer
    if cur != None:
        x = random.randint(0, 0xFF)
        cur_chr = chr(truth[pos] ^ x)
        answer = answer[:cur.b] + cur_chr + answer[cur.b+1:]
        pos = pos + 1
        if cur.d:
            assert cur.d.a < cur.a
        if cur.e:
            assert cur.a < cur.e.a
        pos = trace(cur.d, truth, pos, depth+1)
        pos = trace(cur.e, truth, pos, depth+1)
    return pos

def solve():
    random.seed("flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}")
    assert random.randint(0, 65535) == 54830
    
    class_b = Splay()

    # input_flag = input("Please enter the flag: ")

    # if len(input_flag) != 36:
    #     print("Try again!")
    #     return
    # if input_flag[:5] != "flag{" or input_flag[-1] != "}":
    #     print("Try again!")
    #     return

    # for char in input_flag:
    #     class_b.insert(random.random(), ord(char))

    for i in range(36):
        class_b.insert(random.random(), i)

    for _ in range(0x100):
        random_splay(class_b)

    # answer = gather_answer(class_b.root)
    # truth = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    final_pos = trace(class_b.root, base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I"), 0, 0)
    print(final_pos)
    print(answer)

    # if answer == truth:
    #     print("You got the flag3!")
    # else:
    #     print("Try again!")


if __name__ == "__main__":
    solve()

