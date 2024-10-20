# [Algorithm] 打破复杂度

- 命题人：Yasar
- 关于SPFA—它死了：200 分
- Dinic并非万能：200 分

## 题目描述

<blockquote>
<p>众所周知，复杂度的计算是复杂的。</p>
</blockquote>
<p>小 Y 最近在学习图论，老师教了他如何计算图论算法的复杂度。</p>
<p>但是他发现平时使用这些算法的时候，情况有所不同，它们大多都运行得非常快，时常优于其理论复杂度。</p>
<p>于是，长久以来，他变得相信可以“一招鲜，吃遍天”，直到有一天……</p>
<p><center><p>
    <img src="media/algo-complexity-death_of_spfa.webp" style="max-width: 100%; max-height: 400px">
    <br><span style="opacity: 0.6">↑ 此图在二压后码率减小了 85%，插图清晰度变糊不是你的错觉</span>
</p></center></p>
<p>和毒瘤出题人签订契约，<strong>卡掉 SPFA 和 Dinic 算法</strong>吧。</p>
<p><strong>补充说明：</strong></p>
<ul>
<li>请上传符合代码要求的输入格式的原始输入文件，不需要打包成压缩包。输入长度限制为 200KB。</li>
<li>如果提示 “Internal System Error” 或 “Runtime Error” 可能是因为程序的 assert 没有通过，请检查输入格式；如果提示 “Time Limit Exceeded” 可能是因为输入不完整（例如输入末尾缺少回车），导致程序卡在 <code>cin</code>。</li>
</ul>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>SPFA 和 Dinic 算法好像都是多轮更新的算法，如何让更新轮数达到理论极限呢？</li>
<li>SPFA 和 Dinic 算法好像都基于路径边数来判断局部最优路径，如何让这种贪心失效呢？</li>
</ul>
</div>

**【网页链接：访问题目网页】**

## 预期解法

本题并没有想要为难选手，在目标设置上较为宽松。~~下次有机会可以出个 KoH 让大家卷（bushi~~

### 算法分析

~~众所周知，“有问题，上知乎”。~~

- SPFA：[https://www.zhihu.com/question/292283275](https://www.zhihu.com/question/292283275)
- Dinic：[https://www.zhihu.com/question/266149721](https://www.zhihu.com/question/266149721)

SPFA 算法和 Dinic 算法都使用基于队列实现的 BFS 来作为每轮更新的依据。
这种更新方式假设了经过的边数越少的路径为较优路径，在大多数图中这种方式都能显著降低更新的轮数。
但是只需要打破这一点，让更新轮数增加，就能让两个算法逼近理论上的最坏时间复杂度。

出题人的做法对 SPFA 构造网格图，对 Dinic 则构造多轮的二分图完全匹配。

## Exp

```python
import random

edge = []
n = 10
m = 200
for i in range(n):
    for j in range(m):
        if j < m - 1:
            edge.append((i * m + j, i * m + j + 1, 100 + (-1) ** j * i * 3))
        if i < n - 1:
            edge.append((i * m + j, (i + 1) * m + j, 1))
print(n * m, len(edge))
with open("spfa.txt", "w") as f:
    print(n * m, len(edge), "1", n * m, file=f)
    for u, v, w in edge:
        print(u + 1, v + 1, w, file=f)

edge = []
n = 100
k = n // 3
p = n // 12 - 1
s = 1
t = k * 2 + p * 4 + 2
for i in range(k):
    edge.append((s, i + 2, k))
    edge.append((k + 2 + i, t, k))

for i in range(k):
    for j in range(k):
        edge.append((i + 2, k + j + 2, 1))

edge.append((s, k * 2 + 2, k * k * p))
edge.append((k * 2 + 2, k * 2 + 3, k * k * p))
edge.append((k * 2 + 2 + p * 2, t, k * k * p))
edge.append((k * 2 + 3 + p * 2, k * 2 + 2 + p * 2, k * k * p))
for i in range(k):
    edge.append((k * 2 + 3, k + 2 + i, k))
    edge.append((i + 2, k * 2 + 3 + p * 2, k))

for j in range(1, p):

    edge.append((k * 2 + 1 + j * 2, k * 2 + 2 + j * 2, k * k * p))
    edge.append((k * 2 + 2 + j * 2, k * 2 + 3 + j * 2, k * k * p))
    edge.append((k * 2 + 2 + p * 2 + j * 2, k * 2 + 1 + p * 2 + j * 2, k * k * p))
    edge.append((k * 2 + 3 + p * 2 + j * 2, k * 2 + 2 + p * 2 + j * 2, k * k * p))
    if j & 1:
        for i in range(k):
            edge.append((k * 2 + 3 + j * 2, 2 + i, k))
            edge.append((k + i + 2, k * 2 + 3 + p * 2 + j * 2, k))
    else:
        for i in range(k):
            edge.append((k * 2 + 3 + j * 2, k + 2 + i, k))
            edge.append((i + 2, k * 2 + 3 + p * 2 + j * 2, k))

print(t, len(edge))
with open("dinic.txt", "w") as f:
    print(t, len(edge), s, t, file=f)
    for u, v, w in edge:
        print(u, v, w, file=f)
```