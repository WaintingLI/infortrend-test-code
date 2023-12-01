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
#JIRASOFWARE_IP = cf.get("APP_Info","JiraSoftware_ip")
#ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
#ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
#ADMIN_EMAIL = cf.get("APP_Info","Admin_E-Mail")
#獲取專案的名稱與設定
#PROJECT_NAME = cf.get("Project","Project_Name")
#PROJECT_KEY = cf.get("Project","Project_Key")
test_datas=list()
new_datas=list()

def save_ini(file_path: str, section: str, option: str, value: str) -> None:
    """_summary_
    用來存檔ini,且不移除註解,僅修改相對應的option值
    Args:
        file_path (str): 要修改的ini檔案路徑
        section (str): ini檔案中的section(ex:[APP_Info])
        option (str): ini檔案中的option(ex:Admin_Username)
        value (str): option要修改的值
    """
    old_datas = list()
    new_datas = list()
    FIND_FLAG = False
    if not os.path.isfile(file_path):
        print(file_path,"is not found")
        return
    #讀取檔案
    with open(file_path,"r",encoding="utf-8") as f:
        meta_datas = f.readlines()
        for item in meta_datas:
            old_datas.append(item)
    #處理字串,並且依section(ex:[APP_Info])與option(ex:Admin_Username =)來寫入對應的資料
    for index,item in enumerate(old_datas):
        #移除當前字串的所有空格,方便檢查
        string_meta = item.replace(" ","")
        #檢查當前字串是否為註解,是的話,跳過
        if string_meta[0] == "#":
            new_datas.append(old_datas[index])
            continue
        #找尋相對應的Section
        if string_meta[0] == "[":
            if string_meta[0:len(section)] == section:
                FIND_FLAG =True
            else:
                FIND_FLAG = False
        else:
            if not FIND_FLAG:
                new_datas.append(old_datas[index])
                continue
        #找到Section後,在找到相對應的option
        string_meta_2_option = string_meta[0:string_meta.find("=")]
        if string_meta_2_option == option:
            string_index = old_datas[index].find("=")
            add_string = old_datas[index][0:string_index] + "= " +value+"\n"
            new_datas.append(add_string)
        else:
            new_datas.append(old_datas[index])
    #創造或複蓋文件
    with open(file_path,"w",encoding="utf-8") as f:
        f.writelines(new_datas)

if __name__ == "__main__":
    # 要檢查的檔案路徑
    #filepath = "/etc/motd"
    filepath = "config-test.ini"

    # 檢查檔案是否存在
    if os.path.isfile(filepath):
        print("檔案存在。")
    else:
        print("檔案不存在。")
        
    save_ini("config-test.ini",
             "[User1]",
             "Password",
             "qwer123456789")
        
            
            
    '''
    print("test_data[2] =",test_datas[2])
    s= test_datas[2]
    print("長度",len(s),type(s))
    for i in s:
        print(i)
    strings = test_datas[2].split("=")
    print(strings[0])
    strings2 = "test = test =123"
    print(strings2)
    print(strings2.find("="))
    print(strings2[strings2.find("=")+1:len(strings2)+1])
    print("○●○●○●○●○●○●○●==>Test result PASS<==○●○●○●○●○●○●○●○●○●○●")
    print(strings2.replace(" ",""))
    '''