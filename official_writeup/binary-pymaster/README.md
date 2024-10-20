# [Binary] 从零开始学Python

- 命题人：Yasar
- 源码中遗留的隐藏信息：200 分
- 影响随机数的神秘力量：150 分
- 科学家获得的实验结果：200 分

## 题目描述

<blockquote>
<p>杰弗里·辛顿 (Geoffrey Hinton)，在 2018 年因其在深度学习方面的贡献，获得了图灵奖这一计算机领域内的最富盛名的奖项。
2024 年他获得了诺贝尔物理学奖，以表彰在使用人工神经网络实现机器学习方面奠基性发现和发明。
他表示自己完全没有想到这样的事情会发生。</p>
<p>荒诞的世界变得更加荒诞，也许未来某一天，计算机科学也将不复存在！</p>
</blockquote>
<p>2991 年，距离 Python 发布已经过去了 1000 年。</p>
<p>小 Y 在一台历史悠久的电脑上找到了一个尘封已久的程序，好像是个特殊的校验器。
程序在几百年后的电脑上已经无法运行，但是电脑上遗留的一些实验日志记录了一些蛛丝马迹。</p>
<p><em>众所周知，Python 的 <code>random</code> 库可以生成伪随机数。</em></p>
<p>曾经的一个科学家写下了这一份代码，尝试从随机的混乱中找到一丝秩序。
但是有<strong>神秘力量</strong>稳定了混乱的随机数，让程序失去了随机性，实验获得了一个稳定且非常好的结果。</p>
<p>请尝试通过这份程序复现实验：</p>
<ul>
<li>源码中遗留的隐藏信息 —— Flag 1</li>
<li>影响随机数的神秘力量 —— Flag 2</li>
<li>科学家获得的实验结果 —— Flag 3</li>
</ul>
<p><strong>注意</strong>：请关注程序运行的每一步，不经意的遗漏都可能导致你功亏一篑。</p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>Python 最常用的打包工具好像已经有了解包工具，拿来试试？</li>
<li><code>import</code> 究竟引来了何方神圣？打包过程中，被调用的所有库会被打包成 pyz 文件，去那找找吧。</li>
<li>程序理论上只有 1/65536 的概率能正常运行，为什么它现在能每次都运行起来呢？</li>
<li>请你一定要始终牢记最初的发现，不要在解题过程中迷失了自我。</li>
</ul>
</div>

**[【附件：下载题目附件（binary-pymaster.zip）】](attachment/binary-pymaster.zip)**

## 预期解法

本题主要希望大家对 Python 的**可执行文件打包**以及**字节码**进行了解和学习。

题目的可执行文件使用 *PyInstaller* 进行打包，*PyInstaller* 会将 Python 应用程序及其所有依赖项打包成一个可执行文件。用户无需安装 Python 解释器和任何模块即可运行打包好的应用程序。所以程序运行中调用的库也会被打包进其中。

本题使用的逆向工具主要有：

- [pyinstxtractor-ng](https://github.com/pyinstxtractor/pyinstxtractor-ng) 可以帮助我们对 PyInstaller 打包的应用程序进行解包得到 pyc 文件，这是 Python 源文件经过编译之后生成的字节码文件，也可以被 Python 直接运行。
- [pycdc](https://github.com/zrax/pycdc) 可以帮助我们对 pyc 文件进行反编译，在很多情况下 pycdc 都可以非常好地还原源代码。但是在特定情况下，它还原的代码可能会存在一些错误，但在本题并没有出现。

使用 pyinstxtractor-ng 解包后，用 pycdc 对解包得到的 `pymaster.pyc` 进行反编译得到如下结果：

```python
# Source Generated with Decompyle++
# File: pymaster.pyc (Python 3.8)

import marshal
import random
import base64
if random.randint(0, 65535) == 54830:
    exec(marshal.loads(base64.b64decode(b'YwAAAAAAAAAAAAAAAAAAAAAFAAAAQAAAAHMwAAAAZABaAGUBZAGDAWUCZQNkAoMBZAODAmUCZQNkBIMBZAWDAmUAgwGDAYMBAQBkBlMAKQdztAQAAGVKekZWMTFQMnpBVWZhL1UvMkN5bDBSanlCV3NiR2g3R0N2ZFlCMHBHNkFGeEt5MGRkdWdORUg1Z0VRVC8zMTIzQ1NPN1RSdDBiUlVhdFBjYzI5OGo0K3ZyNTNGZ3g5RUlMQzlpYjlvdHh6MmQyU0h1SHZRYnJWYnI4RFV0V2NkOEJGbzlPWlA2c2ZvVTdDUG9xOG42THY5OHhJSHlPeWpvWFU0aDk2elJqM2FyYkZyaHlHd0oyZGZnc3RmcG5WKzFHNEJjazN3RkNEa2VFNkVrRjVZaDd2QUpGZjJEWTBsbEY0bFlvOEN5QWpvVDUwZE1qdXNzVVBxZis1N1dHMkhacE1kRm5aRmhxUFZHZFprZFVvdUxtb2VvSXhhSWFtNDkvbHdUM1BIeFp5TnBickRvbkk0ZWpsVEViZ2tSb21XUENoTzhpZkVLZnlFUkl0YlR4Y0NHTEl2ZGtQVlVPcENYamVFeEM1SlFwZmpOZWVsOFBFbUV0VXFaM1VFUTVIVldpVFZNYlVOdzF2VEFWOU1COXlPRG1tQ042SGpuNm5qNVhSc3FZNm1qT3I4bW9XaFhIYmJydUoxaDY0b2U5ZVZzcGZ3eEtTa1hDWUMvVWxlblZPQlZUS3o3RkZOT1dUR2ZHOUl1TGNVejdLYlNzUmtWY21VYTN0YUFqS3BKZFF6cWEyZG5FVjBsbWFueE1JcU5zMzlrd3BKTEtWVVNibTNCdVdtUUxtWlV3NWx5dUVxeXVGL3BSeXVTK05LeWswRjVYQWp5cE5OT2lCU2hiaDJTdWZRQ25ETWd4a3RKVXJaQ1FsTlJGd3plMHZmRWllMUYxbWY5b0ZEWkozYnFySlNHV3lzcUl0TmRVa09vR29CODNJTUpIVnRwSzB5bmlDeVplTExBaStsek10R0hVTktrbGVseWtWVllMbUcwVGRZbzFyUjNBVnZYNzR2SlBGSG1zYitWUHM5V1FVaGVFM1FhWVJEL2JiQ0xSbm03K1VaWW8vK09GNmt3MTBBazM3ZnVET0VBTXJ4WlBTc2pjeUZIK0FvRGp3UUtwSk5TNWY3UEZtMWF1NjVOU0t0anpYV3hvcDFRUWlWV2VrWVZIQmlJVnB2U1NpVTByd1V1RXc1clJRN3NFQmNUNWZvdXVjamovUmkzeTZlelFuQThSN2lTTmVHTGlhSFI0QzlDQWNnbXVQcy9IZ0V0TUtKY09KaWJzZVpHNVRUL1M2WDFrTkFxZEl1Z3hUWU05dnhkalJPR1d6T1pjSE9iNC9lM3RGUTdLQ3FBVC9nalc4NnpQaXNiZm9pOW1US2h4dVFiTG5ncXByTmNaM29uQWo4aFc3c2tyRk5TZ1lHaHNHL0JkSGdCRHJET2t3NlVMMGxWT1F0elljRDFJdUhTZDBRMEZlMEJtUW4vcjFSOTJDQ3gvNEU2OXJoeWRqOVlRMVB6YkQzT0lpdGI3M2hZSGpqd0xQUndEcCtQN3J3MzMyKzZibjl4NmRqQ3g2T3crNXBUaDAvSjA2bEE3NlNtYmY4R016OHFCREtmakVEZ3RLVk0wVS9EajF5ZS9ZQ0kwUmZwaUcwSUdhRU5GSEVQYXJidjV1T0tGVT3aBGV4ZWPaBHpsaWLaCmRlY29tcHJlc3PaBmJhc2U2NNoJYjY0ZGVjb2RlTikE2gRjb2Rl2gRldmFs2gdnZXRhdHRy2gpfX2ltcG9ydF9fqQByCQAAAHIJAAAA2gDaCDxtb2R1bGU+AQAAAHMKAAAABAEGAQwBEP8C/w==')))
```

首先关注到在程序入口处有个随机数，而 Python 中的随机数默认是以时间戳为 seed 的，理论上并没有办法稳定输出一样的结果，但是执行下发的文件会发现每次都可以进入 flag 校验的步骤。说明 random 的 seed 可能被固定了。

之前提到 PyInstaller 会将所有的库文件也打包进可执行文件，它们被储存在 pyz 文件当中。pyinstxtractor-ng 会自动解包 pyz 文件，在其中可以找到 `random.pyc`，使用 pycdc 反编译后会在构建函数中发现预设的 seed：

```python
...
def Random():
    '''Random'''
    __doc__ = "Random number generator base class used by bound module functions.\n\n    Used to instantiate instances of Random to get generators that don't\n    share state.\n\n    Class Random can also be subclassed if you want to use a different basic\n    generator of your own devising: in that case, override the following\n    methods:  random(), seed(), getstate(), and setstate().\n    Optionally, implement a getrandbits() method so that randrange()\n    can cover arbitrarily large ranges.\n\n    "
    VERSION = 3

    def __init__(self, x = ('flag2 = flag{wElc0me_tO_THe_w0RlD_OF_pYtHON}',)):
        '''Initialize an instance.

        Optional argument x controls seeding, as for Random.seed().
        '''
        self.seed(x)
        self.gauss_next = None
...
```

~~出题人并没有想到这一步会给很多选手带来困难 orz~~

继续分析程序逻辑，marshal 是 Python 的对象序列化方法，被序列化的是一个 code object 对象，通过 `compile(code, "", "exec")` 生成。可以使用 Python 中 `dis` 库对其反汇编并进行分析：

```python
>>> import dis
>>> dis.dis(marshal.loads(base64.b64decode(b'YwAAAAAAAAAAAAAAAAAAAAAFAAAAQAAAAHMwAAAAZABaAGUBZAGDAWUCZQNkAoMBZAODAmUCZQNkBIMBZAWDAmUAgwGDAYMBAQBkBlMAKQdztAQAAGVKekZWMTFQMnpBVWZhL1UvMkN5bDBSanlCV3NiR2g3R0N2ZFlCMHBHNkFGeEt5MGRkdWdORUg1Z0VRVC8zMTIzQ1NPN1RSdDBiUlVhdFBjYzI5OGo0K3ZyNTNGZ3g5RUlMQzlpYjlvdHh6MmQyU0h1SHZRYnJWYnI4RFV0V2NkOEJGbzlPWlA2c2ZvVTdDUG9xOG42THY5OHhJSHlPeWpvWFU0aDk2elJqM2FyYkZyaHlHd0oyZGZnc3RmcG5WKzFHNEJjazN3RkNEa2VFNkVrRjVZaDd2QUpGZjJEWTBsbEY0bFlvOEN5QWpvVDUwZE1qdXNzVVBxZis1N1dHMkhacE1kRm5aRmhxUFZHZFprZFVvdUxtb2VvSXhhSWFtNDkvbHdUM1BIeFp5TnBickRvbkk0ZWpsVEViZ2tSb21XUENoTzhpZkVLZnlFUkl0YlR4Y0NHTEl2ZGtQVlVPcENYamVFeEM1SlFwZmpOZWVsOFBFbUV0VXFaM1VFUTVIVldpVFZNYlVOdzF2VEFWOU1COXlPRG1tQ042SGpuNm5qNVhSc3FZNm1qT3I4bW9XaFhIYmJydUoxaDY0b2U5ZVZzcGZ3eEtTa1hDWUMvVWxlblZPQlZUS3o3RkZOT1dUR2ZHOUl1TGNVejdLYlNzUmtWY21VYTN0YUFqS3BKZFF6cWEyZG5FVjBsbWFueE1JcU5zMzlrd3BKTEtWVVNibTNCdVdtUUxtWlV3NWx5dUVxeXVGL3BSeXVTK05LeWswRjVYQWp5cE5OT2lCU2hiaDJTdWZRQ25ETWd4a3RKVXJaQ1FsTlJGd3plMHZmRWllMUYxbWY5b0ZEWkozYnFySlNHV3lzcUl0TmRVa09vR29CODNJTUpIVnRwSzB5bmlDeVplTExBaStsek10R0hVTktrbGVseWtWVllMbUcwVGRZbzFyUjNBVnZYNzR2SlBGSG1zYitWUHM5V1FVaGVFM1FhWVJEL2JiQ0xSbm03K1VaWW8vK09GNmt3MTBBazM3ZnVET0VBTXJ4WlBTc2pjeUZIK0FvRGp3UUtwSk5TNWY3UEZtMWF1NjVOU0t0anpYV3hvcDFRUWlWV2VrWVZIQmlJVnB2U1NpVTByd1V1RXc1clJRN3NFQmNUNWZvdXVjamovUmkzeTZlelFuQThSN2lTTmVHTGlhSFI0QzlDQWNnbXVQcy9IZ0V0TUtKY09KaWJzZVpHNVRUL1M2WDFrTkFxZEl1Z3hUWU05dnhkalJPR1d6T1pjSE9iNC9lM3RGUTdLQ3FBVC9nalc4NnpQaXNiZm9pOW1US2h4dVFiTG5ncXByTmNaM29uQWo4aFc3c2tyRk5TZ1lHaHNHL0JkSGdCRHJET2t3NlVMMGxWT1F0elljRDFJdUhTZDBRMEZlMEJtUW4vcjFSOTJDQ3gvNEU2OXJoeWRqOVlRMVB6YkQzT0lpdGI3M2hZSGpqd0xQUndEcCtQN3J3MzMyKzZibjl4NmRqQ3g2T3crNXBUaDAvSjA2bEE3NlNtYmY4R016OHFCREtmakVEZ3RLVk0wVS9EajF5ZS9ZQ0kwUmZwaUcwSUdhRU5GSEVQYXJidjV1T0tGVT3aBGV4ZWPaBHpsaWLaCmRlY29tcHJlc3PaBmJhc2U2NNoJYjY0ZGVjb2RlTikE2gRjb2Rl2gRldmFs2gdnZXRhdHRy2gpfX2ltcG9ydF9fqQByCQAAAHIJAAAA2gDaCDxtb2R1bGU+AQAAAHMKAAAABAEGAQwBEP8C/w==')))
  1           0 LOAD_CONST               0 (b'eJzFV11P2zAUfa/U/2Cyl0RjyBWsbGh7GCvdYB0pG6AFxKy0ddugNEH5gEQT/3123CSO7TRt0bRUatPcc298j4+vr53Fgx9EILC9ib9otxz2d2SHuHvQbrVbr8DUtWcd8BFo9OZP6sfoU7CPoq8n6Lv98xIHyOyjoXU4h96zRj3arbFrhyGwJ2dfgstfpnV+1G4Bck3wFCDkeE6EkF5Yh7vAJFf2DY0llF4lYo8CyAjoT50dMjussUPqf+57WG2HZpMdFnZFhqPVGdZkdUouLmoeoIxaIam49/lwT3PHxZyNpbrDonI4ejlTEbgkRomWPChO8ifEKfyERItbTxcCGLIvdkPVUOpCXjeExC5JQpfjNeel8PEmEtUqZ3UEQ5HVWiTVMbUNw1vTAV9MB9yODmmCN6Hjn6nj5XRsqY6mjOr8moWhXHbbruJ1h64oe9eVspfwxKSkXCYC/UlenVOBVTKz7FFNOWTGfG9IuLcUz7KbSsRkVcmUa3taAjKpJdQzqa2dnEV0lmanxMIqNs39kwpJLKVUSbm3BuWmQLmZUw5lyuEqyuF/pRyuS+NKyk0F5XAjypNNOiBShbh2SufQCnDMgxktJUrZCQlNRFwze0vfEie1F1mf9oFDZJ3bqrJSGWysqItNdUkOoGoB83IMJHVtpK0yniCyZeLLAi+lzMtGHUNKklelykVVYLmG0TdYo1rR3AVvX74vJPFHmsb+VPs9WQUheE3QaYRD/bbCLRnm7+UZYo/+OF6kw10Ak37fuDOEAMrxZPSsjcyFH+AoDjwQKpJNS5f7PFm1au65NSKtjzXWxop1QQiVWekYVHBiIVpvSSiU0rwUuEw5rRQ7sEBcT5fouucjj/Ri3y6ezQnA8R7iSNeGLiaHR4C9CAcgmuPs/HgEtMKJcOJibseZG5TT/S6X1kNAqdIugxTYM9vxdjROGWzOZcHOb4/e3tFQ7KCqAT/gjW86zPisbfoi9mTKhxuQbLngqprNcZ3onAj8hW7skrFNSgYGhsG/BdHgBDrDOkw6UL0lVOQtzYcD1IuHSd0Q0Fe0BmQn/r1R92CCx/4E69rhydj9YQ1PzbD3OIitb73hYHjjwLPRwDp+P7rw332+6bn9x6djCx6Ow+5pTh0/J06lA76Smbf8GMz8qBDKfjEDgtKVM0U/Dj1ye/YCI0RfpiG0IGaENFHEParbv5uOKFU=')
              2 STORE_NAME               0 (code)

  2           4 LOAD_NAME                1 (eval)
              6 LOAD_CONST               1 ('exec')
              8 CALL_FUNCTION            1

  3          10 LOAD_NAME                2 (getattr)
             12 LOAD_NAME                3 (__import__)
             14 LOAD_CONST               2 ('zlib')
             16 CALL_FUNCTION            1
             18 LOAD_CONST               3 ('decompress')
             20 CALL_FUNCTION            2

  4          22 LOAD_NAME                2 (getattr)
             24 LOAD_NAME                3 (__import__)
             26 LOAD_CONST               4 ('base64')
             28 CALL_FUNCTION            1
             30 LOAD_CONST               5 ('b64decode')
             32 CALL_FUNCTION            2
             34 LOAD_NAME                0 (code)
             36 CALL_FUNCTION            1

  3          38 CALL_FUNCTION            1

  2          40 CALL_FUNCTION            1
             42 POP_TOP
             44 LOAD_CONST               6 (None)
             46 RETURN_VALUE
>>> print(zlib.decompress(base64.b64decode("eJzFV11P2zAUfa/U/2Cyl0RjyBWsbGh7GCvdYB0pG6AFxKy0ddugNEH5gEQT/3123CSO7TRt0bRUatPcc298j4+vr53Fgx9EILC9ib9otxz2d2SHuHvQbrVbr8DUtWcd8BFo9OZP6sfoU7CPoq8n6Lv98xIHyOyjoXU4h96zRj3arbFrhyGwJ2dfgstfpnV+1G4Bck3wFCDkeE6EkF5Yh7vAJFf2DY0llF4lYo8CyAjoT50dMjussUPqf+57WG2HZpMdFnZFhqPVGdZkdUouLmoeoIxaIam49/lwT3PHxZyNpbrDonI4ejlTEbgkRomWPChO8ifEKfyERItbTxcCGLIvdkPVUOpCXjeExC5JQpfjNeel8PEmEtUqZ3UEQ5HVWiTVMbUNw1vTAV9MB9yODmmCN6Hjn6nj5XRsqY6mjOr8moWhXHbbruJ1h64oe9eVspfwxKSkXCYC/UlenVOBVTKz7FFNOWTGfG9IuLcUz7KbSsRkVcmUa3taAjKpJdQzqa2dnEV0lmanxMIqNs39kwpJLKVUSbm3BuWmQLmZUw5lyuEqyuF/pRyuS+NKyk0F5XAjypNNOiBShbh2SufQCnDMgxktJUrZCQlNRFwze0vfEie1F1mf9oFDZJ3bqrJSGWysqItNdUkOoGoB83IMJHVtpK0yniCyZeLLAi+lzMtGHUNKklelykVVYLmG0TdYo1rR3AVvX74vJPFHmsb+VPs9WQUheE3QaYRD/bbCLRnm7+UZYo/+OF6kw10Ak37fuDOEAMrxZPSsjcyFH+AoDjwQKpJNS5f7PFm1au65NSKtjzXWxop1QQiVWekYVHBiIVpvSSiU0rwUuEw5rRQ7sEBcT5fouucjj/Ri3y6ezQnA8R7iSNeGLiaHR4C9CAcgmuPs/HgEtMKJcOJibseZG5TT/S6X1kNAqdIugxTYM9vxdjROGWzOZcHOb4/e3tFQ7KCqAT/gjW86zPisbfoi9mTKhxuQbLngqprNcZ3onAj8hW7skrFNSgYGhsG/BdHgBDrDOkw6UL0lVOQtzYcD1IuHSd0Q0Fe0BmQn/r1R92CCx/4E69rhydj9YQ1PzbD3OIitb73hYHjjwLPRwDp+P7rw332+6bn9x6djCx6Ow+5pTh0/J06lA76Smbf8GMz8qBDKfjEDgtKVM0U/Dj1ye/YCI0RfpiG0IGaENFHEParbv5uOKFU=")).decode())
import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"


class adJGrTXOYN:
    def __init__(adJGrTXOYP, OOOO, OOO0):
        adJGrTXOYP.OOOO = OOOO
        adJGrTXOYP.OOO0 = OOO0
        adJGrTXOYP.OO0O = None
        adJGrTXOYP.O0OO = None
        adJGrTXOYP.O0O0 = None


class adJGrTXOYb:
    def __init__(adJGrTXOYP):
        adJGrTXOYP.IIII = None

    def adJGrTXOYb(adJGrTXOYP, adJGrTXOYo):
        while adJGrTXOYo.OO0O != None:
            if adJGrTXOYo.OO0O.OO0O == None:
                if adJGrTXOYo == adJGrTXOYo.OO0O.O0OO:
                    adJGrTXOYP.adJGrTXOYn(adJGrTXOYo.OO0O)
                else:
                    adJGrTXOYP.adJGrTXOYV(adJGrTXOYo.OO0O)
            elif (
                adJGrTXOYo == adJGrTXOYo.OO0O.O0OO
                and adJGrTXOYo.OO0O == adJGrTXOYo.OO0O.OO0O.O0OO
            ):
                adJGrTXOYP.adJGrTXOYn(adJGrTXOYo.OO0O.OO0O)
                adJGrTXOYP.adJGrTXOYn(adJGrTXOYo.OO0O)
            elif (
                adJGrTXOYo == adJGrTXOYo.OO0O.O0O0
                and adJGrTXOYo.OO0O == adJGrTXOYo.OO0O.OO0O.O0O0
            ):
                adJGrTXOYP.adJGrTXOYV(adJGrTXOYo.OO0O.OO0O)
                adJGrTXOYP.adJGrTXOYV(adJGrTXOYo.OO0O)
            elif (
                adJGrTXOYo == adJGrTXOYo.OO0O.O0O0
                and adJGrTXOYo.OO0O == adJGrTXOYo.OO0O.OO0O.O0OO
            ):
                adJGrTXOYP.adJGrTXOYV(adJGrTXOYo.OO0O)
                adJGrTXOYP.adJGrTXOYn(adJGrTXOYo.OO0O)
            else:
                adJGrTXOYP.adJGrTXOYn(adJGrTXOYo.OO0O)
                adJGrTXOYP.adJGrTXOYV(adJGrTXOYo.OO0O)

    def adJGrTXOYV(adJGrTXOYP, x):
        y = x.O0O0
        x.O0O0 = y.O0OO
        if y.O0OO != None:
            y.O0OO.OO0O = x
        y.OO0O = x.OO0O
        if x.OO0O == None:
            adJGrTXOYP.IIII = y
        elif x == x.OO0O.O0OO:
            x.OO0O.O0OO = y
        else:
            x.OO0O.O0O0 = y
        y.O0OO = x
        x.OO0O = y

    def adJGrTXOYn(adJGrTXOYP, x):
        y = x.O0OO
        x.O0OO = y.O0O0
        if y.O0O0 != None:
            y.O0O0.OO0O = x
        y.OO0O = x.OO0O
        if x.OO0O == None:
            adJGrTXOYP.IIII = y
        elif x == x.OO0O.O0O0:
            x.OO0O.O0O0 = y
        else:
            x.OO0O.O0OO = y
        y.O0O0 = x
        x.OO0O = y

    def adJGrTXOYx(adJGrTXOYP, OOOO, OOO0):
        adJGrTXOYo = adJGrTXOYN(OOOO, OOO0)
        adJGrTXOYu = adJGrTXOYP.IIII
        OO0O = None
        while adJGrTXOYu != None:
            OO0O = adJGrTXOYu
            if OOOO < adJGrTXOYu.OOOO:
                adJGrTXOYu = adJGrTXOYu.O0OO
            else:
                adJGrTXOYu = adJGrTXOYu.O0O0
        adJGrTXOYo.OO0O = OO0O
        if OO0O == None:
            adJGrTXOYP.IIII = adJGrTXOYo
        elif OOOO < OO0O.OOOO:
            OO0O.O0OO = adJGrTXOYo
        else:
            OO0O.O0O0 = adJGrTXOYo
        adJGrTXOYP.adJGrTXOYb(adJGrTXOYo)


def adJGrTXOYQ(adJGrTXOYo):
    s = b""
    if adJGrTXOYo != None:
        s += bytes([adJGrTXOYo.OOO0 ^ random.randint(0, 0xFF)])
        s += adJGrTXOYQ(adJGrTXOYo.O0OO)
        s += adJGrTXOYQ(adJGrTXOYo.O0O0)
    return s


def adJGrTXOYy(adJGrTXOYj):
    adJGrTXOYu = adJGrTXOYj.IIII
    OO0O = None
    while adJGrTXOYu != None:
        OO0O = adJGrTXOYu
        if random.randint(0, 1) == 0:
            adJGrTXOYu = adJGrTXOYu.O0OO
        else:
            adJGrTXOYu = adJGrTXOYu.O0O0
    adJGrTXOYj.adJGrTXOYb(OO0O)


def adJGrTXOYD():
    adJGrTXOYj = adJGrTXOYb()

    adJGrTXOYh = input("Please enter the flag: ")

    if len(adJGrTXOYh) != 36:
        print("Try again!")
        return
    if adJGrTXOYh[:5] != "flag{" or adJGrTXOYh[-1] != "}":
        print("Try again!")
        return

    for adJGrTXOYL in adJGrTXOYh:
        adJGrTXOYj.adJGrTXOYx(random.random(), ord(adJGrTXOYL))

    for _ in range(0x100):
        adJGrTXOYy(adJGrTXOYj)

    adJGrTXOYi = adJGrTXOYQ(adJGrTXOYj.IIII)
    adJGrTXOYU = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    if adJGrTXOYi == adJGrTXOYU:
        print("You got the flag3!")
    else:
        print("Try again!")


if __name__ == "__main__":
    adJGrTXOYD()

>>>
```

至此获得了源码，虽然源码经过了混淆，通过手动反混淆会发现实现了一个伸展树 Splay，将 flag 以随机权值插入树后进行了 0x100 次随机伸展，最后将树的中序遍历异或上随机值后进行判断。由于随机的 seed 是固定的，所以整个过程就可以稳定运行。

由于随机伸展部分只涉及位置的改变，而异或部分只涉及值的改变，将两个部分分别逆向进行即可获得最终的 flag。

## Exp

```python
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
```