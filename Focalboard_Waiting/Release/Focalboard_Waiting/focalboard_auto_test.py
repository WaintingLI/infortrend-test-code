'''
用來自動化測試Focal Board
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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import clipboard
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
driver.implicitly_wait(10)

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
FOCALBOARD_IP = cf.get("APP_Info","Focalboard_ip")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
ADMIN_PASSWORD_2 = cf.get("APP_Info","Admin_Password_2")
ADMIN_EMAIL = cf.get("APP_Info","Admin_E-Mail")
#獲取使用者1資訊
USER1_NAME = cf.get("User1","Name")
USER1_E_MAIL = cf.get("User1","E-Mail")
USER1_PASSWORD = cf.get("User1","Password")

#用來判斷說是否已經有第一個帳戶
ALREADY_HAVE_FIRST_ACCOUNT_FLAG = False




def click_button(a):
    '''
    點擊按鈕
    
    Args:
     - a = WebDriver物件
    Example:
     click_button(driver.find_element(By.CSS_SELECTOR,"button#button-payment-methods"))
    '''
    #滾動到當前的元素位置
    #driver.execute_script("arguments[0].scrollIntoView();", element)
    element = a
    driver.execute_script("arguments[0].click();",element)


def creat_first_account() -> None:
    """_summary_
    
    創建第一個帳戶,僅創建第一個帳戶可以使用,創建完後,會直接登入focalboard頁面
    """
    global ALREADY_HAVE_FIRST_ACCOUNT_FLAG
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > a")))
    element.click()
    sleep(2)
    driver.find_element(By.CSS_SELECTOR,"input#login-email").send_keys(ADMIN_EMAIL)
    driver.find_element(By.CSS_SELECTOR,"input#login-username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.CSS_SELECTOR,"input#login-password").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR,"div#main > div > form > button > span").click()
    try:
        sleep(0.1)
        register_error_message = driver.find_element(By.CSS_SELECTOR,"div#main > div > div.error").text
        print("Error, Register is not created")
        print(register_error_message)
        ALREADY_HAVE_FIRST_ACCOUNT_FLAG = True
        driver.get(FOCALBOARD_IP)
    except NoSuchElementException:
        print("Register Created !!!")
        

def login_focalboard(login_username:str, login_password:str) -> None:
    """_summary_
    記得先要到登入頁面
    Args:
        login_username (str): 要登入的使用者
        login_password (str): 要登入的密碼
    """
    global ALREADY_HAVE_FIRST_ACCOUNT_FLAG
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#login-username")))
    element.send_keys(login_username)
    driver.find_element(By.CSS_SELECTOR,"input#login-password").send_keys(login_password)
    driver.find_element(By.CSS_SELECTOR,"div#main > div > form > button > span").click()
    login_focalboard_error_message = driver.find_element(By.CSS_SELECTOR,"div#main > div > div").text
    if login_focalboard_error_message != "Login failed":
        print("Log in Successfully !!!")
        ALREADY_HAVE_FIRST_ACCOUNT_FLAG = True
    else:
        print("Log in Fail")
        print(login_focalboard_error_message)
        sys.exit(1)

def change_password(old_password:str, new_password:str) -> None :
    """_summary_
    請務必在登入帳戶後，才使用該程式，用來測試更改帳戶密碼

    Args:
        old_password (str): 原本的密碼
        new_password (str): 新的密碼
    """
    driver.get(FOCALBOARD_IP+"change_password")
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#login-oldpassword")))
    element.send_keys(old_password)
    driver.find_element(By.CSS_SELECTOR,"input#login-newpassword").send_keys(new_password)
    driver.find_element(By.CSS_SELECTOR,"div#main > div > form > button > span").click()
    try:
        #Password changed, click to continue.
        change_password_message = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#main > div > a.succeeded"))).text
    except NoSuchElementException:
        change_password_message = driver.find_element(By.CSS_SELECTOR,"div#main > div > div.error").text
    if change_password_message == "Password changed, click to continue.":
        print("Change Password Successfully !!!")
        driver.get(FOCALBOARD_IP)
    else:
        print("Change Password Fail")
        print(change_password_message)
        sys.exit(1)

def log_out() -> None:
    """_summary_
    要記得登入帳號後,回到最一開始的頁面,才能使用自動登出的程式
    """
    driver.get(FOCALBOARD_IP)
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-header > div.heading > div > div > div > div > div > span")))
    element.click()
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-header > div.heading > div > div > div > div.Menu.noselect.bottom > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)")))
    element.click()
    

def add_board(board_name = "Meeting Agenda") -> None:
    """_summary_

    Args:
        board_name (str, optional): 輸入要增加的Board Name就會自行創建. Defaults to "Meeting Agenda". "Content Calendar"
    """
    try:
        #只有在還沒有任何一個Board時，可以使用
        board_list = driver.find_elements(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.mainFrame > div > div > div.templates > div.templates-sidebar > div.templates-list > div > span.template-name")
        for item in board_list:
            if item.text == board_name:
                print("Add board name => ",item.text)
                item.click()
                break
        driver.find_element(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.mainFrame > div > div > div.templates > div.templates-content > div.buttons > button").click()
        #不知道為什麼創完後，不會更新網頁畫面，所以強制更新
        driver.refresh()
        #print("第一種方式")
    except NoSuchElementException:
        #print("第二種方式")
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.add-board")))
        element.click()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > div.Workspace > div.mainFrame > div.BoardTemplateSelector__container > div.BoardTemplateSelector > div.templates > div.templates-sidebar > div.templates-list > div")))
        board_list = driver.find_elements(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.mainFrame > div.BoardTemplateSelector__container > div.BoardTemplateSelector > div.templates > div.templates-sidebar > div.templates-list > div > span.template-name")
        for item in board_list:
            if item.text == board_name:
                print("Add board name => ",item.text)
                item.click()
                sleep(3)
                driver.find_element(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.mainFrame > div.BoardTemplateSelector__container > div.BoardTemplateSelector > div.templates > div.templates-content > div.buttons > button").click()
            #    #需要強制睡眠，不然會重新爬蟲導致 -> StaleElementReferenceException: Message: stale element reference: stale element not found
            #    sleep(3)
                break
        driver.refresh()

def check_board( check_board_name = "Meeting Agenda" ) -> None:
    """_summary_
    請記得先登入帳號,這是用來檢查是否有創見board

    Args:
        check_board_name (str, optional): 要檢查的Board Name. Defaults to "Meeting Agenda".
    """
    try:
        collapsed_table = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-list > div > div > div > div.octo-sidebar-item.category.collapsed")))
        collapsed_table.click()
    except TimeoutException:
        #print("Table is already expanded")
        pass
    except NoSuchElementException:
        #print("Table is already expanded")
        pass
    created_board_list = driver.find_elements(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-list > div > div > div > div > div > div.octo-sidebar-title")
    for item in created_board_list:
        if item.text == check_board_name:
            print("The \""+check_board_name+"\" is checked")
            break
    else:
        print("The \""+check_board_name+"\" is not found")
        sys.exit(1)

def add_new_account(user_email:str, user_name:str, user_password:str ) -> None :
    """_summary_
    請記得先登入帳號,這個程式會先獲得可以Register的網址,之後再透過一個新的瀏覽器來這側該帳號
    Args:
        user_email (str): 要創建的電子郵件
        user_name (str): 要創建的使用者名稱
        user_password (str): 要創建的使用者密碼
    """
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-header > div.heading > div > div > div > div > div > span")))
    element.click()
    #driver.find_element(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-header > div.heading > div > div > div > div.Menu.noselect.bottom > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(4)").click()
    driver.find_element(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-header > div.heading > div > div > div > div.Menu.noselect.bottom > div > div:nth-child(1) > div:nth-child(1) > div[aria-label='Invite users']").click()
    driver.find_element(By.CSS_SELECTOR,"div#main > div > div.Workspace > div.Sidebar.octo-sidebar > div.octo-sidebar-header > div.heading > div > div > div.Modal.bottom-right > div.RegistrationLink > div:nth-child(2) > button").click()
        #啟動chrome
    driver_2 = webdriver.Chrome(service=service, options=options)
        #隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
    driver_2.implicitly_wait(10)

    print("get register URL =>"+clipboard.paste())
    driver_2.get(clipboard.paste())
    element = WebDriverWait(driver_2, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#login-email")))
    element.send_keys(user_email)
    driver_2.find_element(By.CSS_SELECTOR,"input#login-username").send_keys(user_name)
    driver_2.find_element(By.CSS_SELECTOR,"input#login-password").send_keys(user_password)
    driver_2.find_element(By.CSS_SELECTOR,"div#main > div > form > button > span").click()
    print("Register info:")
    print("\t E-mail:",user_email)
    print("\t user name:",user_name)
    print("\t user password:",user_password)
    try:
        register_error_message = driver_2.find_element(By.CSS_SELECTOR,"div#main > div > div.error").text
        print("Error, Register is not created")
        print(register_error_message)
    except NoSuchElementException:
        print("Register Created !!!")
    sleep(3)
    driver_2.close()
def delet_all_board() -> None:
    """_summary_
    請登入後,到一開始的畫面
    """
    driver.get(FOCALBOARD_IP)
    sleep(3)
    try:
        #element = driver.find_element(By.CSS_SELECTOR,"div#main > div > div > div.Sidebar.octo-sidebar > div.octo-sidebar-list > div > div > div > div:nth-child(2) > div.SidebarBoardItem.subitem.active > div:nth-child(3) > div > button > i")
        elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.categoryBoardsDroppableArea > div[data-rbd-draggable-context-id] > div[role=\"button\"]")))
        for element in elements:
            ActionChains(driver).move_to_element(element).perform()
            element.find_element(By.CSS_SELECTOR,"div > div > button > i").click()
            #滑鼠表單-刪除
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.Menu.noselect.auto.fixed > div > div > div > div[aria-label=\"Delete board\"]"))).click()
            #跳出詢問的刪除選單
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.dialog > div.container > div > button.Button.filled.danger.size--medium"))).click()
            sleep(3)
    except ElementNotInteractableException:
        pass
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass
    print("All Boards is deleted !!!")


if __name__ == "__main__":
    #檢查網頁是否連線正常
    response = requests.get(FOCALBOARD_IP, timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",FOCALBOARD_IP)
        sys.exit(1)

    #開啟網址
    driver.get(FOCALBOARD_IP)

    if not ALREADY_HAVE_FIRST_ACCOUNT_FLAG:
        #僅第一次設定帳戶有效
        creat_first_account()

    if ALREADY_HAVE_FIRST_ACCOUNT_FLAG:
        print("已經有創立帳號，再次登入")
        driver.get(FOCALBOARD_IP)
        #已經有創立帳號，再次登入:
        login_focalboard(ADMIN_USERNAME, ADMIN_PASSWORD)

    #網站轉跳太快
    sleep(3)
    #在以登入的狀態下，改變密碼
    change_password(ADMIN_PASSWORD,ADMIN_PASSWORD_2)
    #重新回到登入後的初始畫面，執行登出動作
    log_out()

    sleep(3) #切換太快
    #重新登入帳號
    driver.get(FOCALBOARD_IP)
    login_focalboard(ADMIN_USERNAME, ADMIN_PASSWORD_2)
    sleep(3) #切換太快
    #在以登入的狀態下，將密碼改回原本的
    change_password(ADMIN_PASSWORD_2, ADMIN_PASSWORD)
    sleep(3)
    #切換為原來的頁面
    driver.get(FOCALBOARD_IP)
    sleep(3)
    #在登入的狀態下，新增Board，並且檢查是否新增成功
    add_board("Meeting Agenda")

    #檢查是否有創見該Board，可能會有網址列縮排問題
    check_board("Meeting Agenda")
    #新增使用者(如果要測試新的使用者，可以直接在USER1_E_MAIL與USER1_NAME後面家字串，就可以直接創造新的使用者)
    add_new_account(USER1_E_MAIL, USER1_NAME, USER1_PASSWORD)
    #測試結束
    #刪除所有boards
    delet_all_board()
    sleep(10)
    driver.close()
    print("○●○●○●○●○●○●○●==>Test result PASS<==○●○●○●○●○●○●○●○●○●○●")
