'''
用來自動化加班填寫流程
'''
from time import sleep
import sys
import os
import configparser
from argparse import ArgumentParser
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
import datetime
import Connect_workovertime_Google_Sheet



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







#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
E_FLOW_ip = cf.get("APP_Info","E_FLOW_ip")
REASON_FOR_OVERTIME = cf.get("APP_Info","Reason_for_overtime")

#獲取使用者資料

def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="Clickhouse Example")
    parser.add_argument(
        "--reason",
        type=str,
        default=REASON_FOR_OVERTIME,
        metavar="AI(Project)(Reason)",
        help=f"Reason for overtime,Default:{REASON_FOR_OVERTIME}",
    )
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments


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
    #讀取輸入參數
    args = create_args()
    #啟動chrome
    driver = webdriver.Chrome(service=service, options=options)
    #隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
    driver.implicitly_wait(10)
    #檢查網頁是否連線正常
    response = requests.get(E_FLOW_ip, timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",E_FLOW_ip)
        sys.exit(1)

    #開啟網址
    driver.get(E_FLOW_ip)
    
    
    #登入
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#username")))
    driver.find_element(By.CSS_SELECTOR,"input#username").send_keys("帳號")
    driver.find_element(By.CSS_SELECTOR,"input#Password").send_keys("密碼")
    driver.find_element(By.CSS_SELECTOR,"button.btn.btn-default").click()
    sleep(3)
    #開始填寫今天資料
    #找尋找員工編號,並獲取員工編號
    get_employee_number = driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_Employee_No")
    get_employee_number_string = get_employee_number.get_attribute('value')
    #輸入員工編號
    get_employee_number = driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_EmpNo1").send_keys(get_employee_number_string)
    #輸入今天日期
    #print(datetime.date.today().strftime("%Y/%m/%d"))
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_ApplyDate1").send_keys(datetime.date.today().strftime("%Y/%m/%d"))
    
    #輸入起始與結束時間
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromApplyHour1").send_keys('18')
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromApplyMinute1").send_keys('0')
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_ToApplyHour1").send_keys("19")
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_ToApplyMinute1").send_keys("0")
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_RealApplyTotal1").send_keys("1")
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_Reason1").send_keys(args.reason)
    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_IsSupplyLeave1_No").click()

    #點選送出
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#ContentPlaceHolder1_UcSign1_btnSend"))).click()
    
    #上傳加班時間到對應的Google表單(我自己的紀錄表單)
    Connect_workovertime_Google_Sheet.update_work_overtime_date()
    
    #上傳加班表(主管自己建的)
    Connect_workovertime_Google_Sheet.update_workovertime_schedule()
    
    #倒數關閉
    print("即將關閉瀏覽器")
    for i in range(30):
        print(30-i-1,'s')
        sleep(1)
    driver.close()
