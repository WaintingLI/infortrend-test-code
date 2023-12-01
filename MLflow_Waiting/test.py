import os, sys
import logging
import configparser



print(os.getcwd())  #顯示當前路徑
print(sys.argv[0])  #顯示所執行的Python檔路徑

#切換命令提示字元到Python檔案所在的目錄
ab_path_2 = os.path.dirname(sys.argv[0])
print("ab_path_2 = ",ab_path_2)
os.chdir(os.path.dirname(sys.argv[0]))
print(os.getcwd())

#讀取檔案參數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
MLFLOW_IP=cf.get("APP_Info","Mlflow_ip")
DEBUG_MODE = cf.getboolean("APP_Info","Debug_mode")
print("DEBUG_MODE = ",DEBUG_MODE,", type of DEBUG_MODE = ",type(DEBUG_MODE))

