file_name = "dinic_input.txt"


def generate():
    n = 100
    m = 4058
    s = 1
    t = 100
    with open(file_name, 'w') as f:
        f.write(f"{n} {m} {s} {t}\n")
        for i in range(1, 100):
            f.write(f"{i} 100 {1}\n")
            for j in range(1, 40):
                f.write(f"100 {i} {j}\n")
        for i in range(1, 99):
            f.write(f"{i} {i+1} {1000}\n")


generate()
