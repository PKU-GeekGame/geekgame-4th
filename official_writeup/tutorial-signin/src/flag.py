import json

with open('flag_adjs.json', encoding='utf-8') as f:
    FLAG_ADJS = json.load(f)

N_VARIANTS = len(FLAG_ADJS) * len(FLAG_ADJS) * 3 * 3 * 2

def flag_for_variant(var):
    var_the = var % 2
    var = var // 2
    var_space = var % 3
    var = var // 3
    var_case = var % 3
    var = var // 3
    var_adj_1 = FLAG_ADJS[var % len(FLAG_ADJS)]
    var = var // len(FLAG_ADJS)
    var_adj_2 = FLAG_ADJS[var]

    if var_the:
        words = ['w3lcome', 'to', 'the', var_adj_1, var_adj_2, 'geekgame']
    else:
        words = ['w3lcome', 'to', var_adj_1, var_adj_2, 'geekgame!']

    if var_case==1:
        words = [word.upper() for word in words]
    elif var_case==2:
        words = [word.title() for word in words]

    if var_space==1:
        flag = '_'.join(words)
    elif var_space==2:
        flag = '-'.join(words)
    else:
        flag = ' '.join(words)

    return 'flag{' + flag + '}'

def flag_for_challenge(u, ch):
    var = u.get_partition(ch, N_VARIANTS)
    return flag_for_variant(var)

def flag(u, f):
    return flag_for_challenge(u, f.challenge)