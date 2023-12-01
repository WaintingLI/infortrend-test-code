'''
用來自動化測試Open Cart
'''
from time import sleep
import sys
import os
import re
import logging
import configparser
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup
import requests


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

def click_button(a):
    '''
    點擊按鈕
    
    Args:
     - a = WebDriver物件
    Example:
     click_button(driver.find_element(By.CSS_SELECTOR,"button#button-payment-methods"))
    '''
    element = a
    driver.execute_script("arguments[0].click();",element)

def creat_new_account(customer_first_name: str, customer_last_name: str, customer_e_mail: str, customer_password: str) -> None:
    '''
    註冊一個新的帳戶
    
    :Args:
     - Customer_First_Name  :輸入顧客(Customer)的First_Name
     - Customer_Last_Name   :輸入顧客(Customer)的Last_Name
     - Customer_E_Mail      :輸入顧客(Customer)的E-mail
     - Customer_Password    :輸入顧客(Customer)的Password
    '''
    #註冊一個新帳戶
    print("========================開始註冊新帳戶-START===========================")
    driver.get(OPENCART_IP+"en-gb?route=account/logout")
    driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[2]/div/a/span").click()
    driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[2]/div/ul/li[1]/a").click()
    #waiting_time(5)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[1]/div[1]/div/input").send_keys(customer_first_name)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[1]/div[2]/div/input").send_keys(customer_last_name)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[1]/div[3]/div/input").send_keys(customer_e_mail)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[2]/div/div/input").send_keys(customer_password)
    #點擊滑動開關，不能用上面的寫法，好像會誤判
    element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/div/div/input")
    driver.execute_script("arguments[0].click();",element)
    element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/div/button")
    driver.execute_script("arguments[0].click();",element)
    #註冊完新帳戶，會直接登入
    waiting_time(1)
    creat_account_respons_string = driver.find_element(By.CSS_SELECTOR,"div#alert").text
    if creat_account_respons_string=="":
        pass
    else:
        print(creat_account_respons_string)



    print("========================開始註冊新帳戶-END===========================")

def login_account(customer_e_mail: str, customer_password: str) -> None:
    '''
    使用E-mail與Password來登入帳戶
    
    :Args:
     - Customer_E_Mail      :輸入顧客(Customer)的E-mail
     - Customer_Password    :輸入顧客(Customer)的Password
    '''
    print("========================登入帳戶-START===========================")
    waiting_time(1)
    driver.get((OPENCART_IP+"en-gb?route=account/login"))
    #waiting_time(3)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,"input#input-email"))
        )
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div/form/div[1]/input").send_keys(customer_e_mail)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div/form/div[2]/input").send_keys(customer_password)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div/form/div[3]/button").click()
    #click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div/form/div[3]/button"))


    waiting_time(1)
    respons_string = driver.find_element(By.CSS_SELECTOR,"div#alert").text
    if respons_string == "":
        print("帳號=>",customer_e_mail,"成功登陸")
    else:
        print("有錯誤 =>",respons_string)
        sys.exit(1)
    #print("driver.find_element(By.CSS_SELECTOR,\"div#alert\").text",driver.find_element(By.CSS_SELECTOR,"div#alert").text)
    print("========================登入帳戶-END===========================")


def shopping_and_wish_list():
    '''
    自動購買與許願清單
    '''
    driver.get(OPENCART_IP)
    #waiting_time(5)
    print("========================購買與whish list-START===========================")
    driver.find_element(By.XPATH,"/html/body/main/div[1]/nav/div[2]/ul/li[6]/a").click()
    waiting_time(5)
    click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[1]/div/div[2]/form/div/button[1]"))
    click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[1]/div/div[2]/form/div/button[2]"))
    click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/button[1]"))
    click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/button[2]"))
    click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[3]/div/div[2]/form/div/button[1]"))
    click_button(driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[2]/div[3]/div/div[2]/form/div/button[2]"))
    print("========================購買與whish list-END===========================")

def check_whish_list():
    '''
    檢查whish list
    '''
    print("========================檢查whish list-START===========================")
    #driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/span").click()
    click_button(driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[3]/a/span"))
    #waiting_time(5)
    check_item_1 = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[1]/div/table/tbody/tr[1]/td[2]/a").text
    check_item_2 = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[2]/a").text
    check_item_3 = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div[1]/div/table/tbody/tr[3]/td[2]/a").text
    print("Check_Item_1 =",check_item_1)
    print("Check_Item_2 =",check_item_2)
    print("Check_Item_3 =",check_item_3)
    print(check_item(check_item_1))
    print(check_item(check_item_2))
    print(check_item(check_item_3))
    print("========================檢查whish list-END===========================")

def check_out() -> None :
    '''
    不管登入的帳號為誰，都會使用固定的地址來執行結帳動作
    '''
    print("========================結帳(Chekout)-START===========================")
    waiting_time(1)
    driver.get((OPENCART_IP+"en-gb?route=checkout/checkout"))
    #獲取所需要的列表
    try:
        driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[1]/div/fieldset/div[3]/form/div[1]/div[1]/input").send_keys(USER1_FIRST_NAME)
        driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[1]/div/fieldset/div[3]/form/div[1]/div[2]/input").send_keys(USER1_LAST_NAME)
        driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[1]/div/fieldset/div[3]/form/div[1]/div[4]/input").send_keys(ADDRESS)
        driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[1]/div/fieldset/div[3]/form/div[1]/div[6]/input").send_keys(CITY)
        driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[1]/div/fieldset/div[3]/form/div[1]/div[7]/input").send_keys(POST_CODE)
        print("Country")
        select = Select(driver.find_element(By.ID,"input-shipping-country"))

        # select by visible text
        select.select_by_visible_text('Taiwan')

        # select by value
        select.select_by_value('206')

        print("Region/State")
        #element = driver.find_element(By.ID,"input-shipping-zone")
        #driver.execute_script("arguments[0].scrollIntoView();", element)
        select2 = Select(driver.find_element(By.ID,"input-shipping-zone"))

        # select by visible text
        select2.select_by_visible_text('T\'ai-pei city')

        # select by value
        select2.select_by_value('3159')

        #點選Continue

        element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[1]/div/fieldset/div[3]/form/div[2]/button")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)
    except ElementNotInteractableException:
        #except Exception:
        print("已經有先設定地址，所以跳過新增地址的步驟，選用第一個地址")
        select3 = Select(driver.find_element(By.ID,"input-shipping-address"))

        # select by visible text
        select3.select_by_visible_text(select3.options[1].text)
        # select by value
        select3.select_by_value(select3.options[1].get_attribute("value"))

    #點選Shipping Method
    print("Shipping Method")
    #driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div[1]/fieldset/div[1]/button").click()
    element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div[1]/fieldset/div[1]/button")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)

    #driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/form/div[1]/input").click()


    #sleep(2)
    #driver.find_element(By.CSS_SELECTOR,"input#input-shipping-method-flat-flat").click()
    element = WebDriverWait(driver, 2).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR,"input#input-shipping-method-flat-flat"))
    )
    driver.find_element(By.CSS_SELECTOR,"input#input-shipping-method-flat-flat").click()



    driver.find_element(By.CSS_SELECTOR,"button#button-shipping-method").click()
    #driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/form/div[2]/button").click()
    #driver.find_element(By.XPATH,"/html/body[@class='modal-open']/div[@id='modal-shipping']/div[@class='modal-dialog modal-dialog-centered']/div[@class='modal-content']/div[@class='modal-body']/form[@id='form-shipping-method']/div[@class='text-end']/button[@id='button-shipping-method']").click()
    #點選Payment Method
    print("Payment Method")
    #網頁響應沒有那麼快
    waiting_time(2)
    #driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div[2]/fieldset/div[1]/button").click()
    #driver.find_element(By.CSS_SELECTOR,"button#button-payment-methods").click()
    click_button(driver.find_element(By.CSS_SELECTOR,"button#button-payment-methods"))
    element = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"input#input-shipping-method-flat-flat"))
            )
    driver.find_element(By.CSS_SELECTOR,"input#input-payment-method-cod-cod").click()
    driver.find_element(By.CSS_SELECTOR,"button#button-payment-method").click()
    #點擊Comfirm Order
    print("點擊Comfirm Order")
    element = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"button#button-confirm"))
            )
    element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/div/div[2]/div[3]/div[2]/div/button")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)
    print("========================結帳(Chekout)-END===========================")

def administration_operation_login() -> None:
    '''
    用來登入Admin頁面
    '''
    print("*******************Administration_Operation_Login-START*********************")
    waiting_time(1)
    driver.get(OPENCART_IP+"administration")
    #登入Administration帳號密碼
    driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/div[1]/div/input").send_keys(ADMIN_USERNAME)
    driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/div[2]/form/div[2]/div/input").send_keys(ADMIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR,"form#form-login > div.text-end > button").click()
    print("*******************Administration_Operation_Login-END*********************")

def administration_operation_check_order(first_name: str, last_name: str) -> None :
    '''
    ※請先登入Administration頁面
    用來在Administration頁面下,用來檢查是否有該位顧客的訂單
    
    :Args:
     - First_Name:輸入First Name
     - Last_Name:輸入Last Name
    '''
    print("*******************Administration_Operation_Check_Order-START*********************")
    #選取Sales
    driver.find_element(By.CSS_SELECTOR,"li#menu-sale").click()
    driver.find_element(By.CSS_SELECTOR,"ul#collapse-4 > li:nth-child(1) > a").click()

    #選取Sales中的表格
    #sales_tables = driver.find_elements(By.CSS_SELECTOR,"form#form-order > div.table-responsive > table > tbody")
    try:
        sales_tables = driver.find_elements(By.CSS_SELECTOR,"form#form-order > div.table-responsive > table > tbody > tr")
        for item in sales_tables:
            if(first_name+" "+last_name)==item.find_elements(By.TAG_NAME,"td")[3].text:
                print("確認有",item.find_elements(By.TAG_NAME,"td")[3].text,"的訂單")
                break
        else:
            print("找不到訂單")
    except IndexError:
        print("沒有找到任何Order")
    #關閉Sale
    driver.find_element(By.CSS_SELECTOR,"li#menu-sale > a").click()
    print("*******************Administration_Operation_Check_Order-END*********************")

def administration_operation_check_customer(customer_email: str) -> None:
    '''
    ※請先登入Administration頁面
    用來在Administration頁面下,用來檢查是否有該位顧客
    
    :Args:
     - Customer_Email:輸入顧客(Customer)的 E-mail
    '''
    print("*******************Administration_Operation_Check_Customer-START*********************")
    #選取Customers
    driver.find_element(By.CSS_SELECTOR,"li#menu-customer").click()
    driver.find_element(By.CSS_SELECTOR,"ul#collapse-5 > li:nth-child(1) > a").click()

    #讀取Customer表格
    try:
        customer_tables = driver.find_elements(By.CSS_SELECTOR,"form#form-customer > div.table-responsive > table > tbody > tr")
        for item in customer_tables:
            #print(item.text,"=====",item.find_elements(By.TAG_NAME,"td")[2].text)
            if customer_email==item.find_elements(By.TAG_NAME,"td")[2].text:
                print("確認Customer=>",item.find_elements(By.TAG_NAME,"td")[2].text,"是存在")
                break
        else:
            print("找不到Customer =>",customer_email)
    except IndexError:
        print("沒有找到任何Customer")
    #關閉Cutomer Menu
    driver.find_element(By.CSS_SELECTOR,"li#menu-customer > a").click()
    print("*******************Administration_Operation_Check_Customer-END*********************")


def administration_operation_add_customer(customer_first_name: str, customer_last_name: str, customer_e_mail: str, customer_password: str) -> None:
    '''
    ※請先登入Administration頁面
    用來在Administration頁面下,新增顧客
    
    :Args:
     - Customer_First_Name  :輸入顧客(Customer)的First_Name
     - Customer_Last_Name   :輸入顧客(Customer)的Last_Name
     - Customer_E_Mail      :輸入顧客(Customer)的E-mail
     - Customer_Password    :輸入顧客(Customer)的Password
    '''
    print("*******************Administration_Operation_Add_Customer-START*********************")
    #選取Customers
    driver.find_element(By.CSS_SELECTOR,"li#menu-customer").click()
    driver.find_element(By.CSS_SELECTOR,"ul#collapse-5 > li:nth-child(1) > a").click()
    #新增新的顧客Customer
    driver.find_element(By.CSS_SELECTOR,"div#content > div.page-header > div > div > a").click()

    #開始新增
    driver.find_element(By.CSS_SELECTOR,"input#input-firstname").send_keys(customer_first_name)
    driver.find_element(By.CSS_SELECTOR,"input#input-lastname").send_keys(customer_last_name)
    driver.find_element(By.CSS_SELECTOR,"input#input-email").send_keys(customer_e_mail)
    driver.find_element(By.CSS_SELECTOR,"input#input-password").send_keys(customer_password)
    driver.find_element(By.CSS_SELECTOR,"input#input-confirm").send_keys(customer_password)
    driver.find_element(By.CSS_SELECTOR,"div#content > div.page-header > div > div > button").click()

    #檢查是否會重複新增帳戶
    waiting_time(1)
    admin_creat_account_respons_string = driver.find_element(By.CSS_SELECTOR,"div#alert").text
    if admin_creat_account_respons_string=="Success: You have modified customers!":
        pass
    else:
        print(admin_creat_account_respons_string)
    #關閉Customer Menu
    driver.find_element(By.CSS_SELECTOR,"li#menu-customer > a").click()
    print("*******************Administration_Operation_Add_Customer-END*********************")


if __name__ == "__main__":
    #開啟網址
    driver.get(OPENCART_IP)
    creat_new_account(USER1_FIRST_NAME, USER1_LAST_NAME, USER1_E_MAIL,USER1_PASSWORD)
    login_account(USER1_E_MAIL, USER1_PASSWORD)
    shopping_and_wish_list()
    check_whish_list()
    check_out()

    #administration頁面操作
    administration_operation_login()
    administration_operation_check_order(USER1_FIRST_NAME, USER1_LAST_NAME)
    administration_operation_check_customer(USER1_E_MAIL)
    administration_operation_add_customer(USER2_FIRST_NAME, USER2_LAST_NAME, USER2_E_MAIL, USER2_PASSWORD)
    
    #進行第二位USER2來購買與結帳
    login_account(USER2_E_MAIL, USER2_PASSWORD)
    shopping_and_wish_list()
    check_whish_list()
    check_out()
    
    #administration頁面操作
    administration_operation_login()
    administration_operation_check_order(USER2_FIRST_NAME, USER2_LAST_NAME)


    sleep(5)
    driver.close()
    print("○●○●○●○●○●○●○●==>測試結果 PASS<==○●○●○●○●○●○●○●○●○●○●")

