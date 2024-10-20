import base64
data="amtj=78e1VY=6CdkNO=77Um5h=58b1da=50a0hE=6EZnJE=61bkdp=41c3Z6=6BY30="
data = data[:-1]
result = ""
buffered_b64 = ""
i = 0

while i < len(data):
    if data[i] == "=":
        assert(i + 2 < len(data))
        result += base64.b64decode(buffered_b64).decode()
        # result += '|'
        buffered_b64 = ""
        result += chr(int(data[i + 1:i + 3], 16))
        # result += "|"
        i += 3
    else:
        buffered_b64 += data[i]
        i += 1

if buffered_b64:
    # refill the previously discarded "="
    print(buffered_b64 + "=")
    result += base64.b64decode(buffered_b64 + "=").decode()

print(result)
