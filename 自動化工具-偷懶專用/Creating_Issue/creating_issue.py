'''
用來自動化發Issue時,所需要的常用資料
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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import Select
import requests
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
BINARY_LOCATION='C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chrome-win64/chrome.exe'
options.binary_location=BINARY_LOCATION
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chromedriver-win64/chromedriver.exe")


#啟動chrome
driver = webdriver.Chrome(service=service, options=options)
#隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
driver.implicitly_wait(10)




#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
REDMINE_IP = cf.get("APP_Info","Redmine_ip")
SUBJECT =  cf.get("APP_Info","Subject")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
ADMIN_EMAIL = cf.get("APP_Info","Admin_E-Mail")
FILE_PATH = cf.get("APP_Info","Watcher_list")
#獲取使用者資料
USER1_NAME = cf.get("User1","User1_Name")
USER1_APPELLATION = cf.get("User1","User1_Appellation")
USER1_EMAIL = cf.get("User1","User1_Email")
USER1_PASSWORD = cf.get("User1","User1_Password")



def check_element(driver_2:WebDriver,element:WebElement,sec:int):
    """_summary_
    用來確定按鈕可以被看到與點擊
    Example:
        check_element(driver,element=(By.LINK_TEXT,("Content")),sec=15)
    Args:
        driver (WebDriver): 所使用得瀏覽器
        element (WebElement): 網頁元素,例如:
        sec (int): _description_
    """
    try:
        WebDriverWait(driver_2,int(sec)).until(EC.element_to_be_clickable(element)).click()
    except Exception as e:
        print(f"An error occurred: {e}")
        driver_2.close()
        driver_2.quit()
        sys.exit(1)


if __name__ == "__main__":
    #檢查網頁是否連線正常
    response = requests.get(REDMINE_IP, timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",REDMINE_IP)
        sys.exit(1)

    #開啟網址
    driver.get(REDMINE_IP)
    
    
    #登入
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#username")))
    driver.find_element(By.CSS_SELECTOR,"input#username").send_keys("自己的帳號")
    driver.find_element(By.CSS_SELECTOR,"input#password").send_keys("自己的密碼")
    driver.find_element(By.CSS_SELECTOR,"input#login-submit").click()
    sleep(3)
    #開始設定Issue
    driver.find_element(By.CSS_SELECTOR,"input#issue_subject").send_keys(SUBJECT)
    select_status = Select(driver.find_element(By.CSS_SELECTOR,"select#issue_status_id"))
    select_status.select_by_visible_text("Assigned")
    #由於上面的程式會影響亞面的填值,所以需要停止一會
    sleep(3)
    select_priority = Select(driver.find_element(By.CSS_SELECTOR,"select#issue_priority_id"))
    select_priority.select_by_visible_text("High (3)")
    
    select_assignee = Select(driver.find_element(By.CSS_SELECTOR,"select#issue_assigned_to_id"))
    select_assignee.select_by_visible_text("Hank Su")
    
    select_category = Select(driver.find_element(By.CSS_SELECTOR,"select#issue_category_id"))
    select_category.select_by_visible_text("Maintain")
    
    
    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"span.search_for_watchers > a"))).click()
    if not os.path.isfile(FILE_PATH):
        print(FILE_PATH,"is not found")
    else:
        with open(FILE_PATH,"r",encoding="utf-8") as f:
            meta_data = f.readlines()
            for watcher in meta_data:
                watcher = watcher.rstrip("\n")
                print("Add Watcher:",watcher)
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"span.search_for_watchers > a"))).click()
                print("收尋:",watcher)
                
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#user_search"))).send_keys(watcher)
                try:
                    get_watcher = WebDriverWait(driver, 10)\
                        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#users_for_watcher > label:first-child"))).text
                except StaleElementReferenceException:
                    pass
                except NoSuchElementException:
                    print("無此人=>",watcher)
                #get_watcher = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#users_for_watcher > label:first-child"))).text
                while(get_watcher != watcher):
                    print("收尋到誰=>",get_watcher)
                    try:
                        get_watcher = WebDriverWait(driver, 10)\
                            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#users_for_watcher > label:first-child"))).text
                    except StaleElementReferenceException:
                        pass
                    except NoSuchElementException:
                        print("無此人=>",watcher)
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#users_for_watcher > label:first-child"))).click()
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"form#new-watcher-form > p.buttons > input[type=submit]"))).click()
    exit(0)
    
