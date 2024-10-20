import json
from threading import Lock
import pathlib
import datetime

locks = {}
meta_lock = Lock()
def get_lock(uid):
    with meta_lock:
        if uid not in locks:
            locks[uid] = Lock()
        return locks[uid]

def write(uid, item):
    assert isinstance(item, list)
    ts = datetime.datetime.now()
    encoded = (json.dumps(
        [ts.timestamp(), ts.strftime('%m%d-%H%M%S')] + item,
        ensure_ascii=False,
    )+'\n').encode('utf-8')
    with get_lock(uid):
        with (pathlib.Path('logs')/f'{uid}.log').open('ab') as f:
            f.write(encoded)