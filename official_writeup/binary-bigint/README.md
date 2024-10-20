# [Binary] 大整数类

- 命题人：debugger
- Flag 1：350 分
- Flag 2：300 分

## 题目描述

<p>10 年前，小 Z 是一个 OIer。小 Z 找了一个大整数类模板，这个模板支持大整数比较、加法、减法、乘法（<strong>包括大整数和大整数相乘、大整数和小整数相乘</strong>）、取余。</p>
<p>小 Z 用这个模板写了一个<strong>检查 Flag 的程序，</strong>但是代码已经找不到了。现在请你来分析一下这个程序到底做了什么。</p>
<p><strong>提示：</strong></p>
<ul>
<li>这个大整数类模板支持存储最多 1200 个十进制位的整数，但是存储一个大整数需要 4804 字节。</li>
<li>程序使用的加密算法有常见的攻击手段和现成的利用工具。</li>
<li>使用有动态调试功能的工具会更有帮助。</li>
<li>压缩包里面的 Linux 和 Windows 可执行文件是用相同的源代码编译生成的。程序没有使用任何混淆手段。或许 Linux 程序会比较容易逆向一些。</li>
<li>此题有彩蛋，但是不会计入比赛分数。你只需要提交能使程序两问输出 Correct 的 flag 就可以解出本题。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>这里有<a target="_blank" rel="noopener noreferrer" href="/service/attachment/binary-bigint/binary-bigint-new.zip">带符号的程序</a>，可能对你会有帮助。</li>
<li>觉得程序里面的字符串有点奇怪？看看<a target="_blank" rel="noopener noreferrer" href="https://www.freepascal.org/docs-html/ref/refsu9.html#:~:text=the%20length%20is%20stored">这里</a>。另外，其实大整数类的实现和字符串的存储方法存在某种相似之处。</li>
<li>“现成的利用工具”指的是<a target="_blank" rel="noopener noreferrer" href="https://github.com/RsaCtfTool/RsaCtfTool">RsaCtfTool</a>。</li>
</ul>
</div>

**[【附件：下载题目附件（binary-bigint.zip）】](attachment/binary-bigint.zip)**

**[【附件：下载带符号的题目附件（binary-bigint-new.zip）】](attachment/binary-bigint-new.zip)**

## 预期解法

此题是一个用Pascal写的大整数模板，实际上是用从网上随便找的一个版本简单改写得到的。

预期需要选手完成以下步骤：
* 找到主函数（通过搜索字符串即可知道主函数）。
* 知道字符串的存储格式（第一个字节表示长度）。
* 因为没有符号，选手需要区分哪个函数是内置的库函数，哪个是真正用来处理字符串的函数。
* 知道了处理字符串的函数之后，分析出哪个是大整数比较、加法、减法、乘法的函数，以及字符串转大整数的过程。注意没有用于判断相等的函数，而是用x<=y且y<=x来判断x和y是否相等。
* 还原出程序的大整数操作。

Flag 1会把输入的flag拆成3个部分，然后每个部分转成整数都调用一个函数，三个调用都返回true则返回Flag正确。而checkflag1函数会计算一个大整数的三次函数，三次方程有三个根，选手需要把系数提取出来，然后有众多工具（SageMath、sympy、Mathematica均可）可以得到方程的根。

Flag 2会把flag转成整数后自乘16次再和flag相乘，每步操作后都和一个常数m取余，最后把结果和另一个常数v比较。这里实现了一个RSA。使用<a target="_blank" rel="noopener noreferrer" href="https://github.com/RsaCtfTool/RsaCtfTool">RsaCtfTool</a>可以把m分解。此后还原回flag是显然的。

本题旧版本还有一个Flag 3（后来因为flag太多而且程序也无法给出反馈删了），输入flag后会计算flag^2+m，然后直接退出。实际上m可以分解成两个素数k+flag和k-flag的积，如果你输入的flag是正确的计算出来的结果会是平方数，但是这个模板没有开平方根的功能。这也是Fermat分解方法的原理：当两个素数大小接近时，你可以先找到比m大的最小平方数，然后减去m，如果得到的是平方数，那么m是两个平方数的差，因此可以分解。