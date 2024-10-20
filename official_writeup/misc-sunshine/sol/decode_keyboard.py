from ast import literal_eval

with open('data/sunshine.log') as f:
    t = f.read()
    
for chunk in t.split('Debug: --begin keyboard packet--')[1:]:
    chunk = chunk.partition('--end keyboard packet--')[0]
    action = literal_eval('0x'+chunk.partition('keyAction [')[2].partition(']')[0])
    keycode = literal_eval('0x'+chunk.partition('keyCode [')[2].partition(']')[0])
    modifiers = literal_eval('0x'+chunk.partition('modifiers [')[2].partition(']')[0])
    
    key = chr(keycode-0x8000)
    # https://github.com/LizardByte/Sunshine/blob/fb712e30a06eb5824d1d8803c5886871aeb21231/src/input.cpp#L41-L49
    key = {
        '\x10': 'shift',
        '\xA0': 'lshift',
        '\xA1': 'rshift',
        '\x11': 'ctrl',
        '\xA2': 'lctrl',
        '\xA3': 'rctrl',
        '\x12': 'menu',
        '\xA4': 'lmenu',
        '\xA5': 'rmenu',
        '\r': 'enter',
        ' ': 'space',
        '\t': 'tab',
    }.get(key, key)
    
    action = {
        3: 'down',
        4: 'up',
    }.get(action, action)
    
    if action=='down':
        print(key)