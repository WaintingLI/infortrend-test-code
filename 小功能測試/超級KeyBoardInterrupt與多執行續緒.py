import threading
import hashlib
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import time
import sys,os,re
import logging
import configparser



#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地，如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))
    
#設定Chrome driver 的相關屬性
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument("--disable-gpu")
options.add_argument('ignore-certificate-errors')
options.add_argument('disable-application-cache')
options.add_argument('window-size=1600x900')
#options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#driver_location='/usr/bin/chromedriver'
#binary_location='/usr/bin/google-chrome'
#options.binary_location=binary_location
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="./chromedriver.exe")
#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
CHATWOOT_IP = cf.get("APP_Info","TEST_ip")

REFRESH_FILE_VARIABLE = False               #用來判斷是否更新從檔案獲取的變數
#啟動chrome

#driver = webdriver.Chrome(service=service, options=options)


def test_threading():
    global REFRESH_FILE_VARIABLE
    md5_hold = hashlib.md5(open('config.ini', 'r', encoding='UTF-8').read().encode('utf-8')).hexdigest()
    
    while True:
        sleep(1)
        if md5_hold != hashlib.md5(open('config.ini', 'r', encoding='UTF-8').read().encode('utf-8')).hexdigest():
            REFRESH_FILE_VARIABLE = True
            md5_hold = hashlib.md5(open('config.ini', 'r', encoding='UTF-8').read().encode('utf-8')).hexdigest()
            
def asdf():
    global CHATWOOT_IP
    cf=configparser.ConfigParser()
    cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
    CHATWOOT_IP = cf.get("APP_Info","TEST_ip")

def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook
    
    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            print("\nKeyboardInterrupt...")
            print("do something")
            
    sys.excepthook = new_hook


#啟動多執行續
a = threading.Thread(target=test_threading)  # 建立新的執行緒
a.daemon = True                                 #當主程序退出，該執行緒也會跟著結束

if __name__ == "__main__":
    suppress_keyboard_interrupt_message()
    a.start()
    while True:
        sleep(1)
        if REFRESH_FILE_VARIABLE:
            asdf()
            print("檔案有變動")
            REFRESH_FILE_VARIABLE =False
            print(CHATWOOT_IP)
            