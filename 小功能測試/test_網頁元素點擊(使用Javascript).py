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




def click_button(a):
    '''
    點擊按鈕
    
    Args:
     - a = WebDriver物件
    Example:
     click_button(driver.find_element(By.CSS_SELECTOR,"button#button-payment-methods"))
    '''
    element = a
    #需要增加sleep，來防止StaleElementReferenceException: Message: stale element reference: element is not attached to the page document錯誤
    sleep(2)
    #藉由WebDriverWait來判斷該元素是否可以點擊，如果可以，將會獲得該元素的值 (尚未實驗)
    element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "code")))
    #透過Java Script來進行螢幕滾動到element的位置
    driver.execute_script("arguments[0].scrollIntoView();", element)
    #透過Java Script來進行, element位置的點擊
    driver.execute_script("arguments[0].click();",element)


def check_element(driver,element,sec):
    '''
    check_element(driver,element=(By.LINK_TEXT,("Content")),sec=15)
    '''
    try:
        WebDriverWait(driver,int(sec)).until(EC.visibility_of_element_located(element))
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.close()
        driver.quit()
        sys.exit(1)
