import zipfile

def solve(f):
    with zipfile.ZipFile(f) as z:
        for name in z.namelist():
            with z.open(name, 'r') as subf:
                if name.endswith('.zip'):
                    solve(subf)
                else:
                    txt = subf.read().decode()
                    if 'flag{' in txt:
                        print(txt)

solve('tutorial-signin.zip')