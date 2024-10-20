import os

while True:
    zip_files = [f for f in os.listdir() if f.endswith('.zip')]
    if not zip_files:
        break
    zip_file = zip_files[0]
    os.system(f'unzip {zip_file}')
    os.system(f'rm {zip_file}')

txts = [f for f in os.listdir() if f.endswith('.txt')]
for txt in txts:
    with open(txt) as f:
        content = f.read()
        print(content)
