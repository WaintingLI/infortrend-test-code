'''
用來自動化架設Datahub
'''
from time import sleep
import sys
import os
import configparser
from argparse import ArgumentParser
from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException




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
BINARY_LOCATION ='C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chrome-win64/chrome.exe'
options.binary_location=BINARY_LOCATION
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chromedriver-win64/chromedriver.exe")




#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
DATAHUB_IP = cf.get("APP_Info","Datahub_ip")
USERNAME = cf.get("APP_Info","Username")
PASSWORD = cf.get("APP_Info","Password")

#獲取PostgreSQL
POSTGRESQL_IP_PORT = cf.get("PostgreSQL_Info","PostgreSQL_IP_PORT")
POSTGRESQL_USERNAME = cf.get("PostgreSQL_Info","Username")
POSTGRESQL_PWD = cf.get("PostgreSQL_Info","Password")
POSTGRESQL_DATABASE = cf.get("PostgreSQL_Info","Database")



def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="Datahub Example")
    parser.add_argument(
        "--ip",
        type=str,
        default="Default",
        metavar="172.24.128.215",
        help="input ipv4",
    )
    parser.add_argument(
        "--port",
        type=str,
        default="Default",
        metavar="9002",
        help="input ip port",
    )
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments




if __name__ == "__main__":
    args = create_args()
    if args.ip != "Default" and args.port != "Default":
        DATAHUB_IP = "http://" + args.ip + ":" + args.port
    elif args.ip != "Default":
        DATAHUB_IP = "http://" + args.ip + ":" + DATAHUB_IP.split(":")[2]
    elif args.port != "Default":
        DATAHUB_IP = DATAHUB_IP.split(":")[0] + DATAHUB_IP.split(":")[1] + ":" + args.port


    #啟動chrome
    driver = webdriver.Chrome(service=service, options=options)
    #隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
    driver.implicitly_wait(10)

    #開啟網址
    driver.get(DATAHUB_IP)
    #登入
    driver.find_element(By.CSS_SELECTOR,"input#username").send_keys(USERNAME)
    driver.find_element(By.CSS_SELECTOR,"input#password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR,"button.ant-btn.ant-btn-primary").click()
    sleep(3)
    #close popup message
    try:
        driver.find_element(By.CSS_SELECTOR,"button[aria-label=\"Close\"]").click()
    except NoSuchElementException:
        pass
    get_button_list = driver.find_elements(By.CSS_SELECTOR,"button > span")
    for item in get_button_list:
        #print(item.text)
        if item.text == "Ingestion":
            try:
                item.click()
            except ElementClickInterceptedException:
                driver.find_element(By.CSS_SELECTOR,"button[aria-label=\"Close\"]").click()
                item.click()
            break
    #close popup message
    #try:
    #    driver.find_element(By.CSS_SELECTOR,"button[aria-label=\"Close\"]").click()
    #except NoSuchElementException:
    #    pass
    get_button_list = driver.find_elements(By.CSS_SELECTOR,"button > span")
    for item in get_button_list:
        #print(item.text)
        if item.text == "Create new source":
            try:
                item.click()
            except ElementClickInterceptedException:
                driver.find_element(By.CSS_SELECTOR,"button[aria-label=\"Close\"]").click()
                item.click()
            break
    try:
        driver.find_element(By.CSS_SELECTOR,"span > input[placeholder=\"Search data sources...\"]").send_keys("Postgre")
    except ElementNotInteractableException:
        driver.find_element(By.CSS_SELECTOR,"button[aria-label=\"Close\"]").click()
        driver.find_element(By.CSS_SELECTOR,"span > input[placeholder=\"Search data sources...\"]").send_keys("Postgre")

    #點選PostgreSQL
    check_flag = False
    while not check_flag:
        get_button_list = driver.find_elements(By.CSS_SELECTOR,"div > button > div")
        for item in get_button_list:
            #print(item.text)
            if item.text == "Postgres":
                item.click()
                check_flag = True
                break
        else:
            print("Not click PostgreSQL")

    #點選Settings
    get_button_list = driver.find_elements(By.CSS_SELECTOR,"div.ant-collapse-item")
    for item in get_button_list:
        #print(item.text)
        if item.text == "Settings":
            item.click()
            break
    #開始設定
    driver.find_element(By.CSS_SELECTOR,"input#host_port").send_keys(POSTGRESQL_IP_PORT)
    driver.find_element(By.CSS_SELECTOR,"input#username").send_keys(POSTGRESQL_USERNAME)
    driver.find_element(By.CSS_SELECTOR,"input#database").send_keys(POSTGRESQL_DATABASE)
    driver.find_element(By.CSS_SELECTOR,"input#password").send_keys(POSTGRESQL_PWD)
    driver.find_element(By.CSS_SELECTOR,"input[id=\"column_profiling.enabled\"]").click()
    #點選Next
    get_button_list = driver.find_elements(By.CSS_SELECTOR,"button.sc-dIsUp")
    for item in get_button_list:
        #print(item.text)
        if item.text == "Next":
            item.click()
    #點選Next
    get_button_list = driver.find_elements(By.CSS_SELECTOR,"button.sc-dIsUp")
    for item in get_button_list:
        #print(item.text)
        if item.text == "Next":
            item.click()
    #sleep(3)
    #selenium.common.exceptions.InvalidSelectorException: Message: invalid selector
    driver.find_element(By.CSS_SELECTOR,"input[placeholder=\"My Redshift Source #2\"]").send_keys("test")
    get_button_list = driver.find_elements(By.CSS_SELECTOR,"button.sc-dIsUp")
    for item in get_button_list:
        #print(item.text)
        if item.text == "Save & Run":
            item.click()
    driver.close()
    print("○●○●○●○●○●○●○●==>Setting Over<==○●○●○●○●○●○●○●○●○●○●")
