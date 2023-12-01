'''
用來自動化測試Jira Software
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
JIRASOFWARE_IP = cf.get("APP_Info","JiraSoftware_ip")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
ADMIN_EMAIL = cf.get("APP_Info","Admin_E-Mail")
#獲取專案的名稱與設定
PROJECT_NAME = cf.get("Project","Project_Name")
PROJECT_KEY = cf.get("Project","Project_Key")


def login_jira(username:str, password:str) -> None:
    """_summary_

    Args:
        username (str): 登入的admin帳號
        password (str): 登入的admin密碼
    """
    print("登入資訊: \n"+"帳號:"+username+"\n"+"密碼:"+password)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input#login-form-username"))).send_keys(username)
    #driver.find_element(By.CSS_SELECTOR,"input#login-form-username").send_keys(ADMIN_USERNAME)
    driver.find_element(By.CSS_SELECTOR,"input#login-form-password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR,"input#login").click()

def creating_project(project_name:str, project_key:str) -> None:
    """_summary_

    Args:
        project_name (str): 要輸入的Project Name
        project_key (str): 要輸入的Project Key
    """
    global PROJECT_KEY
    #第一次創建Project
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button#emptyProject"))).click()
    
    except TimeoutException:
        #第一次創建Project後
        try:
            #已經有創造一個Project以上的做法
            driver.get(JIRASOFWARE_IP+"secure/BrowseProjects.jspa?selectedCategory=all&selectedProjectType=software")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a#browse-projects-create-project"))).click()
        except TimeoutException:
            #沒有創造任一個Project的作法
            driver.get(JIRASOFWARE_IP+"secure/BrowseProjects.jspa?selectedCategory=all&selectedProjectType=software")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#content > div > p:nth-child(4) > a"))).click()
    #跳出視窗
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#project-template-group-software > div.pt-templates-list > fieldset > div > div.template.selected"))).click()
    driver.find_element(By.CSS_SELECTOR,"div#add-project-dialog > div:nth-child(3) > div.dialog-button-panel > button").click()
    
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div#add-project-dialog > div:nth-child(4) > div.dialog-button-panel > button.template-info-dialog-create-button.pt-submit-button.aui-button.aui-button-primary"))).click()
    
    driver.find_element(By.CSS_SELECTOR,"input#name").send_keys(project_name)
    element_project_key = driver.find_element(By.CSS_SELECTOR,"input#key")
    element_project_key.send_keys(project_key)
    #實際抓到的Project Key
    hold_project_key = element_project_key.get_attribute("value")
    
    sleep(3)
    driver.find_element(By.CSS_SELECTOR,"div#add-project-dialog > div:nth-child(5) > div.dialog-button-panel > button.add-project-dialog-create-button.pt-submit-button.aui-button.aui-button-primary").click()
    try:
        try:
            check_error_message = driver.find_element(By.CSS_SELECTOR,"form#add-project-form > fieldset > div:nth-child(2) > div.error").text
            if check_error_message:
                print("check_error_message =>" + check_error_message)
        except NoSuchElementException:
            pass
        
        try:
            check_error_message = driver.find_element(By.CSS_SELECTOR,"form#add-project-form > fieldset > div:nth-child(3) > div.error").text
            if check_error_message:
                print("check_error_message =>" + check_error_message)
        except NoSuchElementException:
            pass
        #等待網頁變化
        sleep(2)
        #Cancel取消新增此Project
        driver.find_element(By.CSS_SELECTOR,"div#add-project-dialog > div:nth-child(5) > div.dialog-button-panel > a").click()
    except NoSuchElementException:
        print("Create Project Successfully !!!")
        #專案創造成功，所以需要更換當前的Project Key
        cf.set("Project", "Project_Key", hold_project_key)
        f = open('config.ini', 'w', encoding='UTF-8')
        cf.write(f)
        f.close()
        PROJECT_KEY = hold_project_key

def creating_issue(issue_summary:str) -> None:
    """_summary_
    自動創造issue
    Args:
        issue_summary (str): 輸入要創造的Issue summary
    """
    #在登入且也有創見Project情況下，去 Ceate Issue
    driver.get(JIRASOFWARE_IP+"secure/CreateIssue!default.jspa")
    #driver.find_element(By.CSS_SELECTOR,"input#issue-create-submit").click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#issue-create-submit"))).click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#summary"))).send_keys(issue_summary)
    handles = driver.window_handles
    iframe = driver.find_elements(By.TAG_NAME,'iframe')[0]
    driver.switch_to.frame(iframe)
    
    element = driver.find_element(By.CSS_SELECTOR,"body#tinymce > p")
    element.send_keys("test1234567")
    #sleep(3)
    #print("切換回來")
    driver.switch_to.window(handles[0])
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#issue-create-submit"))).click()
    #driver.find_element(By.CSS_SELECTOR,"input#issue-create-submit")

def check_issue(summary_text:str) -> None:
    """_summary_
    用來檢查issue是否有被創造
    Args:
        summary_text (str): 輸入要檢查Issue的Summary
    """
    #快速登入Board進入
    driver.get(JIRASOFWARE_IP+"secure/RapidBoard.jspa?projectKey="+PROJECT_KEY+"&view=planning.nodetail&issueLimit=100")
    board_logs = driver.find_elements(By.CSS_SELECTOR,"div#ghx-content-group > div.ghx-backlog-group > div.ghx-backlog-container.ghx-open.ghx-everything-else.ui-droppable > div.ghx-issues.js-issue-list.ghx-has-issues > div > div.ghx-issue-content > div > div.ghx-summary > span")
    for item in board_logs:
        if item.text == summary_text:
            print("found Issue Summary =>"+item.text)
            break
    else:
        print("No found Issue \""+summary_text+"\"")
        print("check issue Fail")
        sys.exit(1)

if __name__ == "__main__":
    #檢查網頁是否連線正常
    response = requests.get(JIRASOFWARE_IP, timeout=10)
    if response.status_code != 200:
        print("網路異常, 網路status_code = ",response.status_code,"連線網址 =",JIRASOFWARE_IP)
        sys.exit(1)

    #開啟網址
    driver.get(JIRASOFWARE_IP)

    #登入網頁
    login_jira(ADMIN_USERNAME, ADMIN_PASSWORD)
    #等網頁登入完成
    sleep(1)
    #創建Project
    creating_project(PROJECT_NAME, PROJECT_KEY)
    #sleep(600)
    #已經創建Project後-要Creat Issue
    random_list_number = random.choices("0123456789ABCDEF", k=16)
    SUMMARY = ''.join(random_list_number)
    creating_issue(SUMMARY)
    #已經創建Project後-檢查Creat Issue
    sleep(3) #等待Issue創造延遲
    check_issue(SUMMARY)

    sleep(10)
    driver.close()
    print("○●○●○●○●○●○●○●==>Test result PASS<==○●○●○●○●○●○●○●○●○●○●")
