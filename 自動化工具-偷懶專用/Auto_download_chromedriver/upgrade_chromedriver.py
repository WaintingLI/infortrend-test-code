'''
給Windows (x64)自動下載最新版本的Chrome Driver 來用,前提是chromedriver要在當前目錄
'''
from time import sleep
import sys
import os
import configparser
import zipfile
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import SessionNotCreatedException
import requests
import shutil
import get_chromedriver_website

#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

def start() -> None:
    """_summary_
    自動更新當前目錄下的chromedriver.exe
    """
    download_url = get_chromedriver_website.get_stable_chromedriver_website()
    response = requests.get(download_url,timeout= 10)
    with open('test_meta_data.zip', 'wb') as file:
        file.write(response.content)
        file.close()
    #解壓縮文件
    files = zipfile.ZipFile("test_meta_data.zip")
    files.extractall(r'./test_meta_data')
    files.close()
    #檢查路徑是否存在
    if  os.path.exists("test_meta_data"):
        src = "test_meta_data/chromedriver-win64/chromedriver.exe"
        dst = "chromedriver.exe"
        shutil.copyfile(src, dst)
    else:
        print("不存在路徑")
    #開始刪除文件
    shutil.rmtree("test_meta_data")
    os.remove("test_meta_data.zip")




if __name__ == "__main__":
    #下載檔案
    print("測試===>",get_chromedriver_website.get_stable_chromedriver_website())
    download_url_2 = "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.155/win64/chromedriver-win64.zip"
    response_2 = requests.get(download_url_2)
    with open('test.zip', 'wb') as file_2:
        file_2.write(response_2.content)
        file_2.close()
    #解壓縮文件
    files_2 = zipfile.ZipFile("test.zip")
    files_2.extractall(r'./test')
    files_2.close()
    #檢查路徑是否存在
    if  os.path.exists("test"):
        SRC_2 = "test/chromedriver-win64/chromedriver.exe"
        DST_2 = "chromedriver.exe"
        shutil.copyfile(SRC_2, DST_2)
    else:
        print("不存在路徑")
    #開始刪除文件
    shutil.rmtree("test")
    os.remove("test.zip")



     
