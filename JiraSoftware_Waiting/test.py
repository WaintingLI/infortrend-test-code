'''
用來自動化測試Jira Software
'''
from time import sleep
import sys
import os
import configparser
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
import random
#import clipboard



#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#設定Chrome driver 的相關屬性
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument("--disable-gpu")
options.add_argument('ignore-certificate-errors')
options.add_argument('disable-application-cache')
#最大化窗口
options.add_argument('--start-maximized')
#options.add_argument('window-size=1600x900')
#options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#driver_location='/usr/bin/chromedriver'
#指令Chromedriver位置
#BINARY_LOCATION='./chrome-win64/chrome.exe'
#options.binary_location=BINARY_LOCATION
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="./chromedriver.exe")


#啟動chrome
#driver = webdriver.Chrome(service=service, options=options)
#隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
#driver.implicitly_wait(10)

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
JIRASOFWARE_IP = cf.get("APP_Info","JiraSoftware_ip")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
ADMIN_EMAIL = cf.get("APP_Info","Admin_E-Mail")
#獲取專案的名稱與設定
PROJECT_NAME = cf.get("Project","Project_Name")
PROJECT_KEY = cf.get("Project","Project_Key")



if __name__ == "__main__":
    str=''
    str2=''
    a=str.join(random.choice("0123456789ABCDEF") for i in range(16))
    
   
    print(a)
    for i in range(10):
        list_test = random.choices("0123456789ABCDEF", k=16)
        s = ''.join(list_test)
        print("s =",s)
    
    print("○●○●○●○●○●○●○●==>Test result PASS<==○●○●○●○●○●○●○●○●○●○●")
