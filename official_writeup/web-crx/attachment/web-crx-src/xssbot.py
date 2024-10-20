# download a chromedriver according to your chrome version here:
# https://googlechromelabs.github.io/chrome-for-testing/#stable
CHROMEDRIVER_LOCATION = '/usr/bin/chromedriver'

from selenium import webdriver
import time
import threading
import subprocess
from pathlib import Path

import flag_server
import hacker_server

try:
    print('\nInput your blog HTML below: (end with a separate line of text "EOF")\n')
    html = ''
    while True:
        line = input('')
        if line=='EOF':
            break
        html += line + '\n'
    hacker_server.HACKER_HTML = html
    
    print('\nStarting servers...')
    threading.Thread(target=flag_server.start, daemon=True).start()
    threading.Thread(target=hacker_server.start, daemon=True).start()
    time.sleep(1)
    
    ext_path = (Path(__file__).parent / 'bxx-extension').resolve()
    assert ext_path.is_dir()

    print(f'\nStarting browser with {ext_path.name}...')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # comment out this line to display the chrome GUI for debugging
    options.add_argument('--no-sandbox') # sandbox not working in docker :(
    options.add_argument(f'--load-extension={ext_path}')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    with webdriver.Chrome(options=options, service=webdriver.ChromeService(executable_path=CHROMEDRIVER_LOCATION)) as driver:
        # switch to the annoying new tab page opened by the extension
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        
        print('\nLogging in...')
        driver.get('http://127.0.1.14:1919/login')
        time.sleep(1)
        
        print('\nVisiting your blog...')
        driver.get('http://127.0.5.14:1919/blog')
        time.sleep(4)
        
        title = driver.title or '(empty)'
        print('\nThe page title is:', title)

    print('\nSee you later :)')
    
except Exception as e:
    print('ERROR', type(e))
