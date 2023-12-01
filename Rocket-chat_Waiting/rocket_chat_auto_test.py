'''
用來自動化測試Rocket Chat
'''
from time import sleep
import sys
import os
import configparser
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
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
#BINARY_LOCATION='./chrome-win64/chrome.exe'
#options.binary_location=BINARY_LOCATION
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="./chromedriver.exe")


#啟動chrome
driver = webdriver.Chrome(service=service, options=options)
#隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
driver.implicitly_wait(10)

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
ROCKET_CAHT_IP = cf.get("APP_Info","Rocket_chat_ip")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
ADMIN_EMAIL = cf.get("APP_Info","Admin_E-Mail")
#獲取使用者資料
USER1_NAME = cf.get("User1","User1_Name")
USER1_APPELLATION = cf.get("User1","User1_Appellation")
USER1_EMAIL = cf.get("User1","User1_Email")
USER1_PASSWORD = cf.get("User1","User1_Password")

def check_element(driver:WebDriver,element:WebElement,sec:int):
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
        WebDriverWait(driver,int(sec)).until(EC.element_to_be_clickable(element)).click()
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.close()
        driver.quit()
        sys.exit(1)

def login_rocket_chat(web_driver:WebDriver,usremail:str, usrpaswd:str) -> None:
    """_summary_
    登入rocket chat,須提前開啟登入頁面
    Args:
        web_driver (WebDriver): 使用的瀏覽器
        usremail (str): 要登入的電子郵件或者使用者名稱
        usrpaswd (str): 要登入的密碼
    """
    WebDriverWait(web_driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#username"))).send_keys(usremail)
    #web_driver.find_element(By.CSS_SELECTOR,"input#username").send_keys(ADMIN_EMAIL)
    web_driver.find_element(By.CSS_SELECTOR,"input#password").send_keys(usrpaswd)
    web_driver.find_element(By.CSS_SELECTOR,"div#react-root > div > div > div.rcx-css-1tmhcn7 > form > footer > div > button").click()
    try:
        login_error_message = WebDriverWait(web_driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.rcx-box.rcx-box--full.rcx-callout__children"))).text
        #login_error_message = driver.find_element(By.CSS_SELECTOR,"div.rcx-box.rcx-box--full.rcx-callout__children").text
        print(usremail," Log in Fail !!! \n",login_error_message)
        sys.exit(1)
    except TimeoutException:
        print("Log in successfully !!!")


def add_new_user(web_driver:WebDriver, 
                 user_name:str, 
                 user_apel:str, 
                 user_email:str, 
                 user_password:str
                 ) -> None:
    """_summary_
    需要使用admin帳號來創建新的使用者
    Args:
        web_driver (WebDriver): 已經登入admin帳號的瀏覽器
        user_name (str): 要新創的使用者的名稱
        user_apel (str): 要新創的使用者的暱稱
        user_email (str): 要新創的使用者的電子郵件
        user_password (str): 要新創的使用者的密碼
    """
    #"http://172.24.128.145/admin/users/new"
    web_driver.get(ROCKET_CAHT_IP+"admin/users/new")
    #要輸入的姓名
    WebDriverWait(web_driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,\
        "div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > fieldset > div:nth-child(1) > span > input"\
            ))).send_keys(user_name)
    #web_driver.find_element(By.CSS_SELECTOR,"div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > fieldset > div:nth-child(1) > span > input").send_keys(USER1_NAME)
    #輸入使用者名稱
    web_driver.find_element(By.CSS_SELECTOR,"div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > fieldset > div:nth-child(2) > span > label > input").send_keys(user_apel)
    #輸入電子郵件
    web_driver.find_element(By.CSS_SELECTOR,"div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > fieldset > div:nth-child(3) > span:nth-child(2) > label > input").send_keys(user_email)
    #滑動開關(已驗證)
    web_driver.find_element(By.CSS_SELECTOR,"div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > fieldset > div:nth-child(3) > span:nth-child(3) > div > label > i").click()
    #輸入密碼
    web_driver.find_element(By.CSS_SELECTOR,"div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > form > div:nth-child(1) > span > label > input").send_keys(user_password)
    #按下儲存
    WebDriverWait(web_driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,\
        "div#rocket-chat > div.rc-old.main-content > section > div > div > div > div.rc-scrollbars-view > form > form > div:nth-child(9) > span > div > button.rcx-box.rcx-box--full.rcx-box--animated.rcx-button--primary.rcx-button.rcx-css-t3n91h"\
            ))).click()
    try:
        list_message = web_driver.find_element(By.CSS_SELECTOR,"div#toastBarRoot > div > div > div > div.rcx-toastbar_inner > div.rcx-toastbar_content")
        print(list_message.text)
        #for item in list_message:
        #    print(item.text)
    except NoSuchElementException:
        print(user_apel,"Created")

def commit_message(web_driver:WebDriver, message:str) -> None:
    """_summary_
    在登入的狀態下,到General Channel發送信息
    Args:
        web_driver (WebDriver): 要使用的瀏覽器
        message (str): 要發送的信息
    """
    if not web_driver.current_url == (ROCKET_CAHT_IP+"channel/general"):
        web_driver.get(ROCKET_CAHT_IP+"channel/general")
    web_driver.find_element(By.CSS_SELECTOR,"section#chat-window-GENERAL > div > div > footer > div.rcx-box.rcx-box--full.rcx-input-box__wrapper.rcx-css-o7c782 > label > textarea").send_keys(message)
    #driver.find_element(By.CSS_SELECTOR,"section#chat-window-GENERAL > div > div > footer > div.rcx-box.rcx-box--full.rcx-input-box__wrapper.rcx-css-o7c782 > div.rcx-box.rcx-box--full.rcx-css-116ma9g > div:nth-child(2) > button").click()
    check_element(web_driver,
                  (By.CSS_SELECTOR,"section#chat-window-GENERAL > div > div > footer > div.rcx-box.rcx-box--full.rcx-input-box__wrapper.rcx-css-o7c782 > div.rcx-box.rcx-box--full.rcx-css-116ma9g > div:nth-child(2) > button"),
                  10)
    print("Send Message =>", message)

def check_message(web_driver:WebDriver,checking_message:str) -> None:
    """_summary_
    在登入狀態下,到general channel中,檢查使否該對話中,有該字串
    Args:
        web_driver (WebDriver): 要使用的瀏覽器
        checking_message (str): 要檢查的字串
    """
    if not web_driver.current_url == (ROCKET_CAHT_IP+"channel/general"):
        web_driver.get(ROCKET_CAHT_IP+"channel/general")
    #message_lists = driver.find_elements(By.CSS_SELECTOR,"section#chat-window-GENERAL > div > div > div.messages-box > div > div > div.rc-scrollbars-view > ul.messages-list > div.rcx-message")
    message_lists = web_driver.find_elements(By.CSS_SELECTOR,"section#chat-window-GENERAL > div > div > div.messages-box > div > div > div.rc-scrollbars-view > ul.messages-list > div.rcx-message > div > div.rcx-message-body")
    for message in message_lists:
        if message.text == checking_message:
            print("Receive Message =>"+message.text)
            break
    else:
        print("No Message found  =>"+message.text)
        print("TEST Fail !!!")
        sys.exit(1)

def random_16_hex_number() -> str:
    """_summary_
    產生亂數的16進位亂數,會回傳16個數字
    Returns:
        str: 字串型態的16
    """
    random_list_number = random.choices("0123456789ABCDEF", k=16)
    random_hex_number = ''.join(random_list_number)
    return random_hex_number

if __name__ == "__main__":
    #檢查網頁是否連線正常
    response = requests.get(ROCKET_CAHT_IP, timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",ROCKET_CAHT_IP)
        sys.exit(1)

    #開啟網址
    driver.get(ROCKET_CAHT_IP)
    sleep(3)
    #登入帳號:
    login_rocket_chat(driver, ADMIN_EMAIL, ADMIN_PASSWORD)

    #新增使用者
    add_new_user(driver, USER1_NAME, USER1_APPELLATION, USER1_EMAIL, USER1_PASSWORD)

    #===========開啟新的使用瀏覽器來登入另外一個使用者=======
    user1_driver = webdriver.Chrome(service=service, options=options)
    #隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
    user1_driver.implicitly_wait(10)
    #user1登入rocket-chat
    user1_driver.get(ROCKET_CAHT_IP)
    login_rocket_chat(user1_driver, USER1_EMAIL, USER1_PASSWORD)
    
    SEND_MESSAGE = random_16_hex_number()
    #==========對話測試, admin to user1==========
    print("auto-test=> admin talk to user1")
    commit_message(driver, SEND_MESSAGE)
    #傳誦與接收間隔
    sleep(3)
    #確認使否有接收到信息
    check_message(user1_driver, SEND_MESSAGE)

    #==========對話測試, user1 to admin==========
    print("auto-test=> user1 talk to admin")
    commit_message(driver, SEND_MESSAGE)
    #傳誦與接收間隔
    sleep(3)
    #確認使否有接收到信息
    check_message(user1_driver, SEND_MESSAGE)

    sleep(10)
    driver.close()
    user1_driver.close()
    print("○●○●○●○●○●○●○●==>Test result PASS<==○●○●○●○●○●○●○●○●○●○●")
