'''
用來當作瀏覽器的範本
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
import requests



#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))







if __name__ == "__main__":
    file_path = "add_watcher.txt"
    if not os.path.isfile(file_path):
        print(file_path,"is not found")
        #return
    print("PASS")
    with open(file_path,"r",encoding="utf-8") as f:
                
        meta_data = f.readlines()
        for watcher in meta_data:
            print(watcher)
            ascii_values = []
            for character in watcher.rstrip("\n"):
                ascii_values.append(hex(ord(character)))
            print(ascii_values)
                #[87, 97, 121, 110, 101, 32, 67, 104, 111, 117, 10]
                #[87, 97, 121, 110, 101, 32, 67, 104, 111, 117]
            
    