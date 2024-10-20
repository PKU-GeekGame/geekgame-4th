import json
import pickle
import zipfile
import io
from pathlib import Path

with open('sentences.json', encoding='utf-8') as f:
    SENTENCES = json.load(f)

with open('ids.json', encoding='utf-8') as f:
    IDS = json.load(f)

MOD_TIME = (2024, 10, 12, 11, 59, 59)

def gen_zip_impl(real_flag: str, codepath: list[int]) -> bytes:
    lv = len(codepath)

    if lv==4:
        o1, o2, o3, o4 = codepath
        offset = o1*27 + o2*9 + o3*3 + o4
        ret = SENTENCES[offset]

        if ret=='__FLAG__':
            ret = real_flag
        return ret.encode()

    o1, o2, o3, o4, *_ = codepath + [0, 0, 0, 0]
    base_offset = 3 * (o1 + o2*3 + o3*9 + o4*27)

    f = io.BytesIO()
    with zipfile.ZipFile(f, 'w', compresslevel=3) as z:
        for idx in range(3):
            fn = IDS[str(lv+1)][base_offset+idx] + ('.txt' if lv==3 else '.zip')
            content = gen_zip(real_flag, codepath + [idx])

            info = zipfile.ZipInfo(fn, MOD_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, content)

        if lv==0:
            info = zipfile.ZipInfo('README.txt', MOD_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, 'Flag在其中的一个压缩包里。是哪个呢？')

    return f.getvalue()

def gen_zip_savecache(real_flag: str, codepath: list[int]) -> bytes:
    can_cache = codepath not in [[], [2], [2, 0], [2, 0, 1], [2, 0, 1, 0]]

    ret = gen_zip_impl(real_flag, codepath)
    if can_cache:
        print('  saved', codepath)
        saved_parts[tuple(codepath)] = ret
    else:
        print('!!!skipped', codepath)
    
    return ret

def gen_zip_cached(real_flag: str, codepath: list[int]) -> bytes:
    if tuple(codepath) in saved_parts:
        return saved_parts[tuple(codepath)]
    else:
        return gen_zip_impl(real_flag, codepath)

gen_zip = gen_zip_cached
#gen_zip = gen_zip_savecache
with open('saved_parts.pickle', 'rb') as f:
    saved_parts = pickle.load(f)

def gen(user, ch) -> Path:
    flag = ch.flags[0].correct_flag(user)

    dst_path = Path('_gen').resolve() / str(user._store.id)
    dst_path.mkdir(exist_ok=True, parents=True)

    out_path = dst_path / 'attachment.zip'

    with out_path.open('wb') as f:
        f.write(gen_zip(flag, []))
    
    return out_path

if __name__ == '__main__':
    # saved_parts = {}
    # gen_zip = gen_zip_savecache
    # gen_zip_savecache('fake{}', [])
    # with open('saved_parts.pickle', 'wb') as f:
    #     pickle.dump(saved_parts, f)

    with open('play.zip', 'wb') as f:
        f.write(gen_zip('fake{}', []))