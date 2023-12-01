'''
用來新增Open Cart 的 Customer 帳戶
'''
from time import sleep
import sys
import os
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
#import configparser
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import Select
#from selenium.common.exceptions import ElementNotInteractableException

#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地，如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#設定Chrome driver 的相關屬性
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument("--disable-gpu")
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
#隱式等待,如果沒有找到元素.每0.5秒重新找一次，直到10秒過後
driver.implicitly_wait(10)

def create_args() -> None:
    '''
    用來接收外部參數的指令
    
    arugment:
     -host  : Open Cart ip address
     -fn    : First Name of customer account
     -ln    : Last_Name of customer account
     -em    : E_Mail of customer account
     -pwd   : password of customer account
     Example:
     
    '''
    parser = ArgumentParser(description="Open Cart ip example: \
                                        open_cart_creat_customer_account.py \
                                        -host http://opencart-test.k8s.local/ \
                                        -fn test \
                                        -ln test \
                                        -em test@example.com \
                                        -pwd ADMIN1234567 \
                                        ")
    parser.add_argument(
        "-host",
        default='http://opencart-test.k8s.local/',
        metavar='host',
        dest="host",
        help="Open Cart ip address (default: \"http://opencart-test.k8s.local/\")",)

    parser.add_argument(
        "-fn",
        default='test',
        metavar='first_name',
        dest="first_name",
        help="First Name of customer account (default: \"test\")",)

    parser.add_argument(
        "-ln",
        default='test',
        metavar='last_name',
        dest="last_name",
        help="Last_Name of customer account (default: \"test\")",)

    parser.add_argument(
        "-em",
        default='test@example.com',
        metavar='e_mail',
        dest="e_mail",
        help="E_Mail of customer account (default: \"test@example.com\")",)

    parser.add_argument(
        "-pwd",
        default='ADMIN1234567',
        metavar='password',
        dest="password",
        help="password of customer account (default: \"ADMIN1234567\")",)

    #parser.add_argument(
    #    "-p",
    #    type=int,
    #    default=5672,
    #    metavar='port',
    #    dest="port",
    #    help="RabbitMQ sender port number (default: \"5672\")",)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    costumer_args = create_args()

    #檢查網頁是否連線正常
    response = requests.get((costumer_args.host+"en-gb?route=account/logout") , timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",costumer_args.host)
        print("請確認連線的網站是否為Open Cart")
        sys.exit(1)
    driver.get(costumer_args.host+"en-gb?route=account/logout")
    driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[2]/div/a/span").click()
    driver.find_element(By.XPATH,"/html/body/nav/div/div[2]/ul/li[2]/div/ul/li[1]/a").click()
    #waiting_time(5)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[1]/div[1]/div/input").send_keys(costumer_args.first_name)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[1]/div[2]/div/input").send_keys(costumer_args.last_name)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[1]/div[3]/div/input").send_keys(costumer_args.e_mail)
    driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/fieldset[2]/div/div/input").send_keys(costumer_args.password)
    #點擊滑動開關，不能用上面的寫法，好像會誤判
    element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/div/div/input")
    driver.execute_script("arguments[0].click();",element)
    element = driver.find_element(By.XPATH,"/html/body/main/div[2]/div/div/form/div/button")
    driver.execute_script("arguments[0].click();",element)
    #註冊完新帳戶，會直接登入
    sleep(1)
    creat_account_respons_string = driver.find_element(By.CSS_SELECTOR,"div#alert").text
    if creat_account_respons_string=="":
        print("Register Success !!!")
    else:
        print("Register Fail")
        print(creat_account_respons_string)
    driver.close()
