# download a chromedriver according to your chrome version here:
# https://googlechromelabs.github.io/chrome-for-testing/#stable
CHROMEDRIVER_LOCATION = '/usr/bin/chromedriver'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import threading
from pathlib import Path
import subprocess

def challenge_1(code):
    try:
        FLAG1 = Path('/flag1').read_text().strip()
    except Exception:
        print('Cannot find flag file!')
        FLAG1 = 'fake{get flag1 on the server}'
    
    print('\nStarting browser...')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # comment out this line to display the chrome GUI for debugging
    options.add_argument('--no-sandbox') # sandbox not working in docker :(
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    with webdriver.Chrome(options=options, service=webdriver.ChromeService(executable_path=CHROMEDRIVER_LOCATION)) as driver:
        print('\nVisiting WebPPL website...')
        driver.get(f'file://{Path("webppl_site/index.html").resolve()}')
        time.sleep(1)
        
        def run_code(c):
            (ActionChains(driver)
            # click the editor
                .click(driver.find_element(By.CLASS_NAME, 'CodeMirror-code'))
            # delete everything
                .key_down(Keys.CONTROL)
                .send_keys('a')
                .key_up(Keys.CONTROL)
                .send_keys(Keys.DELETE)
            # input the code
                .send_keys(c)
            # sometimes the editor auto-complete redundant parentheses, delete them
                .key_down(Keys.SHIFT)
                .send_keys(Keys.END)
                .key_up(Keys.SHIFT)
                .send_keys(Keys.DELETE)
            # done
                .perform()
            )
            time.sleep(.5)
            
            driver.find_element(By.CLASS_NAME, 'run').click()
            time.sleep(1)
        
        print('\nRunning flag...')
        run_code(f'console.log("{FLAG1}")')
        
        print('\nRunning your code...')
        run_code(code)
        
        title = driver.title
        print('\nThe page title is:', title)
        
    print('\nSee you later :)')
    
def challenge_2(code):
    if not Path('/flag2').is_file():
        print('Cannot find flag file!')

    with open('/tmp/code.wppl', 'w', encoding='utf-8') as f:
        f.write(code)
        
    print('\nRunning your code...')
    subprocess.run('bash ./driver.sh', shell=True)
    
    out_path = Path('/tmp/output.txt')
    if out_path.is_file():
        print('\nThe output is:')
        print(out_path.read_text())
    else:
        print('\nOutput does not exist!')
    
try:
    print('\nInput your webppl script below: (end with a separate line of text "EOF")\n')
    code = ''
    while True:
        line = input('')
        if line=='EOF':
            break
        code += line + '\n'
        
    ch = int(input('\nWhich challenge? (1 for browser, 2 for nodejs): '))
    if ch==1:
        challenge_1(code)
    elif ch==2:
        challenge_2(code)
    else:
        print('What challenge is this?')
        
except Exception as e:
    print('ERROR', type(e))