# [Algorithm] 随机数生成器

- 命题人：debugger
- C++：150 分
- Python：200 分
- Go：200 分

## 题目描述

<p>这里有个神秘的随机数生成器。但是，生成的随机数是真的随机的吗？是不是把 Flag 也藏在里面了？</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>本题环境分别使用 <code>g++ (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0</code> 和 <code>go version go1.20.14 linux/amd64</code> 编译。题目附件中的编译产物与题目环境相同。</li>
<li>如果需要自行编译 Go 程序，请<strong>务必</strong>使用 go1.20 编译，使用其他版本可能会导致你无法正常做题。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>C++：如果不知道C++的随机数生成原理，可以看看<a target="_blank" rel="noopener noreferrer" href="https://www.mathstat.dal.ca/~selinger/random/">这里</a>。但是因为随机数种子只有2^32种可能，本题还有更简单的做法。</li>
<li>Python：Python的随机数是<a target="_blank" rel="noopener noreferrer" href="https://github.com/kmyk/mersenne-twister-predictor">可以预测的</a>——一个块（32 bit）的值只与它之前第 624、623、227 个块有关。你可以试试改一下每个块的最低位，看看哪个块对预测的结果影响最大。</li>
<li>Go：可以看看<a target="_blank" rel="noopener noreferrer" href="https://github.com/PKU-GeekGame/geekgame-2nd/blob/master/official_writeup/sweeper2/sol/gorand.py">Go随机数的实现</a>（只需关注uint64和int63函数的实现即可，uint32就是int63()&gt;&gt;31）。预期解是先要找到flag的长度，然后构造线性方程组。</li>
</ul>
</div>

**[【附件：下载题目源码（algo-randomzoo.zip）】](attachment/algo-randomzoo.zip)**

**【终端交互：连接到第一关（C++）】**

**【终端交互：连接到第二关（Python）】**

**【终端交互：连接到第三关（Go）】**

## 预期解法
注意：本题还有其他解法，可见选手wp。此处仅给出出题人的解法。

此题给了一个程序，可以生成一串随机数，但是其中每个随机数都加上了flag的一个字节。

### C++
C++程序用了srand初始化随机数种子。因为srand的参数是32位整数，直接枚举即可。参见sol/exp1.cpp。

C++使用的LFG随机数生成器也是可以预测的，预测方法和下面Go一节类似，这里不再给出具体实现。

### Python
Python的随机数是用MT19937生成的，一个块（32 bit）的值只与它之前第 624、623、227 个块有关。我们不知道每个块的具体值，但是知道tempering之后再加上flag字节的值，所以可以枚举两个块对应的flag字节，从而得到可能的原始的块的具体值。可以尝试改变每个块的tempering之后的值，看看对预测结果有什么变化：
```
def tempering(y):
    y ^= (y >> 11)
    y ^= (y <<  7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    return y

def untempering(y):
    y ^= (y >> 18)
    y ^= (y << 15) & 0xefc60000
    y ^= ((y <<  7) & 0x9d2c5680) ^ ((y << 14) & 0x94284000) ^ ((y << 21) & 0x14200000) ^ ((y << 28) & 0x10000000)
    y ^= (y >> 11) ^ (y >> 22)
    return y

def generate(v_623,v_227):
    y = 0 | (v_623 & 0x7fffffff)
    z1 = v_227 ^ (y >> 1) ^ [0x0, 0x9908b0df][y & 0x1]
    y = 0x80000000 | (v_623 & 0x7fffffff)
    z2 = v_227 ^ (y >> 1) ^ [0x0, 0x9908b0df][y & 0x1]
    return z1, z2

k1=1234567890
k2=987654321
k3=tempering(generate(untempering(k1),untempering(k2))[0])

s=[]
for i1 in range(-127,128):
    for i2 in range(-127,128):
        z1, z2=generate(untempering(k1+i1),untempering(k2+i2))
        z1=tempering(z1)-k3
        z2=tempering(z2)-k3
        if -128<=z1<=128:
            s.append((i1,i2,z1))
        if -128<=z2<=128:
            s.append((i1,i2,z2))

print(s)
print([i[0] for i in s])
```

从这个程序的运行结果可见，改变v_623对预测结果的影响显著大于v_227，或者说其实只要知道某个块和前面第623、227个块加上flag字节并tempering后的结果，就能得到前面第623个块对应的flag字节。如果假设每个块都是可见字符，每个字符需要枚举量不超过128^3。参见sol/exp2.py。
### Go

Go里面随机数用的是64位的块，且每个块等于前面第607和第273个块的和（舍弃进位）。接着int63会把最高位加到最低位，得到63位随机数。uint32只取int63的最高32位。

设第i个uint32为`random[i]`，有`random[i-273]+random[i-607]-random[i]`为0、-1、2^32、2^32-1之一。再设`flag[i]`为flag的第i个字节（循环），则生成的数为`nums[i]=random[i]+flag[i]`，从而`(nums[i-273]+nums[i-607]-nums[i]+c)%2^32=(flag[i-273]+flag[i-607]-flag[i]+c-k)`，其中c为某个数使得`flag[i-273]+flag[i-607]-flag[i]+c`永远大于0，k为0或1。`(nums[i-273]+nums[i-607]-nums[i]+c)%2^32`是一个大约以flag长度为周期的数列，可以用auto correlation等方法找出其周期（直接试也行）。找出周期（设为n）后，可以列出`flag[(i-273)%n]+flag[(i-607)%n]-flag[i%n]`的方程组并解出flag。参见sol/exp3.py。
