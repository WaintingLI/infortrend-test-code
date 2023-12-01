from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from time import sleep
import sys,os,re
import logging
import configparser
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
options.add_argument('window-size=1600x900')
#options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#driver_location='/usr/bin/chromedriver'
#指令Chromedriver位置
#binary_location='/usr/bin/google-chrome'
#options.binary_location=binary_location
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="./chromedriver.exe")


#啟動chrome
driver = webdriver.Chrome(service=service, options=options)



if __name__ == "__main__":
    #開啟網址
    driver.get("http://opencart-test.k8s.local/en-gb?route=account/wishlist&customer_token=202c0ae5e055148d7f6bf0875c")
    for i in range (30):
        print("剩餘秒數 =", (30-i))
        sleep(1)
    response = requests.get(driver.current_url)
    #response = requests.get("http://opencart-test.k8s.local/")
    #response = requests.get("https://journal3.ga4.one/")
    #response = requests.get("http://opencart-test.k8s.local/en-gb/catalog/smartphone")
    
    #藉由selenium套來獲取當前網頁的html
    html = driver.find_element(By.XPATH,"//*").get_attribute("outerHTML")
    print(" html =",html)
    #soup = BeautifulSoup(response.text, "html.parser")
    
    #將html字串，移交給BeautifulSoup套件分析
    soup = BeautifulSoup(html, "html.parser")
    
    #將資料輸出到txt檔案(如果該檔案已經存在，會將新的資料添加在檔案內容的最下方)
    with open('./test.txt','a',encoding="utf-8") as file0:
        #print(soup.prettify())  #輸出排版後的HTML內容
        print(f'{soup.prettify()}' ,file=file0)
    
    results = soup.find_all("td",class_ = "text-start")
    print("results = ",results)
    print("================================================================")
    #將清單的資料，一個一個打印出來
    for item in results:
        print(item.get_text())
    #print("results = ",results)
    #print(soup.prettify())
    
    
    #text = soup.find("h3").get_text()
    #print("text =",text)
    #print("soup.find(\"h3\").getText =" , soup.select_one("h3").get_text() )
    
    
    driver.close()
    #while(True): pass