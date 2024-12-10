'''
用來自動化測試Rocket Chat
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
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import Select
import requests
import Auto_Update_Google_Sheet
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
EONKUBE_IP = cf.get("APP_Info","Eonkube_ip")
EONONE_IP = cf.get("APP_Info","Eonone_ip")
SUBJECT =  cf.get("APP_Info","Subject")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")






def string_to_ascii(get_string:str):
    """_summary_
    將帶入的字串,輸出成16進位表示
    Args:
        get_string (str): _description_
    """
    ascii_values = []
    for character in get_string:
        ascii_values.append(hex(ord(character)))
    print(ascii_values)

if __name__ == "__main__":
    #檢查網頁是否連線正常
    response = requests.get(EONKUBE_IP, timeout=10,verify=False)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",EONKUBE_IP)
        sys.exit(1)

    #開啟網址
    driver.get(EONKUBE_IP)
    
    #登入
    try:
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#username")))
    except TimeoutException:
        #從Active Directory切換到local user
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a#login-useLocal"))).click()
        
    driver.find_element(By.CSS_SELECTOR,"input#username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.CSS_SELECTOR,"input[type=\"password\"]").send_keys(ADMIN_PASSWORD)
    sleep(1)
    driver.find_element(By.CSS_SELECTOR,"button#submit").click()
    sleep(3)
    
    #切回到Node資訊的頁面
    driver.get(EONKUBE_IP)
    WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"table.sortable-table > tbody > tr.main-row")))
    #獲取Eonkube當前Node的資訊
    tables = driver.find_elements(By.CSS_SELECTOR,"table.sortable-table > tbody > tr.main-row")
    Eonkube_node_list = []
    Input_string = ""
    Eonkube_node_list.append("Eonkube DashBoard\n")
    for node_table in tables:
        node_status = node_table.find_element(By.CSS_SELECTOR,"td.col-badge-state-formatter").text
        #string_to_ascii(node_status)
        if(node_status == "Active"):
            node_name = node_table.find_element(By.CSS_SELECTOR,"td:nth-child(3)").text
            node_cpu = node_table.find_element(By.CSS_SELECTOR,"td:nth-child(8)").text
            node_ram = node_table.find_element(By.CSS_SELECTOR,"td:nth-child(9)").text
            node_gpu = node_table.find_element(By.CSS_SELECTOR,"td:nth-child(10)").text
            print(node_name)
            string_to_ascii(node_name)
            Eonkube_node_list.append(node_name)
            Eonkube_node_list.append(":\n")
            print(node_cpu)
            string_to_ascii(node_cpu)
            Eonkube_node_list.append("CPU: ")
            Eonkube_node_list.append(node_cpu)
            print(node_ram)
            string_to_ascii(node_ram)
            Eonkube_node_list.append(", Memory: ")
            Eonkube_node_list.append(node_ram)
            print(node_gpu)
            string_to_ascii(node_gpu)
            Eonkube_node_list.append(", GPU: ")
            Eonkube_node_list.append(node_gpu)
            Eonkube_node_list.append("\n\n")
            print("========================")
        else:
            node_name = node_table.find_element(By.CSS_SELECTOR,"td:nth-child(3)").text
            print(node_name,"is Error =>",node_status)
    
    #driver.close()
    #exit(0)
    #獲取Eonone當前Cluster的資訊
    #登入Eonone
    #Eonone_no_login_flag用來防止Eonone還在讀取時,就先輸入帳密的問題
    Eonone_no_login_flag = True
    Eonone_cluster_list = []
    driver.get(EONONE_IP)
    #WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input[name=\"j_password\"]")))
    while(Eonone_no_login_flag):
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[name=\"j_password\"]")))
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_username\"]").send_keys(ADMIN_USERNAME)
        driver.find_element(By.CSS_SELECTOR,"input[name=\"j_password\"]").send_keys(ADMIN_PASSWORD)
        sleep(1)
        driver.find_element(By.CSS_SELECTOR,"button.btn.btn-Login").click()
        sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR,"div.cutText[title=\"使用者名稱或密碼錯誤。\"]")
        except NoSuchElementException:
            Eonone_no_login_flag = False
    
    #Get info 
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.flex_center > div > div.capacity-body-content")))
    Eonone_cluster_list.append("EonOne Monitor\n")
    Cluster_info =driver.find_elements(By.CSS_SELECTOR,"div.flex_center > div > div.capacity-body-content")
    Cluster_cpu = Cluster_info[0].text
    Cluster_ram = Cluster_info[1].text
    print("Cluster CPU:", Cluster_cpu)
    Eonone_cluster_list.append("CPU:")
    Eonone_cluster_list.append(Cluster_cpu)
    Eonone_cluster_list.append(", ")
    print("Cluster RAM:", Cluster_ram)
    Eonone_cluster_list.append("Memory:")
    Eonone_cluster_list.append(Cluster_ram)
    Eonone_cluster_list.append("\n\n")

    #獲取韌體版本
    #點選詳細資料
    driver.find_element(By.CSS_SELECTOR,"div#sec1rightbox > div:nth-child(6) > ift-link-text > div > a").click()
    #選取韌體版本
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"tbody > ift-item-info-table-element:nth-child(4) > tr")))
    get_firmware_version = driver.find_elements(By.CSS_SELECTOR,"tbody > ift-item-info-table-element:nth-child(4) > tr > ift-item-info-table-item")
    get_firmware_version_string = ''
    print(get_firmware_version[0].text)
    if get_firmware_version[0].text == "韌體版本":
        print(get_firmware_version[1].text)
        get_firmware_version_string = get_firmware_version[1].text
    else:
        print("沒有找到韌體資訊")
        get_firmware_version_string = "沒有找到韌體資訊"
    
    #組合文字
    for element in Eonone_cluster_list:
        Input_string = Input_string + element
    for element in Eonkube_node_list:
        Input_string = Input_string + element
    
    print("即將上傳的資訊")
    print(get_firmware_version_string)
    print(Input_string)
    Auto_Update_Google_Sheet.update_experiment_data(get_firmware_version_string, Input_string)
    print("==================上傳完成====================")
    driver.quit()
    #driver.close()
    
