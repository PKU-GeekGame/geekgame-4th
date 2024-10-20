#! /bin/sh

sudo cp /usr/lib/python3.8/random.py ./random.py.bak
sudo cp ./random.py /usr/lib/python3.8/random.py
pyinstaller --onefile pymaster.py
sudo cp ./random.py.bak /usr/lib/python3.8/random.py
