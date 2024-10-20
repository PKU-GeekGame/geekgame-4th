import json

with open('o.json') as f:
    seq = json.load(f)
    
TIMING_OFFSET = 687
RAIL_KEYS = ['alt', 'space', 'f4', 'down', 'enter', 'backspace']
RAIL_OFFSETS = [0, 86, 171, 256, 342, 427]
STEP_TIME = 60*1000/183/2
    
with open('beatmap.txt', 'w') as f:
    for idx, k in enumerate(seq):
        offset = RAIL_OFFSETS[RAIL_KEYS.index(k)]
        typ = 128 if k=='alt' else 1
        t_begin = TIMING_OFFSET + idx*STEP_TIME
        hit_sample = (f'{t_begin+STEP_TIME}:' if k=='alt' else '') + '1:0:0:100:'
        f.write(f'{offset},192,{t_begin},{typ},0,{hit_sample}\n')