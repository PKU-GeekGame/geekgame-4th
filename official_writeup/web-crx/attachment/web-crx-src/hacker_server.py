from flask import *

app = Flask(__name__)

HACKER_HTML = '...'

@app.get('/blog')
def blog():
    return HACKER_HTML
    
def start():
    app.run(host='127.0.5.14', port=1919)