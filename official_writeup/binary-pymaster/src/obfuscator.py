import zlib
import base64

f = open("challenge.py", "rb").read()

code = """code = %s
eval("exec")(
    getattr(__import__("zlib"), "decompress")(
        getattr(__import__("base64"), "b64decode")(code)
    )
)""" % base64.b64encode(
    zlib.compress(f)
)

print(code)

import marshal

code = base64.b64encode(marshal.dumps(compile(code, "", "exec")))

with open("pymaster.py", "w") as f:
    f.write("import marshal\n")
    f.write("import random\n")
    f.write("import base64\n")
    f.write("if random.randint(0, 0xFFFF) == 54830:\n")
    f.write(f"    exec(marshal.loads(base64.b64decode({code})))")
