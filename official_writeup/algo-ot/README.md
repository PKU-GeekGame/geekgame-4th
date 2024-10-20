# [Algorithm] 不经意的逆转

- 命题人：unprintable123
- 🗝 简单开个锁️：200 分
- 🔒🔒🔒🔒🔒：300 分

## 题目描述

<blockquote>
<p>如今，法院为了提升收视率推出的卡牌对决庭审再次面临热度骤降的危机。</p>
<p>为了拯救庭审，刚刚学完密码学基础的审判长灵机一动，提出了全新规则——<strong><ruby>不经意<rt>Oblivious</rt></ruby><ruby>证言<rt>Testimony</rt></ruby></strong>。</p>
<p>简单来说，辩方会从证人处选择一张<ruby>卡牌<rt>证言</rt></ruby>，但辩方不知道其它<ruby>卡牌<rt>证言</rt></ruby>的内容，证人也不知道辩方获得了哪一张<ruby>卡牌<rt>证言</rt></ruby>。</p>
</blockquote>
<p>但不管规则怎么改，房租还是要交的。律师小陈还是普通地接下了案子后普通地站上了辩论席，<strong>不经意</strong>地抽取了<ruby>卡牌<rt>证言</rt></ruby>，然后普通地看到了证人身上的心灵枷锁。在检察官小剑的帮助下，小陈成功解开了证人的心灵枷锁，而等待他的是——更多的锁！</p>
<p>于是，束手无策的小陈来到了现在你所在的地方，告诉了你上面这些离谱的设定。聪明的你，能否<strong><ruby>不经意<rt>Oblivious</rt></ruby>地找出关键的🗝</strong>，为小陈表演一个华丽的逆转？</p>
<p><strong>提示：</strong></p>
<ul>
<li>Flag 2：看看 <a target="_blank" rel="noopener noreferrer" href="https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/">Coppersmith</a></li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Flag 1：想办法找到一个 mod q 对但是 mod p 不对的式子，以及别忘了 $(a^d)^e\equiv a\pmod{n}$
<li>Flag 2：作者解法的其中一行是<code>f=poly.small_roots(X=2**1024, beta=0.49, epsilon=0.04)[0]</code>，具体参数的解释可以看<a target="_blank" rel="noopener noreferrer" href="https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots">Sage Reference Manual</a></li>
</ul>
</div>

**[【附件：下载题目源码（algo-ot.py）】](attachment/algo-ot.py)**

**【终端交互：连接到题目】**

## 预期解法

本题实现了一个基本的不经意传输（Oblivious Transfer）协议，但其安全性保证仍然受限于传输信息的性质。例如[这个](https://github.com/USTC-Hackergame/hackergame2020-writeups/blob/master/official/%E4%B8%8D%E7%BB%8F%E6%84%8F%E4%BC%A0%E8%BE%93/README.md)和[这个](https://github.com/EggRoll-Taiyaki/My-CTF-Challenges/tree/main/idekCTF/2022/Decidophobia)。

### Flag 1

第一问预期有两个做法，一个是直接分解 n，另一个是用第二问的做法。

首先我们可以得到 $(p+q)^d\equiv p^d+q^d\pmod n$。因此，如果我们能够直接拿到两条信息，直接作差再跟 n 算 gcd 即可获得 q。但在加上 $(x-v_0)^d$ 这一项后，上述做法不再可行。

一个尝试是通过设置 $v$ 抵消 $v-x_0$ 和 $v-x_1$ 。如果想要获取 $m_0+km_1$ ，需要解方程 $v-x_0+k^e(v-x_1)\equiv0\pmod n$。
不幸的是（~~实际上是出题人故意的~~）， $k=-1$ 时 $v$ 无解，故不可能作差消去此项。

但这真的意味着我们无法处理 $(v-x_0)^d$ 吗？在不经意传输中，为了让传输者无法分辨接收方获取了哪条信息，接收方会随机选取 $v=x_0+k^e$，利用 $(k^e)^d\equiv k\pmod n$ 的性质，计算 $m_0=v_0-k$ 得到其中一条信息。
而反过来，这也意味着不论我们选了什么都可以计算 $(v-x_0)^d$ 的 $e$ 次方，获得 $(v-x_0)\equiv (v_0-m_0)^e\pmod{n}$。

一般情况下我们没法在不分解 n 时解高次方程，但本问的两条信息之差是 q 的倍数。故我们可以发$v=x_1$，作差消去 f 后获得 $(x_1-x_0)^d+2q^d\equiv v_0-v_1\pmod n$。
从而获得 $(x_1-x_0)\equiv(v_0-v_1-2q^d)^e\equiv(v_0-v_1)^e\pmod q$。显然这对 $\bmod p$ 并不成立，与 n 算 gcd 即可获得 q，之后随便做。

### Flag 2

这一问更改了信息，导致就算我们把两条信息全拿到也没法分解 n。
但注意到题目设置的 f 是固定的，这给了我们进行[Broadcast Attack](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/#basic-broadcast-attack)的可能性。

对于任何一个低次的模数方程，Coppersmith Method 可以在解很小时把模数方程提升为实数域上的方程，从而二分即可求解。且所有 $\bmod n$ 下进行操作在 $\bmod p$ 下也仍然成立，故就算我们不知道 p 也可以通过 $\bmod n$ 找到一个系数足够小的多项式，把它提升为实数域上的方程。

基于 Broadcast Attack 的想法，我们应当想办法每一次获得一个 f 的方程，然后把这些方程凑一起满足 coppersmith 的小整数解要求。但由于 e 太大，第一问的解法并没有什么用。
这里我们需要想起之前的第一个尝试，选择 $v=\frac{x_0+x_1}{2}$ 把两个式子加起来，获得 $2p^d+f+\frac{1}{f}\equiv v_0+v_1\pmod{n}$ 。

于是我们获得了一个在 $\bmod p$ 下成立的模数方程。通过中国剩余定理我们可以将这些方程拼成一个模数足够大的方程，使 f 满足 coppersmith 的小整数解限制。
本题的 f 大约为 $2^{1024}$ ，然后每个 conn 都可以获得一个 2048 bit 的 n，根据 coppersmith 我们需要 $\lceil\frac{1024}{2048\cdot(0.125-\epsilon)}\rceil$ 次连接。

```python
polys, ns = zip(*[run_once() for _ in range(6)])
MOD = prod(ns)
b = crt([poly.list()[1] for poly in polys], list(ns))

R = PolynomialRing(Zmod(MOD), 'x')
x = R.gen()
poly = x**2 + 1 + b * x
f = poly.small_roots(X=2**1024, beta=0.49, epsilon=0.04)[0]
```
