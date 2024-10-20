from collections import deque
import time

import logger

LIMIT_PERIOD = 61
REPORT_INTERVAL = 61
MAX_CALL = 485
MAX_TOKENS = 290000

history = deque()
last_report_ts = 0

def cleanup(cur_ts):
    while len(history)>0:
        ts, _ = history[0]
        if cur_ts - ts < LIMIT_PERIOD:
            return
        history.popleft()

def exceeded():
    global last_report_ts
    
    cur_ts = time.time()
    cleanup(cur_ts)
    
    tot_call = len(history)
    tot_tokens = sum([x[1] for x in history])
    
    if cur_ts - last_report_ts > REPORT_INTERVAL:
        logger.write('sys', ['stats', tot_call, tot_tokens])
        last_report_ts = cur_ts
    
    return tot_call>MAX_CALL or tot_tokens>MAX_TOKENS
    
def report(usage):
    history.append((time.time(), usage))
