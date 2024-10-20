import random
import gzip

def average_bit_count(s):
    return sum(c.bit_count() for c in s) / len(s)

def main():
    text = []
    for j in range(32, 32 + 7):
        for i in range(60, 60 + 22):
            lim = 5
            if i == 60 + 21: lim = 2
            for _ in range(lim):
                text.append(i)
            text.append(j)
    print(len(text))
    comp = gzip.compress(bytes(text))
    prefix = (comp + b'\xFF'*256)[:256]
    print(average_bit_count(prefix))
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
    with open('text1.txt', 'wb') as f:
        f.write(Rev(text))
        f.close()

main()
