# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.alert import Alert

def get_seconds(min, sec):
    return int(min) * 60 + int(sec)

def go_sleep(sec):
    time.sleep(sec)

def get_driver():
    cap = DesiredCapabilities().INTERNETEXPLORER

    cap['ignoreProtectedModeSettings'] = True
    cap['IntroduceInstabilityByIgnoringProtectedModeSettings'] = True
    cap['nativeEvents'] = True
    cap['ignoreZoomSetting'] = True
    cap['requireWindowFocus'] = True
    cap['INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS'] = True
    driver = webdriver.Ie(executable_path="IEDriverServer.exe", capabilities=cap)
    return driver

def login():
    src = '''
     var userid = $("input[name='UserID']");
     userid.focus();
     userid.val("");
     userid.val("%s");
     var loginbtn = $("button.btn_login")[0]
     loginbtn.click();
    ''' % userid

    print("input password plz..")
    driver.execute_script(src)
    time.sleep(2)

    driver.get(start_url + '/Class/Index') # 강으실 입장쿠
    time.sleep(2)

def get_score():

    time.sleep(5)

    handles_len = len(driver.window_handles)
    print("핸들 렌스 {}".format(handles_len))

    # 0: 짱 1: 부짱 2:부부짱


    driver.switch_to_window(driver.window_handles[1])
    time.sleep(5)

    driver.execute_script('''
        $("img[alt='들어가기']").click();
    ''')
    time.sleep(2) # 들어감

    driver.execute_script('''
        var $frame = $('iframe').contents().find('iframe');
        $frame.attr('src', '2.html');
    ''') # 1페이지

    time.sleep(1)

    while 1:

        driver.execute_script(jquery)

        time.sleep(10)

        while 1:

            time.sleep(5)

            t = driver.execute_script('''
                var $frame = $('iframe').contents().find('iframe');
                var $html = $frame.contents().find('html');
                return $html.find('span#d_totalTime').text();
            ''')

            if t == '00:00':
                print("[info] 시간이 로드가 안됨 {}".format(t))
                continue

            print(t)
            break

        matched = re.search('^(\d+):(\d+)$', t)
        if matched:
            sec = get_seconds(matched.group(1), matched.group(2))
            go_sleep(sec)
        else:
            raise Exception(" regex Err")

        time.sleep(1)

        existsBtn = driver.execute_script('''
            var $frame = $('iframe').contents().find('iframe');
            var $html = $frame.contents().find('html');
            var $nextbtn = $html.find('a.page_next');
            if ($nextbtn.attr('href') === '#') {
                return true;
            }
            $html.find('a.page_next')[0].click();
            return false;
        ''')  # 다음페이지

        if existsBtn:
            driver.close()
            time.sleep(5)
            Alert(driver).accept()
            driver.switch_to_window(driver.window_handles[0])
            return


def dreamscore():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for status in soup.select('td.attendResult'):
        score = "".join(re.findall("\d+", status.text.strip()))
        if score == '0':
            href = status.select_one('a')["href"]
            src = 'location.href = "%s"' % href
            driver.execute_script(src)
            get_score()


if __name__ == '__main__':

    userid = 'irnd04'

    driver = get_driver()
    driver.maximize_window()

    start_url = 'https://www.itbankcyber.com/'
    driver.get(start_url)

    with open('jquery-3.2.1.min.js', 'r') as f:
        jquery = f.read()

    login()
    dreamscore()




