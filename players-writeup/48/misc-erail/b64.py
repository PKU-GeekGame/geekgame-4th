import base64
with open('b64.txt', 'r') as f:
    data = f.read()
    # remove '\n'
    data = data.replace('\n', '')
    data = base64.b64decode(data)
    with open('b64.out', 'wb') as f2:
        f2.write(data)