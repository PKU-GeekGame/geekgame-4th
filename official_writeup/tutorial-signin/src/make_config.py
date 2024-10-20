from pathlib import Path
import random
import json

def dedup(l):
    h = set()
    ret = []
    for x in l:
        if x not in h:
            h.add(x)
            ret.append(x)
    return ret

SENTENCES = dedup('''
这个文件没有flag，找找别的吧。
这里是一些无用的信息。
你还没有找到flag，继续努力！
这个文件只是一些普通的文本。
flag不在这里，再找找？
这里的内容与flag无关。
继续查找，flag可能在别的地方。
这里没有flag，看看其他文件吧。
这个文件里没有任何有用的信息。
flag在别处，继续探索。
flag究竟在哪个文件里呢？
这里的文字只是随便写的。
这个文件没有任何秘密。
这里的内容与flag毫无关系。
这个文件只是在浪费你的时间。←这句话是AI说的
flag不在这里，试试其他的文件。
这里是一些无关紧要的句子。
这个文件的内容很普通，没什么特别。
继续寻找，flag在别处等着你。
这个文件没有包含flag的信息。
请继续寻找，flag可能在其他地方。
很抱歉，这里并没有flag。
该文件的内容与flag无关，请查看其他文件。
这个文件只是一些常规信息，flag不在这里。
继续努力，flag可能藏在其他文件中。
这里的内容并不包含flag，建议查看更多文件。
这个文件记录的是一些日常事务，flag不在其中。
请注意，这里没有flag的踪迹。
该文件的目的是提供信息，而非包含flag。
这个文件中没有flag的信息，请继续寻找。
该文件是无关的内容，flag请查看其他位置。
这里并没有flag，您可能需要检查其他文件。
这个文件的内容与flag无关，请继续探索。
很遗憾，这里没有flag的线索。
This file does not contain the flag.
You won't find the flag here.
This document is not the right one for the flag.
The flag is hidden elsewhere, not in this file.
Unfortunately, this file is not where the flag resides.
Keep searching, the flag is not in this location.
This file is unrelated to the flag.
The flag is not present in this document.
You are close, but the flag is not in this file.
This content does not include the flag you seek.
The flag is hiding in a different file.
Sorry, but the flag is not found here.
This file serves a different purpose; no flag here.
The search continues; the flag is not in this document.
This is a friendly reminder: no flag in this file.
The flag is not located within these pages.
Keep looking; this file does not have the flag.
This document does not hold the key to the flag.
The flag is not present in this particular file.
You're on the right track, but the flag is elsewhere.
This file does not contain any flags.
You might want to check another file for the flag.
The flag is not included in this document.
Unfortunately, there’s no flag to be found here.
This file is not the one that holds the flag.
The flag is not hiding in this location.
Keep searching; the flag is in a different file.
This document is unrelated to the flag you are looking for.
No flag can be found within these lines.
The flag is not present in this content.
This file does not lead to the flag.
The flag remains elusive in this document.
This is not the correct file for the flag.
You are looking in the wrong place for the flag.
The flag is not part of this file’s contents.
No flag here; please try another file.
This document does not provide access to the flag.
You might want to explore other files for the flag.
There’s no flag hidden in this text.
This file is not where you’ll find the flag.
你知道吗？“xx #xx”这样的昵称可以让井号后面的文本在排行榜上突出显示。
你知道吗？上届比赛封禁了68个涉及作弊的账号，其中12人在1000分以上。
你知道吗？用GPT-4o-mini生成这些随机句子很方便。
你知道吗？本届比赛平台修复了flag提交框左右圆角相差2px的bug。
你知道吗？本届比赛平台从Python 3.8升级到了3.12。
你知道吗？上届北大校内三等奖的奖品是一个华为手表。——發自我的內心
'''.strip().splitlines())

assert len(SENTENCES) == 3**4-1

random.seed(1337)
random.shuffle(SENTENCES)

# put flag at (3, 1, 2, 1)
SENTENCES.insert((3-1)*27 + (1-1)*9 + (2-1)*3 + (1-1), '__FLAG__')

FLAG_ADJS = dedup('''
Gracious
Generous
Gentle
Gleeful
Glorious
Grateful
Gallant
Glistening
Genteel
Goodhearted
Grounded
Genuine
Graceful
Gutsy
Gifted
Glaring
Glistening
Gloomless
Gallant
Generous
Gentle
Genuine
Gifted
Glamorous
Gleeful
Glorious
Graceful
Gracious
Grand
Grateful
Great
Grounded
Growing
Gutsy
Glistening
Glaring
Galloping
Guiding
Glistening
Genteel
Gripping
Gushy
Glistening
Gritty
Glowing
Generative
Gracious
Groundbreaking
Glistening
Gilded
Gusto
Gallivanting
'''.strip().splitlines())

random.seed(114514)
random.shuffle(FLAG_ADJS)

def gen_random_id():
    return ''.join([random.choice('Il') for _ in range(15)])

IDS = {}
random.seed(666)
for lv in range(1, 4+1):
    cur_ids = []
    IDS[lv] = cur_ids
    for n in range(3**lv):
        cur_ids.append(gen_random_id())
    assert len(dedup(cur_ids)) == len(cur_ids)

with open('sentences.json', 'w', encoding='utf-8') as f:
    json.dump(SENTENCES, f, indent=1, ensure_ascii=False)

with open('flag_adjs.json', 'w', encoding='utf-8') as f:
    json.dump(FLAG_ADJS, f, indent=1, ensure_ascii=False)

with open('ids.json', 'w', encoding='utf-8') as f:
    json.dump(IDS, f, indent=1, ensure_ascii=False)