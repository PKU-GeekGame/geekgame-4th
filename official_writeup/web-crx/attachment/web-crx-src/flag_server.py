from flask import *

from pathlib import Path
try:
    FLAG1 = Path('/flag1').read_text().strip()
    FLAG2 = Path('/flag2').read_text().strip()
except Exception:
    FLAG1 = 'fake{get flag1 on the real server}'
    FLAG2 = 'fake{get flag2 on the real server}'

app = Flask(__name__)

@app.route('/login')
def login():
    resp = make_response('OK')
    resp.set_cookie('login', 'yes', httponly=True, samesite='strict')
    return resp
    
@app.route('/admin')
def admin():
    login = request.cookies.get('login')
    if login=='yes':
        print('FLAG SERVER: your flag is', FLAG1)
        return 'another flag is '+FLAG2
    else:
        print('FLAG SERVER: not logged in :(')
        return 'no flag for you'
        
def start():
    app.run(host='127.0.1.14', port=1919)