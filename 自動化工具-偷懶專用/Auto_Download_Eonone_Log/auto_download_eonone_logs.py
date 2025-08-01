'''
用來自動化下載Logs程序
'''
from time import sleep
import sys
import os
import configparser
import shutil
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select




#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))
#獲取當前所在目錄
TMP_STORE_PATH = "test_download"
DOWNLOAD_DIR = os.getcwd() + "\\" + TMP_STORE_PATH
GET_NODE_NAME = ""
#暫時儲存的位置
if not os.path.exists(TMP_STORE_PATH):
    os.makedirs(TMP_STORE_PATH)
#os.makedirs("test_download/test")
#print(os.listdir("./"+TMP_STORE_PATH))
file_list = os.listdir(TMP_STORE_PATH)
if file_list:
    print("請清空 =>",TMP_STORE_PATH,"<=底下的資料")
    sys.exit(0)
#for file_item in file_list:
    #shutil.copyfile("./test_download/"+file_item,"./test_copy/"+file_item)
    #print(os.path.basename("./test_download/"+file_item).rfind(".crdownload"))
#會刪除整個資料夾
#shutil.rmtree("./test_copy/")


#設定Chrome driver 的相關屬性
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('disable-application-cache')
#最大化窗口
options.add_argument('--start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
BINARY_LOCATION='C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chrome-win64/chrome.exe'
options.binary_location=BINARY_LOCATION
service = Service(executable_path="C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chromedriver-win64/chromedriver.exe")
#下載位置
options.add_experimental_option('prefs', {
    'download.default_directory': DOWNLOAD_DIR,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': False
})
#options.add_experimental_option('prefs', {'download.default_directory': 'C:/Users/waiting.lee/Desktop/Auto Tools/Auto_Download_Eonone_Log/test_download'})

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
EONONE_IP = cf.get("Cluster_Info","Eonone_ip")
ADMIN_USERNAME = cf.get("Cluster_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("Cluster_Info","Admin_Password")

#取消特定網頁的不安全下載封鎖
options.add_argument("--unsafely-treat-insecure-origin-as-secure="+EONONE_IP)

#啟動chrome
driver = webdriver.Chrome(service=service, options=options)
#隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
driver.implicitly_wait(10)


if __name__ == "__main__":
    #登入
    driver.get(EONONE_IP)
    #WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[name=\"j_password\"]")))
    while True:
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[name=\"j_password\"]")))
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_username\"]").send_keys(Keys.CONTROL+"a")
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_username\"]").send_keys(Keys.DELETE)
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_username\"]").send_keys(ADMIN_USERNAME)
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_password\"]").send_keys(Keys.CONTROL+"a")
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_password\"]").send_keys(Keys.DELETE)
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_password\"]").send_keys(ADMIN_PASSWORD)
        sleep(1)
        try:
            driver.find_element(By.CSS_SELECTOR,"button.btn.btn-Login").click()
        except ElementClickInterceptedException:
            #因為網頁更新太慢導致元件還沒好所造成的問題
            continue
        sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR,"div.cutText[title=\"使用者名稱或密碼錯誤。\"]")
        except NoSuchElementException:
            break

    #點選Node
    driver.find_element(By.CSS_SELECTOR,"div[ctagname=\"nodes\"] > p.ng-star-inserted > span").click()
    #點選完後,會看到Node
    node_list = driver.find_elements(By.CSS_SELECTOR,"div.listItem.ng-star-inserted")
    while not node_list:
        node_list = driver.find_elements(By.CSS_SELECTOR,"div.listItem.ng-star-inserted")
        print("Waiting Node List")
        sleep(1)
    for item in node_list:
        #獲取當前Node名稱
        ##div.listItem.ng-star-inserted> div.flex_leftTop.ng-star-inserted > div.flexItem > div:nth-child(1)
        #item.find_element(By.CSS_SELECTOR,"div.flex_leftTop.ng-star-inserted > div.flexItem > div:nth-child(1)")
        GET_NODE_NAME = item.find_element(By.CSS_SELECTOR,"div > div.flexItem > div:nth-child(1) > div").text
        print("Node Name:",GET_NODE_NAME)
        #檢查是否有該名稱的資料夾路徑
        if not os.path.exists(TMP_STORE_PATH + "/" + GET_NODE_NAME):
            os.makedirs(TMP_STORE_PATH + "/" + GET_NODE_NAME)
        item.click()
        item.find_element(By.CSS_SELECTOR,"div > div > div:nth-child(3) > ift-dropdown-button > div > button").click()
        element = "div.locRalative.open > ul.dropdown-menu.dropdown-menu-right > li:nth-child(4)"
        #WebDriverWait(driver,int(10)).until(EC.visibility_of_element_located((By.CSS_SELECTOR,element)))
        #driver.execute_script("arguments[0].scrollIntoView();", element)
        get_location = driver.find_element(By.CSS_SELECTOR,element).location_once_scrolled_into_view
        while True:
            try:
                click_item = driver.find_element(By.CSS_SELECTOR,element)
                ActionChains(driver).move_to_element(click_item).perform()
                #driver.find_element(By.CSS_SELECTOR,element).click()
                click_item.click()
                break
            except ElementNotInteractableException:
                print("不可以點")
            except ElementClickInterceptedException:
                print("有異物")
                
                
        #item.find_element(By.CSS_SELECTOR,"button").click()
        #跳出診斷頁面
        list_diagnost = driver.find_elements(By.CSS_SELECTOR,"div#csNodeDiagnostic > ift-dialog-content > mat-dialog-content > div > ift-layer-section > div > div:nth-child(3) > ift-layer-block > div > div > ift-layer-basic")
        for i,item_2 in enumerate(list_diagnost):
            #print("i=",i)
            OUT_DIR = ""
            if i == 0:
                if not os.path.exists(TMP_STORE_PATH + "/" + GET_NODE_NAME + "/" + "DiagnosticLog"):
                    os.makedirs(TMP_STORE_PATH + "/" + GET_NODE_NAME + "/" + "DiagnosticLog")
                    OUT_DIR = "DiagnosticLog"
            elif i == 1:
                if not os.path.exists(TMP_STORE_PATH + "/" + GET_NODE_NAME + "/" + "NodeCoreDump"):
                    os.makedirs(TMP_STORE_PATH + "/" + GET_NODE_NAME + "/" + "NodeCoreDump")
                    OUT_DIR = "NodeCoreDump"
            print("Creating =>", OUT_DIR, " <= Data!!!")
            item_2.find_element(By.CSS_SELECTOR,"div > button").click()
            #當下在完成後,會跳出資訊"操作完成"的訊息
            while True:
                try:
                    driver.find_element(By.CSS_SELECTOR,"div#infodialog > ift-dialog-footer-default > footer > ift-primary-solid-button > div > button").click()
                    break
                except NoSuchElementException:
                    print("Waiting for Finish...")
                    try:
                        #跳出錯誤訊息
                        get_message = driver.find_element(By.CSS_SELECTOR,"div#errordialog > ift-dialog-content")
                        print(get_message.text)
                        print("**************************************")
                        print(GET_NODE_NAME," won't store ",OUT_DIR)
                        print("**************************************")
                        #關閉錯誤訊息
                        driver.find_element(By.CSS_SELECTOR,"div#errordialog > ift-dialog-footer-default > footer > ift-primary-solid-button > div > button").click()
                        #print("item=>",item)
                    except NoSuchElementException:
                        pass
                    sleep(5)
            file_list = os.listdir("./" + TMP_STORE_PATH)
            #檢查沒有.crdownload的暫存檔案,沒有才可以進行下一步
            while True:
                for file_name in file_list:
                    if file_name.rfind(".crdownload") >= 0 or file_name.rfind(".tmp") >= 0:
                        #print("Find .crdownload or .tmp File =",file_name)
                        sleep(1)
                        break
                else:
                    break
                file_list = os.listdir("./" + TMP_STORE_PATH)
            for file in file_list:
                BASE_PATH = TMP_STORE_PATH + "/"
                if os.path.isfile(BASE_PATH + file):
                    file_status = os.stat(BASE_PATH + file)
                    print("Find File =",file)
                    #Chrome會掃描檔案,等到掃描完在移動檔案
                    hold_st_atime = 0.0
                    hold_st_mtime = 0.0
                    hold_st_ctime = 0.0
                    check_counter = 100
                    while check_counter != 0:
                        if hold_st_atime != file_status.st_atime or \
                           hold_st_mtime != file_status.st_mtime or \
                           hold_st_ctime != file_status.st_ctime:
                            hold_st_atime = file_status.st_atime
                            hold_st_mtime = file_status.st_mtime
                            hold_st_ctime = file_status.st_ctime
                            sleep(1)
                            check_counter = 100
                            continue
                        file_status = os.stat(BASE_PATH + file)
                        check_counter = check_counter - 1
                    #print("os.stat =",
                    #    ";","st_atime=",file_status.st_atime,
                    #    ";","st_mtime",file_status.st_mtime,
                    #    ";","st_ctime",file_status.st_ctime
                    #    )
                    shutil.move(BASE_PATH + file, BASE_PATH + GET_NODE_NAME + "/" + OUT_DIR)

        #關閉診斷資訊
        ELEMENT_ITEM = "div#csNodeDiagnostic > ift-dialog-footer-default > footer > ift-primary-solid-button > div > button"
        driver.find_element(By.CSS_SELECTOR,ELEMENT_ITEM).click()
        sleep(10)
    COUNT_DOWN = 10
    for i in range(COUNT_DOWN):
        print(f"{COUNT_DOWN-i-1} s")
        sleep(1)
    driver.close()
