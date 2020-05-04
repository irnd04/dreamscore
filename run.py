from selenium import webdriver
import time

driver = webdriver.Ie('IEDriverServer.exe')
driver.maximize_window()

driver.get('https://www.naver.com')

time.sleep(.5)

driver.execute_script('''
    document.querySelector('html').innerHTML = ''
''')