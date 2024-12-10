"""
透過Open Webui來讀取Ollama
"""
#from time import sleep
import sys
import os
import configparser
import ollama
from ollama import chat
from ollama import ChatResponse
from ollama import Client



#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
OLLAMA_WEBUI_IP = cf.get("Ollama_Info","Ollama_webui_ip")
MODULE_NAME = cf.get("Ollama_Info","Module_name")
WEBUI_API_KEY = cf.get("Ollama_Info","Ollama_webui_API_KEY")
SEND_GET_COUNTER = cf.getint("Ollama_Info","Communication_counter")



if __name__ == "__main__":
    """成功範例:
    client = ollama.Client(
        host='http://172.24.128.216:8080/ollama',
        headers={'Authorization': 'Bearer sk-4c621e3028f342d4850bdfc792d6931a'},
        timeout=120000.0)
    #print(client.list())
    response = client.chat(model='mistral:7b', messages=[
    {
    'role': 'user',
    'content': '說中文',
    },
    ])
    print("response =",response['message']['content'])
    """
    #設定ollama參數
    ollama_ip = OLLAMA_WEBUI_IP + "ollama"
    header_auth = "Bearer " + WEBUI_API_KEY
    quest_counter = SEND_GET_COUNTER
    client = ollama.Client(
        host=ollama_ip,
        headers={'Authorization': header_auth},
        timeout=120000.0)
    #print(client.list())
    while True:
        quest_counter = quest_counter - 1
        response = client.chat(model=MODULE_NAME, messages=[
        {
        'role': 'user',
        'content': '你好,說一句話就好了',
        },
        ])
        print(response['message']['content'],"對話剩餘次數:",quest_counter," 次")

        if quest_counter <= 0:
            break
