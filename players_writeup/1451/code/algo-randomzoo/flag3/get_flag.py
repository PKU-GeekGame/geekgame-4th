data_list = []
with open("./data_list.txt", "r") as f:
    for line in f.readlines():
        data_list.append(int(line.strip()))

rand_list = []
with open("./rand_list.txt", "r") as f:
    for line in f.readlines():
        rand_list.append(int(line.strip()))


for idx, data in enumerate(data_list):
    print(chr(data_list[idx] - rand_list[idx]), end="")
print()
