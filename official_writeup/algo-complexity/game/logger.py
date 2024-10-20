import json
import os
import pathlib
import datetime

def write(uid, item):
    assert isinstance(item, list)
    
    if uid is None:
        uid = int(os.environ['hackergame_token'].partition(':')[0])
    
    ts = datetime.datetime.now()
    encoded = (json.dumps(
        [ts.timestamp(), ts.strftime('%m%d-%H%M%S')] + item,
        ensure_ascii=False,
    )+'\n').encode('utf-8')
    
    with (pathlib.Path('logs')/f'{uid}.log').open('ab') as f:
        f.write(encoded)