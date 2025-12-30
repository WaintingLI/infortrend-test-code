'''
用來自動化App安裝
'''
from argparse import ArgumentParser
from time import sleep
import sys
import os
import configparser
import csv
import random
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import requests
import string_2_ascii
import logging_config
import get_nodes_available_ip
import communicate_to_machine
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.common.exceptions import SessionNotCreatedException
#from selenium.webdriver.remote.webdriver import WebDriver
#from selenium.webdriver.remote.webdriver import WebElement

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
#options.add_argument("--headless")
#options.add_argument("--disable-gpu")
#options.add_argument('--no-sandbox')

#driver_location='/usr/bin/chromedriver'
#指令Chromedriver位置
BINARY_LOCATION ='C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chrome-win64/chrome.exe'
#BINARY_LOCATION = 'C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chrome-headless-shell-win64/chrome-headless-shell.exe'
options.binary_location=BINARY_LOCATION
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path=
    "C:/Users/waiting.lee/Desktop/Auto Tools/Chrom_driver_kits/chromedriver-win64/chromedriver.exe")







#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
RANCHER_ip = cf.get("Eonkube_Info","Rancher_ip")
ADMIN_USERNAME = cf.get("Eonkube_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("Eonkube_Info","Admin_Password")
DEFAULT_CHART = cf.get("Charts_Info","Default_chart",fallback="All")
CLUSTER_IP_START = cf.get("Cluster_Info","Avaible_IP_Start")
CLUSTER_IP_END = cf.get("Cluster_Info","Avaible_IP_End")


def export_csv_file(get_dict_data:dict) -> None:
    """將App資料以CSV方式儲存在本地位置
    欄位:['App Name', 'Service type', 'Name Space','IP']
    Args:
        get_dict_data (dict): 輸入含有['App Name', 'Service type', 'Name Space','IP']的dict
    """
    csv_name = "app_install_list.csv"
    csv_already_exit_flag = True
    if not os.path.isfile(csv_name):
        csv_already_exit_flag = False


    with open(csv_name, 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['App Name', 'Service type', 'Name Space','IP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not csv_already_exit_flag:
            writer.writeheader()
        writer.writerow(get_dict_data)



def install_from_chart_to_app_deploy(app_name:str="Airbyte",service_type:str="balancer",namespace:str="test-for-balancer") -> str | None:
    """
    從Eonkube安裝特定App
    Args:
        App_name (str, optional): App名稱,要跟Chart的App名稱一樣(大小寫英文字母要一樣). Defaults to "Airbyte".
        Service_type (str, optional): 用來分辨該App是使用哪一個Type,全部使用英文字母小寫(balancer、node、cluster). Defaults to "balancer".
        Namespace (str, optional): 要安裝的NameSpace,如果沒有找到對應的Name Space會自行創建. Defaults to "test-for-balancer".
    Returns:
        str | None: 回傳App的安裝名稱
    """
    to_get_app_list = driver.find_elements(By.CSS_SELECTOR,"main > div > div > div.grid > div > h4.name")
    for app_item in to_get_app_list:
        logging_config.debug(app_item.text)
        if app_item.text == app_name:
            app_item.click()
            #點選Install按鈕
            WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"main > div > div.chart-header > div.name-logo-install > button")))
            driver.find_element(By.CSS_SELECTOR,"main > div > div.chart-header > div.name-logo-install > button").click()

            #點選NameSpace
            click_namespace_flag = True
            while click_namespace_flag:
                click_namespace_flag = False
                #driver.find_element(By.CSS_SELECTOR,"div#vs5__combobox > div.vs__actions").click()
                #namespace_button = driver.find_element(By.CSS_SELECTOR,"div#vs5__combobox > div.vs__actions")
                #namespace_button = driver.find_element(By.CSS_SELECTOR,"div[role=\"combobox\"] > div.vs__actions")
                namespace_button = driver.find_element(By.CSS_SELECTOR,"div[role=\"combobox\"] > div.vs__selected-options")
                driver.execute_script("$(arguments[0]).click()",namespace_button)

                #開啟NameSpace清單
                #vs__dropdown-menu vs__dropdown-up
                css_selector="ul.vs__dropdown-menu.vs__dropdown-up"
                try:
                    WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,css_selector)))
                except  TimeoutException:
                    try:
                        css_selector="ul.vs__dropdown-menu"
                        WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,css_selector)))
                    except TimeoutException:
                        click_namespace_flag =True
                        
            namespace_list = driver.find_elements(By.CSS_SELECTOR,css_selector + "> li")
            for app_item in namespace_list:
                logging_config.debug(app_item.text)
                if app_item.text == namespace:
                    ActionChains(driver).move_to_element(app_item).perform()
                    app_item.click()
                    break
            else:
                #點選Create a New Namespace
                create_a_new_namespace_button = namespace_list[0]
                driver.execute_script("$(arguments[0]).click()",create_a_new_namespace_button)
                driver.find_element(By.CSS_SELECTOR,"div.labeled > div > input[placeholder=\"Create a New Namespace\"]").send_keys(namespace)
            #填寫App名稱
            write_app_name = ""
            #將名稱都轉成小寫英文字母
            for character in app_name:
                if ord(character) < 90 and ord(character) >= 65:
                    write_app_name = write_app_name + chr(ord(character) + 32)
                elif (ord(character) <= 0x7A and ord(character) >= 0x61) or ord(character) == 0x2D:
                    write_app_name = write_app_name + character
            if service_type != "":
                write_app_name = write_app_name + "-" + service_type
            #移除空格(Space)
            #write_app_name = write_app_name.replace(" ","")
            driver.find_element(By.CSS_SELECTOR,"div.labeled > div > input[placeholder=\"A unique name\"]").send_keys(write_app_name)
            #點選Next
            driver.find_element(By.CSS_SELECTOR,"div#wizard-footer-controls > div > button > span").click()
            break
    else:
        logging_config.info("沒有找到App ==>"+ app_name)
        logging_config.info("字串對應的hex")
        string_2_ascii.string_to_hex(app_name)
        logging_config.info("=======App Not Found=======")
        return None
    return write_app_name

def create_pvc(select_name_space:str="test-for-balancer",app_pvc_name:str="test",pvc_storageclass:str="Default") -> str:
    """
    再所需的NS中創建PVC,並且回傳創建PVC的名字
    Args:
        select_name_space (str, optional): 選擇要創建PVC的所在Node. Defaults to "test-for-balancer".
        app_pvc_name (str, optional): 創建pvc的名稱. Defaults to "test".
        pvc_storageclass(str, optional): 設定pvc的Storage Class. Defaults to "Default(預設值)".

    Returns:
        str: 最終創建pvc的名稱
    """
    #自動新增PVC(新開分頁)
    #WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#__layout > div > div.dashboard-content.pin-bottom > nav > div.nav > div.accordion.package.depth-0.expanded.has-children > ul > li:nth-child(4) > a > span"))).click()
    #ActionChains(driver).key_down(Keys.CONTROL).click(click_item).perform()
    #獲取當前的Handle,並且切換到另外一個handle來處理PVC
    main_handle = driver.current_window_handle
    driver.execute_script("window.open('');")
    get_window_handle_num = len(driver.window_handles)
    return_pvc_name=""
    try_counter = 3
    while(return_pvc_name == "" and try_counter > 0):
        for number in range(get_window_handle_num):
            if driver.window_handles[get_window_handle_num-number-1] != main_handle:
                driver.switch_to.window(driver.window_handles[get_window_handle_num-number-1])
                driver.get(RANCHER_ip)
                select_control_ui(driver,"Advanced","Storage","PersistentVolumeClaims")
                #在PVC點選Create
                logging_config.debug("點選create")
                WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#__layout > div > div.dashboard-content.pin-bottom > main > div > header > div.actions-container > div > a"))).click()
                #driver.find_element(By.CSS_SELECTOR,"div#__layout > div > div.dashboard-content.pin-bottom > main > div > header > div.actions-container > div > a").click()
                get_pvc_namespace_name = driver.find_elements(By.CSS_SELECTOR,"form > div.resource-container.cru__content > div.row.mb-20 > div > div")
                #創建PVC旗標
                pvc_done_flage = False
                while not pvc_done_flage:
                    #選擇要在哪一個NameSpace建立
                    for namespace_item in get_pvc_namespace_name:
                        logging_config.info(namespace_item.find_element(By.CSS_SELECTOR,"div > label").text)
                        if namespace_item.find_element(By.CSS_SELECTOR,"div > label").text == "Namespace *":
                            namespace_item.find_element(By.CSS_SELECTOR,"div > div > div > div > input").click()
                            #獲取NameSpace清單
                            pvc_namespace_list = driver.find_elements(By.CSS_SELECTOR,"ul.vs__dropdown-menu > li")
                            for pvc_namespace in pvc_namespace_list:
                                logging_config.debug(pvc_namespace.text)
                                if pvc_namespace.text == select_name_space:
                                    pvc_namespace.click()
                                    #避開StaleElementReferenceException
                                    break
                            else:
                                #點選Create a New Namespace
                                create_a_new_namespace_button = pvc_namespace_list[0]
                                driver.execute_script("$(arguments[0]).click()",create_a_new_namespace_button)
                                driver.find_element(By.CSS_SELECTOR,"div.labeled > div > input[placeholder=\"Create a New Namespace\"]").send_keys(select_name_space)
                    #避開StaleElementReferenceException(創造Name Space會動到網頁)
                    get_pvc_namespace_name = driver.find_elements(By.CSS_SELECTOR,"form > div.resource-container.cru__content > div.row.mb-20 > div > div")
                    for namespace_item in get_pvc_namespace_name:
                        logging_config.info(namespace_item.find_element(By.CSS_SELECTOR,"div > label").text)
                        if namespace_item.find_element(By.CSS_SELECTOR,"label").text == "Name *":
                            namespace_item.find_element(By.CSS_SELECTOR,"div > input").send_keys(Keys.CONTROL+"a")
                            namespace_item.find_element(By.CSS_SELECTOR,"div > input").send_keys(Keys.DELETE)
                            #使用亂數來創造名字
                            string_nuber = 8
                            print_string = ""
                            get_str_list = random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',string_nuber)
                            for number in range(string_nuber):
                                print_string = print_string + get_str_list[number]
                            namespace_item.find_element(By.CSS_SELECTOR,"div > input").send_keys(app_pvc_name+"-"+print_string)
                            return_pvc_name = app_pvc_name+"-"+print_string

                    if pvc_storageclass != "Default":
                        #section#volumeclaim > div > div > div > div > div > div.labeled-select
                        driver.find_element(By.CSS_SELECTOR,"section#volumeclaim > div > div > div > div > div > div.labeled-select").click()
                        #ul[role="listbox"] > li
                        get_storageclass_list = driver.find_elements(By.CSS_SELECTOR,"ul[role=\"listbox\"] > li")
                        while not get_storageclass_list:
                            get_storageclass_list = driver.find_elements(By.CSS_SELECTOR,"ul[role=\"listbox\"] > li")
                        for item in get_storageclass_list:
                            if pvc_storageclass == item.text:
                                item.click()
                                break
                    #PVC Create下面的功能設定(Volume Claim, Customize, Labels & Annotations)
                    get_pvc_create_options = driver.find_elements(By.CSS_SELECTOR,"ul.tabs.vertical > li > a > span")
                    for option in get_pvc_create_options:
                        if option.text == "Customize":
                            option.click()

                            get_option_access_modes = driver.find_elements(By.CSS_SELECTOR,"section#customize > div > div")
                            for namespace_item in get_option_access_modes:
                                #Single Node Read-Write、Many Nodes Read-Only 、Many Nodes Read-Write
                                if namespace_item.text == "Single Node Read-Write":
                                    while namespace_item.find_element(By.CSS_SELECTOR,"label > span.checkbox-custom").get_attribute("aria-checked"):
                                        namespace_item.find_element(By.CSS_SELECTOR,"label").click()
                                        logging_config.info("強制取消 => Single Node Read-Write")
                                if namespace_item.text == "Many Nodes Read-Write":
                                    while not namespace_item.find_element(By.CSS_SELECTOR,"label > span.checkbox-custom").get_attribute("aria-checked"):
                                        namespace_item.find_element(By.CSS_SELECTOR,"label").click()
                                        logging_config.info("強制設定 => Many Nodes Read-Write")
                    #按下Create按鈕
                    driver.find_element(By.CSS_SELECTOR," button.btn.role-primary > span").click()
                    try:
                        driver.find_element(By.CSS_SELECTOR,"div#cru-errors > div > div > span")
                        pvc_done_flage = False
                        logging_config.info("創建PVC失敗")
                    except NoSuchElementException:
                        pvc_done_flage = True
        try_counter = try_counter - 1
    driver.close()
    driver.switch_to.window(main_handle)
    return return_pvc_name

def create_args() -> dict:
    """
    用來創建Argument的程式
    Returns:
        _type_: dict的結構變數
    """
    parser = ArgumentParser(description="Auto Install App Example")
    parser.add_argument(
        "--app_name",
        type=str,
        default="MySQL",
        metavar="XXX",
        help="input App Name (default: MySQL)",
    )
    parser.add_argument(
        "--service_type",
        type=str,
        default="LoadBalancer",
        metavar="LoadBalancer",
        help="input app service type(LoadBalancer、NodePort、ClusterIP) (default: LoadBalancer)",
    )
    parser.add_argument(
        "--name_space", 
        type=str,
        default="test-for-balancer",
        metavar="NNNNNNN",
        help="input name space (default: test-for-balancer)"
    )
    parser.add_argument(
        "--ip",
        type=str,
        default="",
        metavar="172.24.128.170",
        help="Input app ip"
    )
    parser.add_argument(
        "--suf",
        type=str,
        default="balancer",
        metavar="xxxxx",
        help="輸入App名稱後面的修飾詞(都是英文小寫) (default: balancer)"
    )
    parser.add_argument(
        "--StorageClass",
        type=str,
        default="Default",
        metavar="xxxxx",
        help="輸入想要的Storage Class,不輸入則使用系統預設值 (default: Default)"
    )
    parser.add_argument(
        "--StorageSize",
        type=str,
        default="Default",
        metavar="1024",
        help="輸入想要的Storage Size(單位:GB),不輸入則使用系統預設值 (default: Default)"
    )
    parser.add_argument(
        "--OTHER_USR",
        type=str,
        default="None",
        metavar="xxxxx",
        help="輸入要登入的使用者名稱,不輸入,則不修改登入使用者 (default: None)"
    )
    parser.add_argument(
        "--OTHER_PWD",
        type=str,
        default="None",
        metavar="xxxxx",
        help="輸入要登入的使用者密碼,不輸入,則不修改登入密碼 (default: None)"
    )
    parser.add_argument(
        "--LDAP_USR",
        type=str,
        default="None",
        metavar="xxxxx",
        help="輸入LDAP or ActiveDirectory使用者名稱,不輸入,則不使LDAP or ActiveDirectory登入 (default: None)"
    )
    parser.add_argument(
        "--LDAP_PWD",
        type=str,
        default="None",
        metavar="xxxxx",
        help="輸入LDAP or ActiveDirectory使用者密碼,不輸入,則不使LDAPor ActiveDirectory登入 (default: None)"
    )
    parser.add_argument(
        "--SELECT_CHART",
        type=str,
        default="None",
        metavar="xxxxx",
        help="輸入想要使用的Chart Server (default: None)"
    )
    parser.add_argument(
        "--FORCE_IP",
        type=str,
        default="None",
        metavar="X.X.X.X",
        help="輸入想要指定的IP (default: None)"
    )
    args = parser.parse_args()
    logging_config.info("Arguments:")
    for arg in vars(args):
        logging_config.info(f"  {arg}: {getattr(args, arg)}")
    return args


def select_control_ui(uidriver:WebDriver,
                      select_item_1:str="None",
                      select_item_2:str="None",
                      select_item_3:str="None"
                      ) -> None:
    """用來切換控制UI的副程式,當前會有兩種UI,一種是傳統,另一種是依照不同使用者權限來分類button
    Args:
        select_item_1 (str): _description_
        select_item_2 (str): _description_
    """
    #依照不同的數值來辨別UI,0為傳統UI,1為依照使用者權限分類的UI
    ui_type = 0
    ##檢測是否為哪一種UI
    while True:
        logging_config.info("Checking UI Type")
        try:
            WebDriverWait(uidriver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"li#User")))
            ui_type = 1
        except TimeoutException:
            try:
                uidriver.find_element(By.CSS_SELECTOR,"nav.side-nav > div > div > div > a > h6")
            except NoSuchElementException:
                continue
            ui_type = 0
        break
    #print("ui_type => ",ui_type)
    def click_loop(uiwebdriver:WebDriver,list_of_webelement:list,goal_click:str) -> None:
        if goal_click == "None":
            #logging_config.info(f"goal_click == {goal_click} will return")
            return
        for item_tab in list_of_webelement:
            #print("item_tab.text =>",item_tab.text)
            if goal_click == item_tab.text:
                item_tab.click()
                break
        else:
            logging_config.info(f"Not find {goal_click}")
            logging_config.info("Close Driver")
            logging_config.info("======END PROCEDURE=====")
            uiwebdriver.close()
    while ui_type == 0:
        #傳統UI與依使用者權限分類差異
        if  select_item_1 == "Dashboard" or select_item_1 == "Management" or select_item_1 == "Advanced":
            select_item_1 = select_item_2
            select_item_2 = select_item_3
            select_item_3 = "None"
        get_list = uidriver.find_elements(By.CSS_SELECTOR,"nav.side-nav > div > div")
        click_loop(uidriver,get_list,select_item_1)
        get_list = uidriver.find_elements(By.CSS_SELECTOR,"nav.side-nav > div > div > ul > li > a > span.label")
        click_loop(uidriver,get_list,select_item_2)
        break
    while ui_type == 1:
        #依使用者權限分類的UI
        ##User類別:Apps、Virtualization、Advanced
        ##Maintainer:Dashboard、Management(跟Admin不一樣)
        ##Admin類別:Dashboard、Cluster、Management(跟Maintainer不一樣)
        if select_item_1 == "Apps" or select_item_1 == "Virtualization" or select_item_1 == "Advanced":
            WebDriverWait(uidriver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"li#User"))).click()
        elif select_item_1 == "Dashboard" or select_item_1 == "Management":
            WebDriverWait(uidriver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"li#Maintainer"))).click()
        elif select_item_1 == "Dashboard" or select_item_1 == "Cluster" or select_item_1 == "Management":
            WebDriverWait(uidriver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"li#Admin"))).click()
        #section > div > div
        get_list = uidriver.find_elements(By.CSS_SELECTOR,"section[role=\"tabpanel\"] > div > div")
        click_loop(uidriver,get_list,select_item_1)
        get_list = uidriver.find_elements(By.CSS_SELECTOR,"section[role=\"tabpanel\"] > div > ul > li")
        #快速連點會出現問題,ui會卡住,由於手動測試不會出現,所以加入delay,來等待
        sleep(10)
        click_loop(uidriver,get_list,select_item_2)
        get_list = uidriver.find_elements(By.CSS_SELECTOR,"section[role=\"tabpanel\"] > div > ul > li > div > ul > li")

        click_loop(uidriver,get_list,select_item_3)
        break
    

if __name__ == "__main__":

    #csv資料宣告
    csv_data_dict = {}
    #設定Arugment
    args_2 = create_args()

    #修改使用者登入資訊
    if args_2.OTHER_USR != "None":
        ADMIN_USERNAME =args_2.OTHER_USR
    if args_2.OTHER_PWD != "None":
        ADMIN_PASSWORD = args_2.OTHER_PWD


    #修改要使用的Chart Server
    if args_2.SELECT_CHART != "None":
        DEFAULT_CHART = args_2.SELECT_CHART

    #確認StorageSize參數是否都為整數
    if args_2.StorageSize != "Default":
        args_2.StorageSize = args_2.StorageSize.replace(" ","")
        for item in args_2.StorageSize:
            if ord(item) < 48 or ord(item) > 57:
                logging_config.info(f"StorageSize, {args_2.StorageSize}, is not integer")
                logging_config.info("===========================StorageSize Error End===========================")
                sys.exit(1)


    #檢查FORCE IP 是否符合IPv4規範且符合Cluster IP 範圍,並且設定FORCE_IP旗標
    SET_FORCE_IP_FLAG = False
    if args_2.FORCE_IP != "None":
        args_2.FORCE_IP = args_2.FORCE_IP.replace(" ","")
        ip_data_check = args_2.FORCE_IP
        ##檢查字元是否為0~9
        for character in ip_data_check:
            if 48 <= ord(character) <=57 or ord(character) == 46:
                pass
            else:
                print("FORCE IP 有輸入錯誤")
                sys.exit(0)
        ##檢查ip是否超過255
        for item in ip_data_check.split("."):
            if int(item) > 255:
                print("FORCE IP 大小錯誤")
                sys.exit(0)
        ##檢查ip是否為ip v4
        if len(ip_data_check.split(".")) % 4 != 0:
            print(len(ip_data_check.split(".")))
            print("非IPv4 IP")
            sys.exit(0)
        ##檢查是否為Cluster IP指定範圍的IPv4
        CLUSTER_IP_START = CLUSTER_IP_START.replace(" ","")
        CLUSTER_IP_END = CLUSTER_IP_END.replace(" ","")
        C_I_S = CLUSTER_IP_START.split(".")
        C_I_E = CLUSTER_IP_END.split(".")
        F_I = args_2.FORCE_IP.split(".")
        for i in range(4):
            if C_I_S[i] != F_I[i]:
                if int(F_I[i]) >= int(C_I_S[i]) and int(F_I[i]) <= int(C_I_E[i]):
                    SET_FORCE_IP_FLAG = True
                else:
                    logging_config.info(f"FORCE IP, {args_2.FORCE_IP}, is not within IP range of Cluster")
                    SET_FORCE_IP_FLAG = False
                    sys.exit(0)
    #啟動chrome
    driver = webdriver.Chrome(service=service, options=options)
    #隱式等待，如果沒有找到元素，每0.5秒重新找一次，直到10秒過後
    driver.implicitly_wait(10)



    #設定logging config
    logging_config.set_consolehandler_level("INFO")

    #檢查網頁是否連線正常
    #response = requests.get(RANCHER_ip, timeout=10, verify=False)
    #if response.status_code != 200:
    #   logging_config.info(f"網路異常, 網路status_code = {response.status_code}連線網址 ={RANCHER_ip}")
    #   sys.exit(1)

    '''
    #獲取App清單,並且依造其Config來安裝App
    get_app_list = []
    get_app_json_config ={}
    APP_INDEX = "App Config/"
    with open("App_install_list.txt","r",encoding="utf-8") as f:
        get_str = f.readline()
        while get_str !='':
            get_app_list.append(get_str.rstrip("\n"))
            get_str = f.readline()
    logging_config.info("get_app_list=" + str(get_app_list))

    for app_name_item in get_app_list:
        get_file_path = APP_INDEX + app_name_item + ".json"
        if not os.path.isfile(get_file_path):
            logging_config.info(str(get_file_path) + "is not found")
            continue
        with open(APP_INDEX + app_name_item + ".json","r",encoding="utf-8") as f:
            get_app_json_config = dict(json.load(f))
        logging_config.info("get_app_json_config ="+ str(get_app_json_config))
    '''
    #檢查該App是否有Configure檔案
    APP_INDEX = "App Config/"
    get_file_path = APP_INDEX + args_2.app_name + ".json"
    if not os.path.isfile(get_file_path):
        logging_config.info(str(get_file_path) + "is not found")
        logging_config.info("結束該App的安裝")
        driver.close()
        sys.exit(0)
    #獲取該App的Config,並且依照Argument來修改參數
    test_dict = {}
    with open(get_file_path,"r",encoding="utf-8") as f:
        test_dict = dict(json.load(f))
    if test_dict["Service"].get("App Image Service Type *",False):
        test_dict["Service"]["App Image Service Type *"] = args_2.service_type
        #刪除LoadBalancer的IP設定
        if test_dict["Service"]["App Image Service Type *"] != "LoadBalancer":
            test_dict["Service"].pop("Static Virtual IP *",None)
    #針對LocalAI格式不一樣來作解決
    if test_dict["Service"].get("App Service Type *",False):
        test_dict["Service"]["App Service Type *"] = args_2.service_type
        #刪除LoadBalancer的IP設定
        if test_dict["Service"]["App Service Type *"] != "LoadBalancer":
            test_dict["Service"].pop("Static Virtual IP *",None)
    #針對MinIO來跟改Service 的設定(因為名稱與)
    if test_dict["Service"].get("MinIO Web Service Type *",False):
        test_dict["Service"]["MinIO Web Service Type *"] = args_2.service_type
        #刪除LoadBalancer的IP設定
        if test_dict["Service"]["MinIO Web Service Type *"] != "LoadBalancer":
            test_dict["Service"].pop("Static Virtual IP for MinIO *",None)
    #是否要指定Storage Class,並且檢查Storage設定是否有誤
    if args_2.StorageClass != "Default":
        #整理StorageClass參數,必定為local,local-delay-bind,local-replica2,local-replica2-delay-bind,local-replica3,local-replica3-delay-bind
        args_2.StorageClass = args_2.StorageClass.replace(" ","")
        #檢查是否為cluster中的storageclass名稱
        get_storage_class_list = []
        while not get_storage_class_list:
            get_storage_class_list = communicate_to_machine.all_node_to_connect_k8s("kubectl get storageclass | awk '{print$1}' | grep -v NAME")
        for storageclass_name in get_storage_class_list:
            if args_2.StorageClass == storageclass_name:
                break
        else:
            logging_config.info(f"StorageClass 設定值為{ args_2.StorageClass} 無法辨識")
            logging_config.info("StorageClass Will set \" default storageclass \"")
            args_2.StorageClass = "Default"
        #檢查是否為預設值StorageClass
        if args_2.StorageClass != "Default":
            get_default_storageclass = communicate_to_machine.all_node_to_connect_k8s("kubectl get storageclass | grep \(default\)  | awk '{print$1}' | grep -v NAME")
            if args_2.StorageClass == get_default_storageclass[0]:
                logging_config.info(f"StorageClass 預設設定值為{get_default_storageclass[0]}, StorageClass 更改為\"Default\"")
                args_2.StorageClass = "Default"
        try:
            if args_2.StorageClass != "Default":
                test_dict["Storage"].update(test_dict["Storage"].pop("Use Default Storage Class"))
            else:
                #如果不需要指定StorageClass則移除該參數
                try:
                    test_dict["Storage"].pop("Use Default Storage Class")
                except KeyError:
                    pass
        except KeyError:
            logging_config.info("json File can't found \"Use Default Storage Class\" Setting")
            logging_config.info("End install")
            driver.close()
            sys.exit(0)
        while test_dict.get("Storage",True):
            logging_config.debug(test_dict)
            if test_dict.get("Storage",False):
                break
    else:
        #如果不需要指定StorageClass則移除該參數
        try:
            test_dict["Storage"].pop("Use Default Storage Class")
        except KeyError:
            pass

    #檢查是否要設定Storage Size,如果沒有則移除相關參數Storage Size
    for item in list(test_dict["Storage"].keys()):
        if item.find("Storage Size") >= 0 or item.find("PVC Size") >= 0:
            if args_2.StorageSize != "Default":
                logging_config.info(f"Find Storage Size, {item}, will set {args_2.StorageSize}Gi")
                test_dict["Storage"][item] = args_2.StorageSize + "Gi"
            else:
                #logging_config.info(f"Find Storage Size, {item}, will be removed")
                test_dict["Storage"].pop(item)


    #獲取csv資料
    csv_data_dict['App Name'] = args_2.app_name
    csv_data_dict['Name Space'] = args_2.name_space
    csv_data_dict['IP'] = "None"
    ##因為Service Type的Key不一定是App Image Service Type *,所以要再檢查是否含有Service Type或者Ingress的字樣
    if test_dict["Service"].get("App Image Service Type *","None") == "None":
        get_key = ""
        for key_item in test_dict["Service"].keys():
            if key_item.rfind("Service Type") > -1:
                csv_data_dict['Service type'] = test_dict["Service"].get(key_item,"None")
                break
            elif key_item.rfind("Ingress") > -1:
                csv_data_dict['Service type'] = "Ingress"
                break
        else:
            csv_data_dict['Service type'] = "None"
    else:
        csv_data_dict['Service type'] = test_dict["Service"].get("App Image Service Type *","None")

    #開啟網址
    while True:
        try:
            driver.set_page_load_timeout(60)
            driver.get(RANCHER_ip)
            driver.set_page_load_timeout(300)
            break
        except TimeoutException:
            pass
    #登入
    #登入EonKube
    ##OpenLDAP登入-Start
    EONKUBE_LDAP_USER = args_2.LDAP_USR
    EONKUBE_LDAP_PASSWORD = args_2.LDAP_PWD
    DO_WHILE_FLAG = True
    while EONKUBE_LDAP_USER != "None" and EONKUBE_LDAP_PASSWORD != "None":
        DO_WHILE_FLAG = False
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div > button")))
        get_login_button = driver.find_element(By.CSS_SELECTOR,"div > button")
        if get_login_button.text != "Log in with OpenLDAP" and get_login_button.text != "Log in with ActiveDirectory":
            logging_config.info("======End LDAP or ActiveDirectory Login=====")
            logging_config.info("======No LDAP or ActiveDirectory MODE=====")
            driver.close()
            sys.exit(0)
        get_login_list = driver.find_elements(By.CSS_SELECTOR,"div.labeled")
        for item in get_login_list:
            string_2_ascii.string_to_hex(item.text)
            if item.text == "Username":
                item.find_element(By.CSS_SELECTOR,"div > input").send_keys(EONKUBE_LDAP_USER)
            elif item.text == "Password":
                item.find_element(By.CSS_SELECTOR,"div > input").send_keys(EONKUBE_LDAP_PASSWORD)
            else:
                print("get nothing")
        #解決登入鍵案太快的問題
        while True:
            try:
                sleep(1) #加這個是因為會有Bug
                get_login_button.click()
                WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.banner.error > div.banner__content")))
                LOGIN_ERROR_MESSAGE = driver.find_element(By.CSS_SELECTOR,"div.banner.error > div.banner__content").text
                logging_config.info(f"Error Message:{LOGIN_ERROR_MESSAGE}")
                logging_config.info("======End LDAP or ActiveDirectory Login=====")
                driver.close()
                sys.exit(0)
            except TimeoutException:
                pass
            except StaleElementReferenceException:
                break
            except ElementClickInterceptedException:
                try:
                    #查看是否有登入後的Dashboard頁面,來作為是否已經登入的判斷基準
                    WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"section.dashboard.outlet")))
                except TimeoutException:
                    continue
        #LDAP登入流程結束
        break
    ##OpenLDAP登入-end
    #DO_WHILE_FLAG = True
    while DO_WHILE_FLAG:
        DO_WHILE_FLAG = False
        #檢查當前網頁是否為正確網頁
        if driver.current_url.find(RANCHER_ip) < 0:
            logging_config.info(f"will go to {RANCHER_ip}")
            driver.get(RANCHER_ip)
        try:
            WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"input#username")))
        except TimeoutException:
            try:
                #從Active Directory切換到local user 
                WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a#login-useLocal"))).click()
            except TimeoutException:
                driver.refresh()
                logging_config.info("Try to login local user")
                DO_WHILE_FLAG = True
                sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR,"input#username").send_keys(ADMIN_USERNAME)
            driver.find_element(By.CSS_SELECTOR,"input[type=\"password\"]").send_keys(ADMIN_PASSWORD)
            sleep(1)
            driver.find_element(By.CSS_SELECTOR,"button#submit").click()
            sleep(3)
        except NoSuchElementException:
            #可能已經登入
            pass
        #檢查是否有該使用者,如果沒有則會顯示錯誤訊息,並且關閉該流程
        try:
            WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.login-messages > div.banner.error")))
            get_error_msg = driver.find_element(By.CSS_SELECTOR,"div.login-messages > div.banner.error").text
            logging_config.info(f"Log in fail => {get_error_msg}")
            driver.close()
            sys.exit(0)
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass
        #將Project id 固定為"Only User Namespaces"
        try:
            WebDriverWait(driver,300).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.ns-filter > div > div")))
            get_project_id_name = driver.find_element(By.CSS_SELECTOR,"div.ns-filter > div > div")
            logging_config.debug(f"get_project_id_name.text ={get_project_id_name.text}")
            if get_project_id_name.text != "Only User Namespaces":
                get_project_id_name.click()
                get_project_id_list = driver.find_elements(By.CSS_SELECTOR,"div.ns-options > div")
                for project_id_item in get_project_id_list:
                    logging_config.debug(f"project_id_item.text = {project_id_item.text}")
                    if project_id_item.text == "Only User Namespaces":
                        project_id_item.click()
                        driver.find_element(By.CSS_SELECTOR,"div.ns-filter > div > div").click()
                        break
            DO_WHILE_FLAG = False
        except NoSuchElementException:
            logging_config.info("NoSuchElementException-Try to login local user")
            driver.refresh()
            DO_WHILE_FLAG = True
            sleep(3)
        except TimeoutException:
            logging_config.info("TimeoutException-Try to login local user")
            driver.refresh()
            DO_WHILE_FLAG = True
            sleep(3)

    #預先創建PVC,解決在安裝App時,創建PVC無法讀取到的問題
    PVC_QUEUE = {}
    while test_dict.get("Storage",False):
        #當前App軍可以自主建立PVC
        break
        for json_option in list(test_dict['Storage'].keys()):
            #兩種狀況,Storage Class或者要創建PVC
            if not str(json_option).startswith("StorageClass"):
                if test_dict['Storage'].get(str(json_option),False):
                    meta_get_pvc_name = test_dict['Storage'][str(json_option)]
                    GET_PVC_NAME = create_pvc(args_2.name_space,meta_get_pvc_name,args_2.StorageClass)
                    PVC_QUEUE[meta_get_pvc_name] = GET_PVC_NAME
                    logging_config.info(f"PVC[{meta_get_pvc_name}]={GET_PVC_NAME}")
        break
    #點選UI控制Tab
    select_control_ui(driver,"Apps","Marketplace")
    #select_control_ui(driver,"Apps","Installed Apps")
    #select_control_ui(driver,"Advanced","Storage","PersistentVolumeClaims")
    #sys.exit(0)

    #點選App Charts中的 ALL
    WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.left-right-split > div.unlabeled-select.checkbox-select.edit")))
    get_chart_name = driver.find_element(By.CSS_SELECTOR,"div.left-right-split > div.unlabeled-select.checkbox-select.edit")
    
    logging_config.info(f"Current Chart: {get_chart_name.text}")
    if get_chart_name.text != DEFAULT_CHART:
        get_chart_name.click()
        get_chart_list = driver.find_elements(By.CSS_SELECTOR,"ul.vs__dropdown-menu[role=\"listbox\"] > li[role=\"option\"]")
        #先檢查是否有該Chart Server
        for chart in get_chart_list:
            if chart.text == DEFAULT_CHART:
                #chart.find_element(By.CSS_SELECTOR,"div > label").click()
                #logging_config.info(f"Alter Chart: {DEFAULT_CHART}")
                break
            #print("chart =>",chart.text)
            #string_2_ascii.string_to_hex(chart.text)
            #print("=========")
        else:
            logging_config.info(f"Default Chart \"{DEFAULT_CHART}\" not found")
            driver.close()
            sys.exit(0)
        #選擇指定的Chart Server,並且將其他改取消勾選
        for chart in get_chart_list:
            if chart.text == DEFAULT_CHART:
                is_check = chart.find_element(By.CSS_SELECTOR,"div > label > span").get_attribute("aria-checked")
                if not is_check:
                    chart.find_element(By.CSS_SELECTOR,"div > label").click()
                    logging_config.info(f"Alter Chart: {DEFAULT_CHART}")
                if chart.text =="All" and DEFAULT_CHART == "All":
                    break
            else:
                #其他Chart Server有勾選起來要取消
                is_check = chart.find_element(By.CSS_SELECTOR,"div > label > span").get_attribute("aria-checked")
                if is_check:
                    chart.find_element(By.CSS_SELECTOR,"div > label").click()
                
    #決定Chart
    #driver.find_element(By.CSS_SELECTOR,"div[role=\"combobox\"] > div.vs__actions").click()
    while True:
        try:
            chart_click = driver.find_element(By.CSS_SELECTOR,"div[role=\"combobox\"] > div.vs__actions")
            ActionChains(driver).move_to_element(chart_click).click().perform()
            if driver.find_element(By.CSS_SELECTOR,"div[role=\"combobox\"]").get_attribute("aria-expanded") == "false":
                break
        except ElementClickInterceptedException:
            logging_config.info("Close dropdown list of chart")
    #點選chart中的App
    try:
        WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"main > div > div > div.grid > div:nth-child(1) > h4.name")))
    except TimeoutException:
        logging_config.info("There is no app")
        logging_config.info("====END====")
        driver.close()

    #開始安裝App
    csv_data_dict['App Name'] = install_from_chart_to_app_deploy(args_2.app_name,args_2.suf,args_2.name_space)
    if not csv_data_dict['App Name']:
        driver.close()
        sys.exit(0)
    print(test_dict)
    #依照不同功能來設定App
    while test_dict.get("General",False):
        logging_config.info("在General")
        driver.find_element(By.CSS_SELECTOR,"li#General > a").click()
        get_options = driver.find_elements(By.CSS_SELECTOR,"section#General >  div > div > div > div > div > div ")
        for i, item in enumerate(get_options):
            logging_config.debug(item.find_element(By.CSS_SELECTOR,"label").text)
            for json_option in list(test_dict['General'].keys()):
                logging_config.debug(f"test_dict['General'][str(json_option)] =>{test_dict['General'][str(json_option)]}")
                logging_config.debug(json_option)
                if item.find_element(By.CSS_SELECTOR,"label").text == str(json_option):
                    try:
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.CONTROL+"a")
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.DELETE)
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(test_dict['General'][str(json_option)])
                    except NoSuchElementException as e:
                        logging_config.debug(e.msg)
                        logging_config.debug(json_option)
                        get_options[i+1].find_element(By.CSS_SELECTOR,"div > div").click()
                        select_list = driver.find_elements(By.CSS_SELECTOR,"ul.vs__dropdown-menu > li")
                        for select_item in select_list:
                            if select_item.text == test_dict["General"][str(json_option)]:
                                select_item.click()
                                break
                    break
        break

    while test_dict.get("Storage",False):
        set_pvc_flag = True
        try:
            storage_tag = driver.find_element(By.CSS_SELECTOR,"li#Storage > a")
            storage_tag.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView();", storage_tag)
            driver.execute_script("arguments[0].click();",storage_tag)
        logging_config.info("In Storage tab")
        if args_2.StorageClass != "Default":
            default_storage_class_button = driver.find_element(By.CSS_SELECTOR,"span[aria-label=\"Use Default Storage Class\"].checkbox-custom")
            try:
                default_storage_class_button.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].scrollIntoView();", default_storage_class_button)
                driver.execute_script("arguments[0].click();",default_storage_class_button)
            ##Check cancel check box
            default_storage_class_button = driver.find_element(By.CSS_SELECTOR,"span[aria-label=\"Use Default Storage Class\"].checkbox-custom")
            #aria-checked
            while default_storage_class_button.get_attribute("aria-checked"):
                default_storage_class_button = driver.find_element(By.CSS_SELECTOR,"span[aria-label=\"Use Default Storage Class\"].checkbox-custom")
                print("點完後=>",default_storage_class_button.get_attribute("aria-checked"))
        get_options = driver.find_elements(By.CSS_SELECTOR,"section#Storage >  div > div > div > div > div > div ")
        for i, item in enumerate(get_options):
            try:
                logging_config.debug(item.find_element(By.CSS_SELECTOR,"label").text)
            except NoSuchElementException as e:
                logging_config.debug(e.msg)
                logging_config.debug("沒有Label相關元素,下一個資料")
                continue
            except StaleElementReferenceException as e:
                logging_config.debug(e.msg)
                logging_config.debug("沒有Label相關元素,下一個資料")
                continue
            #(有選單的)設定Storage PVC
            for json_option in list(test_dict['Storage'].keys()):
                if item.find_element(By.CSS_SELECTOR,"label").text == str(json_option):
                    try:
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.CONTROL+"a")
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.DELETE)
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(test_dict['Storage'][str(json_option)])
                    except NoSuchElementException as e:
                        logging_config.debug(e.msg)
                        logging_config.info(json_option)
                        #按完之後,會跳出選單
                        #==========================
                        #section#Storage >  div > div > div > div > div > div
                        GET_PVC_NAME = ""
                        #有兩種選單,一種是要指定Storage Class,另一種要指定PVC
                        if str(json_option).startswith("StorageClass"):
                            #GET_PVC_NAME = "local-replica2-delay-bind"
                            if args_2.StorageClass != "Default":
                                GET_PVC_NAME = args_2.StorageClass
                                logging_config.info(f"即將設定Storage Class = {GET_PVC_NAME}")
                            else:
                                get_storage_class_list = []
                                while not get_storage_class_list:
                                    get_storage_class_list = communicate_to_machine.all_node_to_connect_k8s("kubectl get storageclass")
                                for item in get_storage_class_list:   
                                    if str(item).find("(default)") > 0:
                                        GET_PVC_NAME = item[0:str(item).find("(default)")].replace(" ","")
                                        logging_config.info(f"從底層獲得預設Storage Class = {GET_PVC_NAME}")
                                #如果有找到Storage Class相關設定,就採用設定值,如果沒有就使用預設值
                                if test_dict["Storage"].get("StorageClass for Database *",False):
                                    if str(test_dict["Storage"]["StorageClass for Database *"]) != "":
                                        GET_PVC_NAME = str(test_dict["Storage"]["StorageClass for Database *"])
                                    logging_config.info(f"在json中找到Storage Class設定值 = {GET_PVC_NAME}")
                        else:
                            if test_dict['Storage'].get(str(json_option),False):
                                meta_get_pvc_name = test_dict['Storage'][str(json_option)]
                                logging_config.info(f"json pvc 設定名稱{meta_get_pvc_name}")
                                if PVC_QUEUE.get(meta_get_pvc_name,False):
                                    GET_PVC_NAME = PVC_QUEUE[meta_get_pvc_name]
                                else:
                                    GET_PVC_NAME = create_pvc(args_2.name_space,meta_get_pvc_name,args_2.StorageClass)
                            else:
                                GET_PVC_NAME = create_pvc(select_name_space=args_2.name_space,pvc_storageclass=args_2.StorageClass)
                            logging_config.info(f"收到的PVC名稱{GET_PVC_NAME}")
                            logging_config.debug(f"i={i}")
                        try:
                            get_options[i+1].click()
                        except ElementClickInterceptedException:
                            element = get_options[i+1]
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            driver.execute_script("$(arguments[0]).click()",element)
                        get_pvc_list = driver.find_elements(By.CSS_SELECTOR,"ul.vs__dropdown-menu > li.vs__dropdown-option")
                        for pvc_item in get_pvc_list:
                            logging_config.debug(f"pvc_item={pvc_item.text}")
                            if pvc_item.text == GET_PVC_NAME and set_pvc_flag:
                                pvc_item.click()
                                break
                        else:
                            set_pvc_flag = False
                            logging_config.info(f"PVC Not Found={GET_PVC_NAME}")
                            logging_config.info("The procedure will terminate")
                            logging_config.info("========================TERMINATED========================")
                            driver.close()
                            sys.exit(0)
                        logging_config.debug(f"{json_option}--END")
        if set_pvc_flag:
            break

    while test_dict.get("Service",False):
        driver.find_element(By.CSS_SELECTOR,"li#Service > a").click()
        get_options = driver.find_elements(By.CSS_SELECTOR,"section#Service >  div > div > div > div > div > div ")
        logging_config.info("In Service tab")
        #Service相關設定
        for i, item in enumerate(get_options):
            try:
                logging_config.info(item.find_element(By.CSS_SELECTOR,"label").text)
            except NoSuchElementException as e:
                logging_config.debug(e.msg)
                #logging_config.info(json_option)
                logging_config.debug("沒有Label相關元素,下一個資料")
                continue
            except StaleElementReferenceException as e:
                logging_config.debug(e.msg)
                #logging_config.info(json_option)
                logging_config.debug("沒有Label相關元素,下一個資料")
                continue
            #(有選單的)設定Service Type
            for json_option in list(test_dict['Service'].keys()):
                if item.find_element(By.CSS_SELECTOR,"label").text == str(json_option):
                    try:
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.CONTROL+"a")
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.DELETE)
                        if str(json_option) == "Static Virtual IP *":
                            if SET_FORCE_IP_FLAG:
                                get_new_ip = args_2.FORCE_IP
                            else:
                                get_new_ip = get_nodes_available_ip.get_available_cluster_ip(test_dict['Service']['Static Virtual IP *'])
                            while get_new_ip == None:
                                get_new_ip = get_nodes_available_ip.get_available_cluster_ip(test_dict['Service']['Static Virtual IP *'])
                                logging_config.info("==從底層獲取IP失敗,請排除問題==")
                                logging_config.info("==重試直到獲取IP為止==")
                            csv_data_dict['IP'] = get_new_ip
                            logging_config.info(f"IP 設定:{get_new_ip}")
                            #沒有找到可用的IP
                            if get_new_ip == "None ip can be available":
                                logging_config.info("There is no ip available")
                                driver.close()
                                sys.exit(0)
                            item.find_element(By.CSS_SELECTOR," div > input").send_keys(get_new_ip)
                        elif str(json_option) == "Static Virtual IP for MinIO *":
                            if SET_FORCE_IP_FLAG:
                                get_new_ip = args_2.FORCE_IP
                            else:
                                get_new_ip = get_nodes_available_ip.get_available_cluster_ip(test_dict['Service']['Static Virtual IP for MinIO *'])
                            while get_new_ip == None:
                                get_new_ip = get_nodes_available_ip.get_available_cluster_ip(test_dict['Service']['Static Virtual IP *'])
                                logging_config.info("==從底層獲取IP失敗,請排除問題==")
                                logging_config.info("==重試直到獲取IP為止==")
                            csv_data_dict['IP'] = get_new_ip
                            logging_config.info(f"IP 設定:{get_new_ip}")
                            #沒有找到可用的IP
                            if get_new_ip == "None ip can be available":
                                logging_config.info("There is no ip available")
                                driver.close()
                                sys.exit(0)
                            item.find_element(By.CSS_SELECTOR," div > input").send_keys(get_new_ip)
                        else:
                            item.find_element(By.CSS_SELECTOR," div > input").send_keys(test_dict['Service'][str(json_option)])
                    except NoSuchElementException as e:
                        logging_config.debug(e.msg)
                        logging_config.info(json_option)
                        #按完之後,會跳出選單
                        try:
                            get_options[i+1].find_element(By.CSS_SELECTOR,"div > div").click()
                        except ElementClickInterceptedException:
                            #WebDriverWait(get_options[i+1],30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div > div"))).click()
                            element = get_options[i+1].find_element(By.CSS_SELECTOR,"div > div")
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            driver.execute_script("$(arguments[0]).click()",element)
                        storage_pvcs = driver.find_elements(By.CSS_SELECTOR,"ul.vs__dropdown-menu > li")
                        for service_item in storage_pvcs:
                            logging_config.info(service_item.text)
                            if service_item.text == test_dict["Service"][str(json_option)]:
                                #LoadBalancer、NodePort、ClusterIP
                                service_item.click()
                                break
                    break
        #Service-Ingress相關設定
        while(test_dict["Service"].get("Ingress",False)):
            logging_config.info("IP Service Ingress Setting")
            get_options = driver.find_elements(By.CSS_SELECTOR,"section#Service >  div > div > div > div > div ")
            for item in get_options:
                logging_config.info(item.find_element(By.CSS_SELECTOR,"label").text)
                for json_option in list(test_dict['Service']['Ingress'].keys()):
                    logging_config.info(f"App ingress config =>{json_option}")
                    if item.find_element(By.CSS_SELECTOR,"label").text == str(json_option):
                        get_ingress_name = test_dict['Service']['Ingress'][str(json_option)]
                        logging_config.info(f"ingress name =>{get_ingress_name}")
                        #使用亂數來創造名字
                        string_nuber = 8
                        print_string = ""
                        get_str_list = random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',string_nuber)
                        for number in range(string_nuber):
                            print_string = print_string + get_str_list[number]
                        get_ingress_name = get_ingress_name + "-" + print_string
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.CONTROL+"a")
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.DELETE)
                        item.find_element(By.CSS_SELECTOR," div > input").send_keys(get_ingress_name)
            break                        
        break

    while test_dict.get("APP setting",False):
        driver.find_element(By.CSS_SELECTOR,"li#APP\\ setting > a").click()
        logging_config.info("IN APP setting tab")
        if args_2.app_name == "Milvus":
            get_check_flage = False
            while not get_check_flage:  
                get_options = driver.find_elements(By.CSS_SELECTOR,"section#APP\\ setting >  div > div > div > div > div > label ")
                for item in get_options:
                    if item.text == "Enable Attu (Milvus Web UI)":
                        item.click()
                get_check_flage = driver.find_element(By.CSS_SELECTOR,"section#APP\\ setting >  div > div > div > div > div > label > span.checkbox-custom").get_attribute("aria-checked")
            get_options = driver.find_elements(By.CSS_SELECTOR,"section#APP\\ setting >  div > div > div > div > div")
        else:
            get_options = driver.find_elements(By.CSS_SELECTOR,"section#APP\\ setting >  div > div > div > div > div > div ")
        for i, item in enumerate(get_options):
            try:
                logging_config.info(item.find_element(By.CSS_SELECTOR,"label").text)
            except NoSuchElementException as e:
                logging_config.debug(e.msg)
                logging_config.info(json_option)
                logging_config.debug("沒有Label相關元素,下一個資料")
                continue
            except StaleElementReferenceException as e:
                logging_config.debug(e.msg)
                logging_config.info(json_option)
                logging_config.debug("沒有Label相關元素,下一個資料")
                continue
            for json_option in list(test_dict['APP setting'].keys()):
                logging_config.debug(f"json_option ={json_option}")
                logging_config.info(test_dict['APP setting'][str(json_option)])
                if item.find_element(By.CSS_SELECTOR,"label").text == str(json_option):
                    try:
                        if args_2.app_name == "Kibana" or args_2.app_name == "Logstash":
                            get_string = item.find_element(By.CSS_SELECTOR," div > input").get_attribute("value")
                            will_send_cmd = "helm list -n " + args_2.name_space + " | grep elasticsearch | " + "awk \'{print $1}\'"
                            get_response = communicate_to_machine.all_node_to_connect_k8s(will_send_cmd)
                            new_string = get_string[0:get_string.find("elasticsearch-master")] + str(get_response[0]).replace(" ","")+ "-" + get_string[get_string.find("elasticsearch-master"):len(get_string)]
                            if not get_response[0]:
                                logging_config.info(f"Elasticsearch name Not Found => {get_response}")
                                driver.close()
                                sys.exit(0)
                            item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.CONTROL+"a")
                            item.find_element(By.CSS_SELECTOR," div > input").send_keys(Keys.DELETE)
                            item.find_element(By.CSS_SELECTOR," div > input").send_keys(new_string)
                        else:
                            item.find_element(By.CSS_SELECTOR," div > input"
                                            ).send_keys(Keys.CONTROL+"a")
                            item.find_element(By.CSS_SELECTOR," div > input"
                                            ).send_keys(Keys.DELETE)
                            item.find_element(By.CSS_SELECTOR," div > input"
                                            ).send_keys(test_dict['APP setting'][str(json_option)])
                    except NoSuchElementException as e:
                        logging_config.debug(e.msg)
                        logging_config.info(json_option)
                        get_options[i+1].find_element(By.CSS_SELECTOR,"div > div").click()
                        select_list = driver.find_elements(By.CSS_SELECTOR,
                                                           "ul.vs__dropdown-menu > li")
                        for select_item in select_list:
                            if select_item.text == test_dict["APP setting"][str(json_option)]:
                                select_item.click()
                                break
                    break
        break



    #安裝App
    driver.find_element(By.CSS_SELECTOR,"div#wizard-footer-controls > div > button.btn.role-primary").click()


    #確認App是否安裝了,在嘗試確認100次後,都沒有就不會自動關閉瀏覽器
    for i in range(100):
        logging_config.info(f"確認App是否安裝,檢查次數{i+1}")
        logging_config.info(f"{csv_data_dict['App Name']},{args_2.name_space}")
        if communicate_to_machine.check_app_pending(csv_data_dict['App Name'],args_2.name_space):
            break
        sleep(1)
    else:
        logging_config.info(f"\"{csv_data_dict['App Name']}\"無法在{args_2.name_space}確認正在安裝(Pending)")


    #倒數關閉
    logging_config.info("即將關閉瀏覽器")

    #匯出資料
    export_csv_file(csv_data_dict)
    count_down = 10
    for i in range(count_down):
        logging_config.info(f"{count_down-i-1} s")
        sleep(1)
    driver.close()
