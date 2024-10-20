with open("./flag2.txt", "w", encoding="utf-8") as out_f:
    with open("./4.in", "r") as in_f:
        in_f.readline()
        out_f.write("100 4715 1 2\n")
        for line in in_f.readlines():
            items = [int(x) for x in line.strip().split()]
            items[0] = (items[0] - 1) % 100 + 1
            items[1] = (items[1] - 1) % 100 + 1
            if items[2] > 1e7:
                items[2] = 1000000
            if items[0] == items[1]:
                items[1] = items[1] + 1
            out_f.write(f"{items[0]} {items[1]} {items[2]}\n")
