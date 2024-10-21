'''
獲取最新版本且穩定的Chromedriver網址
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
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import SessionNotCreatedException
import requests as rq
import shutil
from bs4 import BeautifulSoup


#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

def get_stable_chromedriver_website(chrome_item:str="chromedriver", chose_os:str="win64") -> str:
    """_summary_

    Args:
        chrome_item (str): 尋找的東西,ex:chromedriver
        chose_os (str): 作業系統,ex:win64

    Returns:
        str: 下載的網址,如果找不到匯回傳None
    """
    url = "https://googlechromelabs.github.io/chrome-for-testing/" # Chromedriver website
    response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
    #會去收尋穩定版本的下載網址
    meta = soup.find("section",{"id": "stable"})
    posts = meta.findAll("code")
    for i, item in enumerate(posts):
        if item.string == chrome_item and posts[i+1].string == chose_os and posts[i+3].string == "200":
            return posts[i+2].string
            #print(posts[i].string) #顯示chromedriver
            #print(posts[i+1].string)#顯示win64
            #print(posts[i+2].string)#顯示下載網址
            #print(posts[i+3].string)#顯示狀態200
            #print("====================")
    return None


if __name__ == "__main__":
    url = "https://googlechromelabs.github.io/chrome-for-testing/" # Chromedriver website
    response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
    #print(soup.prettify()) # 把排版後的 html 印出來
    print("=============================================================") 
    #print(soup.find_all("tr", class_= "status-ok"))
    #posts = soup.find_all("code")
    #會去收尋穩定版本的下載網址
    meta = soup.find("section",{"id": "stable"})
    #print(meta.prettify())
    posts = meta.findAll("code")
    
    
    
    
    print(type(posts))
    for i, item in enumerate(posts):
        if item.string == "chromedriver" and posts[i+1].string == "win64" and posts[i+3].string == "200":
            print(posts[i].string) #顯示chromedriver
            print(posts[i+1].string)#顯示win64
            print(posts[i+2].string)#顯示下載網址
            print(posts[i+3].string)#顯示狀態200
            print("====================")
            
