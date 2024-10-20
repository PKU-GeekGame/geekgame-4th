#!/usr/bin/env python3

import signal
import subprocess

def main():
    print('Running...', flush=True)

    proc = subprocess.run(['./run'])

    if proc.returncode == -signal.SIGSEGV:
        flag1 = open('./flag1.txt', 'r').read().strip()
        print(f'Here is Flag 1: {flag1}')

    print('See you later~')

if __name__ == '__main__':
    main()
