import base64
import random
import marshal
import zlib
import dis

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"
# flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}

code = marshal.loads(
    base64.b64decode(
        "YwAAAAAAAAAAAAAAAAAAAAAFAAAAQAAAAHMwAAAAZABaAGUBZAGDAWUCZQNkAoMBZAODAmUCZQNkBIMBZAWDAmUAgwGDAYMBAQBkBlMAKQdztAQAAGVKekZWMTFQMnpBVWZhL1UvMkN5bDBSanlCV3NiR2g3R0N2ZFlCMHBHNkFGeEt5MGRkdWdORUg1Z0VRVC8zMTIzQ1NPN1RSdDBiUlVhdFBjYzI5OGo0K3ZyNTNGZ3g5RUlMQzlpYjlvdHh6MmQyU0h1SHZRYnJWYnI4RFV0V2NkOEJGbzlPWlA2c2ZvVTdDUG9xOG42THY5OHhJSHlPeWpvWFU0aDk2elJqM2FyYkZyaHlHd0oyZGZnc3RmcG5WKzFHNEJjazN3RkNEa2VFNkVrRjVZaDd2QUpGZjJEWTBsbEY0bFlvOEN5QWpvVDUwZE1qdXNzVVBxZis1N1dHMkhacE1kRm5aRmhxUFZHZFprZFVvdUxtb2VvSXhhSWFtNDkvbHdUM1BIeFp5TnBickRvbkk0ZWpsVEViZ2tSb21XUENoTzhpZkVLZnlFUkl0YlR4Y0NHTEl2ZGtQVlVPcENYamVFeEM1SlFwZmpOZWVsOFBFbUV0VXFaM1VFUTVIVldpVFZNYlVOdzF2VEFWOU1COXlPRG1tQ042SGpuNm5qNVhSc3FZNm1qT3I4bW9XaFhIYmJydUoxaDY0b2U5ZVZzcGZ3eEtTa1hDWUMvVWxlblZPQlZUS3o3RkZOT1dUR2ZHOUl1TGNVejdLYlNzUmtWY21VYTN0YUFqS3BKZFF6cWEyZG5FVjBsbWFueE1JcU5zMzlrd3BKTEtWVVNibTNCdVdtUUxtWlV3NWx5dUVxeXVGL3BSeXVTK05LeWswRjVYQWp5cE5OT2lCU2hiaDJTdWZRQ25ETWd4a3RKVXJaQ1FsTlJGd3plMHZmRWllMUYxbWY5b0ZEWkozYnFySlNHV3lzcUl0TmRVa09vR29CODNJTUpIVnRwSzB5bmlDeVplTExBaStsek10R0hVTktrbGVseWtWVllMbUcwVGRZbzFyUjNBVnZYNzR2SlBGSG1zYitWUHM5V1FVaGVFM1FhWVJEL2JiQ0xSbm03K1VaWW8vK09GNmt3MTBBazM3ZnVET0VBTXJ4WlBTc2pjeUZIK0FvRGp3UUtwSk5TNWY3UEZtMWF1NjVOU0t0anpYV3hvcDFRUWlWV2VrWVZIQmlJVnB2U1NpVTByd1V1RXc1clJRN3NFQmNUNWZvdXVjamovUmkzeTZlelFuQThSN2lTTmVHTGlhSFI0QzlDQWNnbXVQcy9IZ0V0TUtKY09KaWJzZVpHNVRUL1M2WDFrTkFxZEl1Z3hUWU05dnhkalJPR1d6T1pjSE9iNC9lM3RGUTdLQ3FBVC9nalc4NnpQaXNiZm9pOW1US2h4dVFiTG5ncXByTmNaM29uQWo4aFc3c2tyRk5TZ1lHaHNHL0JkSGdCRHJET2t3NlVMMGxWT1F0elljRDFJdUhTZDBRMEZlMEJtUW4vcjFSOTJDQ3gvNEU2OXJoeWRqOVlRMVB6YkQzT0lpdGI3M2hZSGpqd0xQUndEcCtQN3J3MzMyKzZibjl4NmRqQ3g2T3crNXBUaDAvSjA2bEE3NlNtYmY4R016OHFCREtmakVEZ3RLVk0wVS9EajF5ZS9ZQ0kwUmZwaUcwSUdhRU5GSEVQYXJidjV1T0tGVT3aBGV4ZWPaBHpsaWLaCmRlY29tcHJlc3PaBmJhc2U2NNoJYjY0ZGVjb2RlTikE2gRjb2Rl2gRldmFs2gdnZXRhdHRy2gpfX2ltcG9ydF9fqQByCQAAAHIJAAAA2gDaCDxtb2R1bGU+AQAAAHMKAAAABAEGAQwBEP8C/w=="
    )
)
print(dis.dis(code))
code = b"eJzFV11P2zAUfa/U/2Cyl0RjyBWsbGh7GCvdYB0pG6AFxKy0ddugNEH5gEQT/3123CSO7TRt0bRUatPcc298j4+vr53Fgx9EILC9ib9otxz2d2SHuHvQbrVbr8DUtWcd8BFo9OZP6sfoU7CPoq8n6Lv98xIHyOyjoXU4h96zRj3arbFrhyGwJ2dfgstfpnV+1G4Bck3wFCDkeE6EkF5Yh7vAJFf2DY0llF4lYo8CyAjoT50dMjussUPqf+57WG2HZpMdFnZFhqPVGdZkdUouLmoeoIxaIam49/lwT3PHxZyNpbrDonI4ejlTEbgkRomWPChO8ifEKfyERItbTxcCGLIvdkPVUOpCXjeExC5JQpfjNeel8PEmEtUqZ3UEQ5HVWiTVMbUNw1vTAV9MB9yODmmCN6Hjn6nj5XRsqY6mjOr8moWhXHbbruJ1h64oe9eVspfwxKSkXCYC/UlenVOBVTKz7FFNOWTGfG9IuLcUz7KbSsRkVcmUa3taAjKpJdQzqa2dnEV0lmanxMIqNs39kwpJLKVUSbm3BuWmQLmZUw5lyuEqyuF/pRyuS+NKyk0F5XAjypNNOiBShbh2SufQCnDMgxktJUrZCQlNRFwze0vfEie1F1mf9oFDZJ3bqrJSGWysqItNdUkOoGoB83IMJHVtpK0yniCyZeLLAi+lzMtGHUNKklelykVVYLmG0TdYo1rR3AVvX74vJPFHmsb+VPs9WQUheE3QaYRD/bbCLRnm7+UZYo/+OF6kw10Ak37fuDOEAMrxZPSsjcyFH+AoDjwQKpJNS5f7PFm1au65NSKtjzXWxop1QQiVWekYVHBiIVpvSSiU0rwUuEw5rRQ7sEBcT5fouucjj/Ri3y6ezQnA8R7iSNeGLiaHR4C9CAcgmuPs/HgEtMKJcOJibseZG5TT/S6X1kNAqdIugxTYM9vxdjROGWzOZcHOb4/e3tFQ7KCqAT/gjW86zPisbfoi9mTKhxuQbLngqprNcZ3onAj8hW7skrFNSgYGhsG/BdHgBDrDOkw6UL0lVOQtzYcD1IuHSd0Q0Fe0BmQn/r1R92CCx/4E69rhydj9YQ1PzbD3OIitb73hYHjjwLPRwDp+P7rw332+6bn9x6djCx6Ow+5pTh0/J06lA76Smbf8GMz8qBDKfjEDgtKVM0U/Dj1ye/YCI0RfpiG0IGaENFHEParbv5uOKFU="
print(zlib.decompress(base64.b64decode(code)).decode())

cypher = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")


class Node:
    def __init__(self, value, key):
        self.value = value
        self.key = key
        self.fa = None
        self.left = None
        self.right = None


class Splay:
    def __init__(self):
        self.root = None

    def splay(self, node):
        while node.fa != None:
            if node.fa.fa == None:
                if node == node.fa.left:
                    self.rotate_right(node.fa)
                else:
                    self.rotate_left(node.fa)
            elif node == node.fa.left and node.fa == node.fa.fa.left:
                self.rotate_right(node.fa.fa)
                self.rotate_right(node.fa)
            elif node == node.fa.right and node.fa == node.fa.fa.right:
                self.rotate_left(node.fa.fa)
                self.rotate_left(node.fa)
            elif node == node.fa.right and node.fa == node.fa.fa.left:
                self.rotate_left(node.fa)
                self.rotate_right(node.fa)
            else:
                self.rotate_right(node.fa)
                self.rotate_left(node.fa)

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.fa = x
        y.fa = x.fa
        if x.fa == None:
            self.root = y
        elif x == x.fa.left:
            x.fa.left = y
        else:
            x.fa.right = y
        y.left = x
        x.fa = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.fa = x
        y.fa = x.fa
        if x.fa == None:
            self.root = y
        elif x == x.fa.right:
            x.fa.right = y
        else:
            x.fa.left = y
        y.right = x
        x.fa = y

    def insert(self, value, key):
        node = Node(value, key)
        cur = self.root
        fa = None
        while cur != None:
            fa = cur
            if value < cur.value:
                cur = cur.left
            else:
                cur = cur.right
        node.fa = fa
        if fa == None:
            self.root = node
        elif value < fa.value:
            fa.left = node
        else:
            fa.right = node
        self.splay(node)


def get(node):
    s = b""
    if node != None:
        s += bytes([node.key ^ random.randint(0, 0xFF)])
        s += get(node.left)
        s += get(node.right)
    return s


def walk(node):
    s = []
    if node != None:
        s.append(node.key)
        s += walk(node.left)
        s += walk(node.right)
    return s


def random_splay(tree):
    cur = tree.root
    fa = None
    while cur != None:
        fa = cur
        if random.randint(0, 1) == 0:
            cur = cur.left
        else:
            cur = cur.right
    tree.splay(fa)


tree = Splay()

random.seed("flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}")
assert random.randint(0, 0xFFFF) == 54830
for i in range(36):
    tree.insert(random.random(), i)
for _ in range(0x100):
    random_splay(tree)
tmp = walk(tree.root)
cypher = list(cypher)
for i in range(36):
    cypher[i] ^= random.randint(0, 0xFF)
flag = "".join([chr(cypher[tmp.index(i)]) for i in range(36)])
print("flag3:", flag)
# flag{YOU_ArE_7ru3lY_m@SteR_oF_sPLAY}
