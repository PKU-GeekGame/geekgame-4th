import OpenSSL
import base64

FLAGS = [
    'flag{llm-hacker-amateur}',
    'flag{jailbreak-master-unleashed}',
]
#后面应该要改成动态的？

with open('2024.pub', 'rb') as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

def getflag(token, idx):
    uid = checktoken(token)
    return FLAGS[idx-1]

def checktoken(token):
    if not token:
        return None
    try:
        id, sig = token.split(':', 1)
        sig_raw = base64.urlsafe_b64decode(sig)
        assert sig==base64.urlsafe_b64encode(sig_raw).decode()
        OpenSSL.crypto.verify(cert, sig_raw, id.encode(), 'sha256')
        return id
    except Exception:
        return None