import OpenSSL
import base64
import hashlib
import string

import logger

#---
#---
#---
#---
#---
#---
#---
#---
#---
#---
FLAGS = [
    'flag{jUst-PREsS-F12-ANd-Copy-tHE-tEXt}',
    'flag{All antI-cOpy TeCHnIques aRe USeLEss BRO}',
]
#---
#---
#---
#---
#---
#---
#---
#---
#---
#---

def leet(flag, salt, token):
    uid = token.partition(':')[0]
    assert flag.startswith('flag{') and flag.endswith('}'), 'wrong flag format'
    
    uid = int(hashlib.sha256(f'{uid}-{salt}'.encode()).hexdigest(), 16)
    rcont = flag[len('flag{'):-len('}')]
    rdlis = []

    for i in range(len(rcont)):
        if rcont[i] in string.ascii_letters:
            rdlis.append(i)
    assert len(rdlis) >= 10, 'insufficient flag entropy'

    rdseed = (uid+233)*114547%123457
    for it in range(6):
        if not rdlis:  # no any leetable chars
            return flag

        np = rdseed%len(rdlis)
        npp = rdlis[np]
        rdseed = (rdseed+233)*114547%123457
        del rdlis[np]
        px = rcont[npp]
        rcont = rcont[:npp] + (px.upper() if px in string.ascii_lowercase else px.lower()) + rcont[npp+1:]

    return 'flag{'+rcont+'}'

with open('2024.pub', 'rb') as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

def getflag(token, idx):
    uid = checktoken(token)
    if not uid:
        return '???'
    #logger.write(uid, ['getflag', idx, token])
    if idx==1:
        return FLAGS[0]
    elif idx==2:
        return leet(FLAGS[1], 'xmcp.copy-flag2', token)

def checktoken(token):
    try:
        id, sig = token.split(':', 1)
        sig_raw = base64.urlsafe_b64decode(sig)
        assert sig==base64.urlsafe_b64encode(sig_raw).decode()
        OpenSSL.crypto.verify(cert, sig_raw, id.encode(), 'sha256')
        return id
    except Exception:
        return None