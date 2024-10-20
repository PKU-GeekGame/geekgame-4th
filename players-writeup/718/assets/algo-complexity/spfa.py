file_name = "spfa_input.txt"


def generate():
    n = 2000
    m = 4994
    s = 1
    t = 2000

    with open(file_name, 'w') as f:
        f.write(f"{n} {m} {s} {t}\n")
        t = 0
        for i in range(1, 1000):
            f.write(f"{i} 1001 {10000-4*i}\n")
            f.write(f"{i} {i+1} {1}\n")
        f.write(f"1000 1001 8000\n")
        for i in range(1999, 1001, -1):
            f.write(f"1001 {i} {4*i}\n")
            f.write(f"{i} {i+1} {2}\n")
            f.write(f"{i} {i+1} {2}\n")
        f.write(f"1001 2000 10000\n")


generate()
