'''
用來自動化填寫加班資料
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
E_FLOW_ip = cf.get("APP_Info","E_FLOW_ip")
USER = cf.get("APP_Info","Admin_Username")
USER_PASSWORD = cf.get("APP_Info","Admin_Password")





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
    response = requests.get(E_FLOW_ip, timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",E_FLOW_ip)
        sys.exit(1)

    #開啟網址
    driver.get(E_FLOW_ip)


    #登入
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#username")))
    driver.find_element(By.CSS_SELECTOR,"input#username").send_keys(USER)
    driver.find_element(By.CSS_SELECTOR,"input#Password").send_keys(USER_PASSWORD)
    driver.find_element(By.CSS_SELECTOR,"button.btn.btn-default").click()
    sleep(10)

    #檢查有多少加班清單
    new_tab_num = 0
    overtime_check_list = driver.find_elements(By.CSS_SELECTOR,"table#ContentPlaceHolder1_gvToDoList > tbody > tr")
    for item in overtime_check_list:
        try:
            Subject = item.find_element(By.CSS_SELECTOR,"td.Subject")
            print("Subject =",Subject.text)
            #有加班申請有出現"Verification Sec. Ⅰ : Hank.Su Applys 加班申請單"
            if Subject.text =="Verification Sec. Ⅰ : Waiting.Lee Applys 加班申請單":
                print("Pass")
                new_tab_num =+ 1
                click_item = Subject.find_element(By.CSS_SELECTOR,"a")
                ActionChains(driver).key_down(Keys.CONTROL).click(click_item).perform()
        except NoSuchElementException as e:
            print("沒有找到相關元素")
            print(e.msg)
    #當前有len(driver.window_handles)個網頁
    while(len(driver.window_handles) != new_tab_num + 1):
        print("len(driver.window_handles=",len(driver.window_handles),"; new_tab_num=",new_tab_num)
        sleep(1)
    print("當前handle=",driver.current_window_handle)
    get_original_window_handle = driver.current_window_handle
    get_window_handle_num = len(driver.window_handles)
    if get_window_handle_num > 1:
        for i in range(get_window_handle_num):
            #print("當前handle=",driver.current_window_handle)
            print("所有handle=",driver.window_handles)
            #切換分頁
            driver.switch_to.window(driver.window_handles[get_window_handle_num-i-1])
            print("切換後,當前handle=",driver.current_window_handle)
            if get_original_window_handle != driver.window_handles[get_window_handle_num-i-1]:
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromActualHour1").send_keys('18')
                get_string = driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromActualHour1").get_property('value')
                #由於切換太快會導致第一個數值輸入不到所以加強檢查
                while(get_string != "18"):
                    driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromActualHour1").send_keys('18')
                    get_string = driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromActualHour1").get_property('value')
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_FromActualMinute1").send_keys('0')
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_ToActualHour1").send_keys("19")
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_ToActualMinute1").send_keys("0")
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_lunch1").send_keys("0")
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_dinner1").send_keys("0")
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_eatFreq1").send_keys("0")
                driver.find_element(By.CSS_SELECTOR,"input#ContentPlaceHolder1_ctlForm_eatFreq1").send_keys()
                WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#ContentPlaceHolder1_UcSign1_btnSend"))).click()
                print("即將關閉當前視窗")
                for i in range(30):
                    print(30-i-1,'s')
                    sleep(1)
                driver.close()
            print("i=",i)
    driver.close()
    print("○●○●○●○●○●○●○●==>加班填寫完成<==○●○●○●○●○●○●○●○●○●○●")
