import random
import gzip

def average_bit_count(s):
    return sum(c.bit_count() for c in s) / len(s)

def main():
    L = 6
    text = "[What can I say? Mamba out! --KobeBryant]"
    stream = []
    for i in range(len(text)):
        val = ord(text[i])
        for j in range(8):
            if val & (1 << j):
                stream.append(1)
            else:
                stream.append(0)
    for rem in range(3, 4): #range(L):
        curval = 0
        curcnt = 0
        bad = False
        S = []
        for i in range(rem, len(stream)):
            curval = curval * 2 + stream[i]
            curcnt += 1
            if curcnt == L:
                S.append(curval)
                if curval == 2 ** L - 1:
                    bad = True
                curval = 0
                curcnt = 0
        if not bad:
            print('Good rem', rem)
        occ = [0, ] * (2 ** L - 1)
        for x in S:
            occ[x] += 1
        max_occ = 0
        for x in occ:
            max_occ = max(max_occ, x)
        occ[0] += 1
        S.append(0)
        occ[6] += 1
        S = [6] + S
        T = []
        for i in range(2 ** L - 1):
            if occ[i] < max_occ:
                for _ in range(max_occ - occ[i]):
                    T.append(i)
        r = random.Random()
        r.seed(1234)
        r.shuffle(T)
        S = T[:194] + S + T[194:]
        S = [c + 32 for c in S]
        S = bytes(S)
        print(S)
        comp = gzip.compress(S)
        print(comp)
        def Rev(text):
            r = random.Random()
            r.seed('Genshin Impact')
            idx = []
            for i in range(len(text)):
                idx.append(i)
            r.shuffle(idx)
            new_text = [0, ] * len(text)
            for i in range(len(text)):
                new_text[idx[i]] = text[i] ^ 13
            return bytes(new_text)
        with open('text2.txt', 'wb') as f:
            f.write(Rev(S))
            f.close()

main()
