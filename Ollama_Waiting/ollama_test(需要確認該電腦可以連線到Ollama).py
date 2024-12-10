"""使用Ollama來讀取
※測試結果:
host => 填寫Ollama的網路位置
model => 填寫Mode名稱
使用curl http://172.24.128.222:11434/api/tags來測試是否可以連Ollama,其中"172.24.128.222:11434"代表IP與對接口
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
'''
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
LOCALAI_IP = cf.get("LocalAI_Info","LocalAI_ip")
MODULE_NAME = cf.get("LocalAI_Info","Module_name")
SEND_GET_COUNTER = cf.getint("LocalAI_Info","Communication_counter")
'''


if __name__ == "__main__":
    #client = Client(host = 'http://172.24.128.222:11434/')
    client = ollama.Client(
        host='http://172.24.128.222:11434',
        headers={'x-some-header': 'some-value'},
        timeout=120000.0)
    #print(client.list())
    response = client.chat(model='mistral:7b', messages=[
    {
    'role': 'user',
    'content': 'Why is the sky blue?',
    },
    ])
    print("response =",response['message']['content'])
    '''
    response = client.chat(
        model='llama3.2',
        messages=[{'role': 'user','content': 'Why is the sky blue?'}]
        )
    '''

