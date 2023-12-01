'''
這是一份用來測試ML Flow的是自動測試文件,透過Chrome來驗證
'''

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
import win32clipboard
import logging
import configparser
import requests
from bs4 import BeautifulSoup


print(requests.__file__)

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
MLFLOW_IP=cf.get("APP_Info","Mlflow_ip")
DEBUG_MODE = cf.getboolean("APP_Info","Debug_mode")

#設定Chrome driver 的相關屬性
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument("--disable-gpu")
options.add_argument('ignore-certificate-errors')
options.add_argument('disable-application-cache')
options.add_argument('window-size=1600x900')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
#driver_location='/usr/bin/chromedriver'
#binary_location='/usr/bin/google-chrome'
#options.binary_location=binary_location
#driver=webdriver.Chrome(executable_path=driver_location,chrome_options=options)
#js="window.open('{}','_blank');"
service = Service(executable_path="C:\\Users\\waiting.lee\\Desktop\\Auto Tools\\chromedriver.exe")


#啟動chrome

driver = webdriver.Chrome(service=service, options=options)

def check_element(driver,element,sec):
    WebDriverWait(driver,int(sec)).until(EC.visibility_of_element_located(element))

    
#BeautifulSoup與requests相關屬性
url ='https://tw.news.yahoo.com/'
html = requests.get(url)
html.encoding = 'UTF-8'

if __name__ == "__main__":
    if 1:
        driver.get("http://172.24.128.183:5000/")
        #方法一 element = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[3]/span[4]/span/div/a")
        #方法二
        element = driver.find_element(By.LINK_TEXT, "default_2")
        #<a href="#/experiments/2" style="width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">default_2</a>
        element.click()
        sleep(5)
        element = driver.find_element(By.LINK_TEXT,"righteous-wren-936")
        #<a href="#/experiments/2/runs/97eebc61c629405f9bf626f2f8dfd0fa">righteous-wren-936</a>
        element.click()
        sleep(5)
        element = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div[1]/div/div[2]/div/div[4]/div[6]/div[3]")
        print(element.text)
        print(driver.current_url)
        
        #BeautifulSoup與requests相關屬性
        #url = driver.current_url
        url = "http://172.24.128.183:5000/#/experiments/2/runs/97eebc61c629405f9bf626f2f8dfd0fa"
        #url ='https://tw.news.yahoo.com/'
        html = requests.get(url)
        html.encoding = 'UTF-8'
        soup = BeautifulSoup(html.text, "lxml")
        sp = BeautifulSoup(html.text, 'html5lib')
        print(sp.title)
        print(sp.div)
        print(html)
        print(soup)
        #<div class="css-1anymhr"><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">Run ID</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content">97eebc61c629405f9bf626f2f8dfd0fa</div></div><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">Date</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content">2023-09-01 17:21:46</div></div><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">Source</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content"><div style="display: flex; align-items: center;"><img alt="Local Source Icon" title="Local Source" src="static-files/static/media/laptop.f3a6b3016fbf319305f629fcbcf937a9.svg" style="height: 20px; margin-right: 4px;">ml.py</div></div></div><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">User</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content"><a href="#/experiments/2?searchFilter=user_id%20%3D%20'Waiting.Lee'">Waiting.Lee</a></div></div><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">Duration</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content">58.0s</div></div><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">Status</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content">FAILED</div></div><div data-test-id="descriptions-item" class="css-1p4cmd6"><div data-test-id="descriptions-item-label" class="css-1bmnxg7"><span class="du-bois-light-typography css-6x034l">Lifecycle Stage</span></div><div data-test-id="descriptions-item-colon" class="css-ttjnck"><span class="du-bois-light-typography css-6x034l">:</span></div><div data-test-id="descriptions-item-content"><a href="#/experiments/2?lifecycleFilter=Active">active</a></div></div></div>
        for a in sp.find_all('div','css-1anymhr'):
            print(a)
        #<div data-test-id="descriptions-item-content">FAILED</div>
        
    else:
        driver.get("http://www.google.com.tw/")
        element = driver.find_element(By.CLASS_NAME, "gLFyf")
        element.send_keys("Selenium Python")
    
    #sleep(60)
