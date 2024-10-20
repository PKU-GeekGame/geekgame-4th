import gzip
import random

random.seed(114514)

char_num = 86


def has_repeated_substring(byte_stream):
    substring_count = {}

    for i in range(len(byte_stream) - 3):
        substring = byte_stream[i:i+3]
        if substring in substring_count:
            substring_count[substring] += 1
        else:
            substring_count[substring] = 1
        if substring_count[substring] > 1:
            return True
    return False


manual_dict = {}

manual_count = 0
for k, v in manual_dict.items():
    manual_count += v

target_dict = manual_dict.copy()

for x in range(0x20, 0x20 + char_num):
    if x in manual_dict:
        continue
    if x == 108:  # 异或完 19 会变成 0x7f，跳过
        continue
    target_dict[x] = (1000 - manual_count) // (char_num - len(manual_dict))

print(target_dict)

manual_text = b'N=' + b'NYB1*2`F*asS\'i`F=auf\\\'-BLT*a`FNR(IB\'1QomdC ?/=stTMRRB'

for char in target_dict:
    if char in manual_text:
        print(f"{chr(char)}: {manual_text.count(char)}")

for char in manual_text:
    target_dict[char] = target_dict[char] - 1
    if target_dict[char] < 0:
        assert False, char


random_list = []
for k in target_dict:
    random_list.extend([k] * target_dict[k])
random.shuffle(random_list)
random_shit = bytes(random_list)

while has_repeated_substring(random_shit):
    random_list = list(random_shit)
    random.shuffle(random_list)
    random_shit = bytes(random_list)

data = manual_text + random_shit

if has_repeated_substring(data):
    assert False, "check!"

print(len(data))

with open("test.txt", "w") as f:
    f.write(data.decode())

with open('test.gz', 'wb') as f:
    compressed_data = gzip.compress(data)
    f.write(compressed_data)
