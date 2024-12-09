"""使用OpenAI用來測試LocalAI
※測試結果:
base_url => 填寫LocalAI的網路位置
model => 填寫Mode名稱
"""
#from time import sleep
import sys
import os
import configparser
from openai import OpenAI



#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
LOCALAI_IP = cf.get("LocalAI_Info","LocalAI_ip")
MODULE_NAME = cf.get("LocalAI_Info","Module_name")
SEND_GET_COUNTER = cf.getint("LocalAI_Info","Communication_counter")

# ...
# Send the conversation and available functions to GPT
#messages = [{"role": "user", "content": "What is the weather like in Beijing now?"}]
messages = [{"role": "user", "content": "說中文"}]
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Return the temperature of the specified region specified by the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "User specified region",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "temperature unit"
                    },
                },
                "required": ["location"],
            },
        },
    }
]

client = OpenAI(
    # This is the default and can be omitted
    api_key="test",
    base_url= LOCALAI_IP + "/v1/"
)

'''
response =client.chat.completions.create(
    messages=messages,
    tools=tools,
    tool_choice ="auto",
    model="meta-llama-3.1-8b-instruct",
)
'''
response =client.chat.completions.create(
    messages=messages,
    model=MODULE_NAME
)

if __name__ == "__main__":
    #問題發送次數
    quest_counter = SEND_GET_COUNTER

    while True:
        quest_counter = quest_counter - 1
        #print("輸入文字:")
        #get_string = input()
        get_string = "你好"
        #sleep(1)
        messages[0]['content'] = get_string
        response =client.chat.completions.create(
            messages=messages,
            model="meta-llama-3.1-8b-instruct"
        )
        print(response.choices[0].message.content,";","呼叫次數剩餘:",quest_counter," 次")

        if quest_counter <= 0:
            break
