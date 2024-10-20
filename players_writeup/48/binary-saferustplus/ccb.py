import subprocess
import signal

def run_(inp):
    ret = subprocess.run(["./run"], input=inp.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ret

def run(config):
    print(f"Running {config}")
    inp = ""
    inp += "1\n" # create
    inp += f"{config['ctype']}\n"
    inp += "0\n"
    inp += f"{config['perm']}\n"
    rinp, winp = "", ""
    rinp += "2\n" # read
    rinp += "0\n0\n"
    rinp += f"{config['rtype']}\n"
    winp += "3\n" # write
    winp += "0\n0\n1\n"
    winp += f"{config['wtype']}\n"
    if config['rwfirst'] == 'r':
        inp += rinp + winp
    else:
        inp += winp + rinp
    ret = run_(inp)
    print(ret.stdout.decode())
    print(ret.stderr.decode())
    print(f"Return code: {ret.returncode}, expected: {-signal.SIGSEGV}")
    return ret.returncode

def main():
    for ctype in [1]: # [1,2,3]
        for perm in [1,2,3]:
            for rwfirst in ['r','w']:
                for rtype in [1,2,3]:
                    for wtype in [1,2,3]:
                        ret = run({
                            'ctype': ctype,
                            'perm': perm,
                            'rwfirst': rwfirst,
                            'rtype': rtype,
                            'wtype': wtype
                        })
                        if ret == -signal.SIGSEGV:
                            print(f"Found! {ctype} {perm} {rwfirst} {rtype} {wtype}")
                            break

if __name__ == "__main__":
    main()
