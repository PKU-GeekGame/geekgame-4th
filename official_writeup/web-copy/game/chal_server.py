from flask import *
from flask_compress import Compress
from flask_caching import Cache
import secrets
import hashlib
import base64
import time
import os
from cryptography.fernet import Fernet

import logger
from flag import checktoken, getflag

app = Flask(__name__)
app.secret_key = 'xmcp.key.7iItDpMhF2gdQub7TNAXEVxXEwNCzszU2_XWXnMz'

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 86400,
})

def get_cache_key(request):
    return request.full_path

app.config['COMPRESS_MIMETYPES'] = ['application/javascript', 'text/javascript']
app.config['COMPRESS_ALGORITHM'] = ['br', 'gzip', 'deflate']
app.config['COMPRESS_LEVEL'] = 9
app.config['COMPRESS_DEFLATE_LEVEL'] = 9
app.config['COMPRESS_BR_LEVEL'] = 9

compress = Compress()
compress.init_app(app)
compress.cache = cache
compress.cache_key = get_cache_key

NOISE_CHARACTERS = 'IJl|1O0()i!'
def gen_noise(n):
    return ''.join(secrets.choice(NOISE_CHARACTERS) for _ in range(n))

def sec_hash(data, salt, ts):
    return hashlib.sha512(f'xmcp.sec_hash:{salt}|{ts}|{data}'.encode('utf-8')).hexdigest()

SALT_1 = 'xmcp.salt.1.6vA9Jci0FaVfcI460L1-z6U1sG3Mhd3firhMpYbs'
SALT_2 = 'xmcp.salt.2.LtqtpVzP4wflmnVjJkGK3tdCMpcPgocPNODg1wEK'

@app.route('/')
def index():
    if 'token' in request.args:
        req_token = request.args['token']
        assert isinstance(req_token, str)
        uid = checktoken(req_token)
        if uid:
            logger.write(uid, ['login'])
            session['token'] = req_token
            return redirect('/')

    if 'token' not in session:
        return 'Token无效，请从比赛平台进入'

    return render_template('index.html')

@app.route('/hacker')
def hacker():
    if 'token' not in session:
        return 'Token无效，请从比赛平台进入'
    uid = session['token'].partition(':')[0]
    
    logger.write(uid, ['hacker'])
    return render_template('result.html', info='有黑客！')

def xor_encrypt(data, key):
    encrypted = []
    key_length = len(key)
    for i, char in enumerate(data):
        encrypted_char = chr(ord(char) ^ key[i % key_length])
        encrypted.append(encrypted_char)
    return ''.join(encrypted)

@app.route('/page1', methods=['GET', 'POST'])
def page1():
    if 'token' not in session:
        return 'Token无效，请从比赛平台进入'
    uid = session['token'].partition(':')[0]
    
    CHALL_LEN = 40*6
    XOR_KEY = [54, 85, 115, 65, 21, 55, 97, 48, 116, 107, 110, 11, 21, 4, 17, 61, 109, 90, 14, 56, 85, 90, 24, 76, 48, 79, 117, 36, 107, 21, 115, 13, 65, 44, 86, 59, 75, 53, 3, 86, 0, 39, 20, 19, 113, 97, 16]
    
    if request.method == 'GET':
        noise = gen_noise(CHALL_LEN)
        encrypted_noise = xor_encrypt(noise, XOR_KEY)
        ts = int(time.time())
        logger.write(uid, ['get_challenge1'])
        return render_template('page1.html', data={
            'ts': ts,
            'certificate': sec_hash(noise, SALT_1, ts),
            'challenge': base64.b64encode(encrypted_noise.encode()).decode(),
        })
    
    else:
        ts = int(request.form['ts'])
        certificate = request.form['certificate']
        response = request.form['response'].replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')

        cur_ts = int(time.time())
        
        ok = len(response)==CHALL_LEN and sec_hash(response, SALT_1, ts)==certificate
        if ok:
            if (ts-1 < cur_ts < ts+61):
                logger.write(uid, ['post_challenge1', 'getflag'])
                return render_template('result.html', info=f'验证码正确！Flag 1 是：{getflag(session["token"], 1)}')
            else:
                logger.write(uid, ['post_challenge1', 'toolate'])
                return render_template('result.html', info='验证码正确，但是太慢了！少侠请重新来过。')
        else:
            logger.write(uid, ['post_challenge1', 'wrong-hash' if len(response)==CHALL_LEN else 'wrong-length'])
            return render_template('result.html', info='不对哦！')

@app.route('/page2', methods=['GET', 'POST'])
def challenge2():
    if 'token' not in session:
        return 'Token无效，请从比赛平台进入'
    uid = session['token'].partition(':')[0]
    
    CHALL_LEN = 200
    CHALL_CNT = 10
    FERNET_KEY = 'kVN7kK-VRmLgWs4ivtpwguMqoM_egcU01KEuwitL5TU='
    XOR_KEY = [61,72,56,103,87,80,18,82,82,3,55,112,9,65,10,108,30,78,56,68,100,124,85,113,82,0,45,71,78,97,48,53,53,97,65,52,98,61,95,83,50,55,28,101,35,17,47,32,31,32,118,34,96,14,110,85,14,22,49,5,93,45,123,122,41,52,10,117,80,73,118,57,65,100,114,59,40,50,106,22,71,110,92,25,12,18,61,7,15,98,103,91,36,20,26,70,125,37,23,11,38,2,57,85,116,48,0,84,67,6,116,59,41,95,75,109,75,50,110,11,104,46,22,102,52,38,41,36,61,59,15,50,90,116,73,117,92]

    if request.method == 'GET':
        encrypted_noises = []
        noises = []
        fernet = Fernet(FERNET_KEY)
        for _ in range(CHALL_CNT):
            noise = gen_noise(CHALL_LEN)
            noises.append(noise)
            encrypted_noise = xor_encrypt(noise, XOR_KEY)
            encrypted_noises.append(fernet.encrypt(encrypted_noise.encode()).decode())
        ts = int(time.time())

        logger.write(uid, ['get_challenge2'])
        #print('!!! gen', ''.join(noises))

        return render_template('page2.html', data={
            'ts': ts,
            'certificate': sec_hash(''.join(noises), SALT_2, ts),
            'challenge': '|'.join(encrypted_noises),
        })
    
    else:
        ts = int(request.form['ts'])
        certificate = request.form['certificate']
        response = request.form['response'].replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')

        cur_ts = int(time.time())
        
        ok = len(response)==CHALL_LEN*CHALL_CNT and sec_hash(response, SALT_2, ts)==certificate

        #print('!!! len', len(response), CHALL_LEN*CHALL_CNT)
        #print('!!! user', response)

        if ok:
            if (ts-1 < cur_ts < ts+61):
                logger.write(uid, ['post_challenge2', 'getflag'])
                return render_template('result.html', info=f'验证码正确！Flag 2 是：{getflag(session["token"], 2)}')
            else:
                logger.write(uid, ['post_challenge2', 'toolate'])
                return render_template('result.html', info='验证码正确，但是太慢了！少侠请重新来过。')
        else:
            logger.write(uid, ['post_challenge2', 'wrong-hash' if len(response)==CHALL_LEN else 'wrong-length'])
            return render_template('result.html', info='不对哦！')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
