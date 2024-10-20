import random
import base64

random.seed("flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}")
_ = random.randint(0, 65535)
assert _ == 54830

class Item:
  def __init__(self, weight: float, value: int):
    self.weight: float = weight
    self.value: int = value
    self.parent: Item = None
    self.left: Item = None
    self.right: Item = None


class Tree:
  def __init__(self):
    self.root: Item = None

  def rebalance(self, item: Item):
    while item.parent != None:
      if item.parent.parent == None:
        if item == item.parent.left:
          self.turn_right(item.parent)
        else:
          self.turn_left(item.parent)
      elif item == item.parent.left and item.parent == item.parent.parent.left:
        self.turn_right(item.parent.parent)
        self.turn_right(item.parent)
      elif item == item.parent.right and item.parent == item.parent.parent.right:
        self.turn_left(item.parent.parent)
        self.turn_left(item.parent)
      elif item == item.parent.right and item.parent == item.parent.parent.left:
        self.turn_left(item.parent)
        self.turn_right(item.parent)
      else:
        self.turn_right(item.parent)
        self.turn_left(item.parent)

  def turn_left(self, x: Item):
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

  def turn_right(self, x: Item):
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

  def insert(self, weight: float, value: int):
    alpha_1: Item = Item(weight, value)
    alpha_2: Item = self.root
    alpha_3: Item = None
    while alpha_2 != None:
      alpha_3 = alpha_2
      if weight < alpha_2.weight:
        alpha_2 = alpha_2.left
      else:
        alpha_2 = alpha_2.right
    alpha_1.parent = alpha_3
    if alpha_3 == None:
      self.root = alpha_1
    elif weight < alpha_3.weight:
      alpha_3.left = alpha_1
    else:
      alpha_3.right = alpha_1
    self.rebalance(alpha_1)


def tree_to_bytes(item: Item) -> bytes:
  s = b""
  if item != None:
    s += bytes([item.value ^ random.randint(0, 0xFF)])
    s += tree_to_bytes(item.left)
    s += tree_to_bytes(item.right)
  return s


def edit_tree(tree: Tree):
  current = tree.root
  item = None
  while current != None:
    item = current
    if random.randint(0, 1) == 0:
      current = current.left
    else:
      current = current.right
  tree.rebalance(item)


def print_tree(item: Item) -> bytes:
  s = b""
  if item != None:
    s += bytes([item.value])
    s += print_tree(item.left)
    s += print_tree(item.right)
  return s


tree = Tree()
flag = "flag{0123456789ABCDEFGHIJKLMNOPQRST}"

for char in flag:
  tree.insert(random.random(), ord(char))

for _ in range(0x100):
  edit_tree(tree)

my_result = tree_to_bytes(tree.root)
true_result = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")

tree_bytes = print_tree(tree.root)
indexes = [flag.index(chr(i)) for i in tree_bytes]
xor_result = bytes([a ^ b ^ c for a, b, c in zip(tree_bytes, my_result, true_result)])
new_flag = list(flag)
for i, index in enumerate(indexes):
  new_flag[index] = chr(xor_result[i])
print("".join(new_flag))
