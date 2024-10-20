# [Binary] Fast Or Clever

- 命题人：Rosayxy
- 题目分值：200 分

## 题目描述

<p>本挑战中，你不仅是个黑客，更是个赛车手。     </p>
<p>你将展现杰出的控制能力，去控制赛场的设定。你将发挥挑战的精神，改变看似必然的失败。你<strong>在线程交替中抢夺时间，</strong>更快到达 Flag 所在的终点。                </p>
<blockquote>
<p>So, are you fast enough… or clever enough… for this challenge?</p>
</blockquote>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>usleep 的时间可以被溢出，使得 <code>get_thread2_input</code> 可以被执行并且改掉输出 flag 的长度</li>
</ul>
</div>

**[【附件：下载题目附件（binary-racecar.zip）】](attachment/binary-racecar.zip)**

**【终端交互：连接到题目】**

## 预期解法

- 在 `do_output` 函数中存在一个 TOCTOU （time-of-check-time-of-use）的漏洞，具体来说，该函数中会把 `siz` 个字节的 flag 输出来，但是一开始检查了 `siz` 在 0 ~ 4 字节，代表不会输出完整的 flag，但是我们可以通过 `get_thread2_input` 把 `siz` 改大，从而输出完整 flag

- 但是一般来说，线程调度是不固定的，所以可能需要多次尝试才能使得 `get_thread2_input` 在 `thread1` 的检查和拷贝之间被调度并且改值，但是这里我们可以溢出 `usleep` 的时间为一个很大的值，来使得 `get_thread2_input` 在 `thread1` 对于 `siz` 的 check 和 use 之间被调度。从而大大增加成功率

- 总结一下，对于 race condition ，一般有两个量是需要关注的：线程间共享对象，时间窗口。我们在线程间共享了 `siz` 对象，并且它可以被写入从而在第一个线程中被改值，而时间窗口则是 toctou 中 check-use 之间的时间间隔，在本题中我们可以溢出 `usleep_time` 来控制