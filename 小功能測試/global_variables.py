'''
用來放全域變數
'''
import configparser

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
CHATWOOT_IP = cf.get("APP_Info","OpenCart_ip")
def initialize():
    global num
    global CHATWOOT_IP
    num = 1


if __name__ == "__main__":
    print("test")
