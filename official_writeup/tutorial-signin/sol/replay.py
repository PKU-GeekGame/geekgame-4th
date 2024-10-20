import keyboard
import json
import time

DELAY = 2 * 60/183/2

_last_sleep = None
def sleep(delay):
    global _last_sleep
    ts = time.time()
    if not _last_sleep:
        _last_sleep = ts
        
    target = _last_sleep + delay
    if target>ts:
        print('  sleep', int(delay*1000/2), 'ms')
        time.sleep(target - ts)
    else:
        print('!!! bad sleep', ts-target)
    _last_sleep = target

with open('o.json') as f:
    seq = json.load(f)

print('ready?')
sleep(3)

for k in seq:
    if k=='alt':
        print('hold', k)
        keyboard.press(k)
    elif k=='f4':
        print('press', k)
        keyboard.press_and_release(k)
        #sleep(DELAY)
        print('release', 'alt')
        keyboard.release('alt')
    else:
        print('press', k)
        keyboard.press_and_release(k)
    sleep(DELAY)