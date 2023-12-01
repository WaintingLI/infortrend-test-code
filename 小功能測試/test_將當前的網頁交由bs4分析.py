'''
將當前的網頁交由Bs4來分析
'''
from bs4 import BeautifulSoup
import requests


if __name__ == "__main__":
    #response = requests.get(driver.current_url)
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
    