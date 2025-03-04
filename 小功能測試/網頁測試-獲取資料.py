'''
用來當作瀏覽器的範本
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
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException
import requests



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
driver = webdriver.Chrome(service=service, options=options)
#隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
driver.implicitly_wait(30)

#讀取檔案參數與全域變數
'''
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
OPENCART_IP = cf.get("APP_Info","OpenCart_ip")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
#獲取使用者1資訊
USER1_FIRST_NAME = cf.get("User1","First_Name")
USER1_LAST_NAME = cf.get("User1","Last_Name")
USER1_E_MAIL = cf.get("User1","E-Mail")
USER1_PASSWORD = cf.get("User1","Password")
#獲取使用者2資訊
USER2_FIRST_NAME = cf.get("User2","First_Name")
USER2_LAST_NAME = cf.get("User2","Last_Name")
USER2_E_MAIL = cf.get("User2","E-Mail")
USER2_PASSWORD = cf.get("User2","Password")
#Chekcout時，所需要的資料
ADDRESS = cf.get("CheckOut","Address")
CITY = cf.get("CheckOut","City")
POST_CODE = cf.get("CheckOut","Post_Code")
'''

def waiting_time(x):
    '''
    用來等待網頁載入的時間
    '''
    for i in range(x):
        print("等待時間剩餘秒數 => ", (x-i))
        sleep(1)

def check_item(item):
    '''
    檢查物件是否存在
    '''
    match item:
        case "HTC Touch HD":
            return "HTC Touch HD is existing"

        case "Palm Treo Pro":
            return "Palm Treo Pro is existing"

        case "iPhone":
            return "iPhone is existing"

        case _:
            new_string = item + " is empty"
            print(new_string)
            sys.exit(1)




if __name__ == "__main__":
    #檢查網頁是否連線正常
    response = requests.get("https://www.google.com/", timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",OPENCART_IP)
        sys.exit(1)

    #開啟網址
    driver.get("https://www.coinglass.com/zh-TW/FundingRate")
    while True:
        crypto_exchanges = driver.find_elements(By.CSS_SELECTOR,"thead.ant-table-thead > tr > th.ant-table-column-has-sorters")
    
        for index, item in enumerate(crypto_exchanges):
            print(item.text)
            if item.text == "BingX":
                print("get => ",item.text )
                print("Index => ",index)
                break
    
    
        print("item.text =>",item.text)
        string_data = item.get_attribute("aria-sort")
        #ascending, descending
        print("string_data =",string_data)
        if string_data != "ascending":
            item.click()
        while True:
            print(item.get_attribute("aria-sort"))
            item.click()
            sleep(1)
            
        #獲取當前貨幣排序
        #div.ant-table-body > table > tbody > tr.data-row-key
        #div.ant-table-body > table > tbody > tr.ant-table-row
        crypto_names = driver.find_elements(By.CSS_SELECTOR,"div.ant-table-body > table > tbody > tr.ant-table-row")
        for number, item2 in enumerate(crypto_names):
            print("number =>",number , item2.get_attribute("data-row-key"))
            #獲取當前幣種的列
            current_crypto_colume = item2.find_elements(By.CSS_SELECTOR,"td.ant-table-cell")
            print("欄位 =>",current_crypto_colume[index+2].find_element(By.CSS_SELECTOR,"a.shou").text)
        "-"
        sleep(2)
    
            


    
    while True:
        pass
    driver.close()
    print("○●○●○●○●○●○●○●==>測試結果 PASS<==○●○●○●○●○●○●○●○●○●○●")
