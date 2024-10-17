"""
用來安裝長時間測試App的腳本
"""
import sys
import os
import configparser

#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))


#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
Node_ip = cf.get("Cluster_Info","Node_ip")
IP_START = cf.get("Cluster_Info","Avaible_IP_Start")
IP_END = cf.get("Cluster_Info","Avaible_IP_End")


if __name__ == "__main__":
    set_app_name = "Redmine"
    set_command = "python auto_app_install.py --app_name " + set_app_name
    os.system(set_command)
    
    set_app_name = "SQL Server"
    set_command = "python auto_app_install.py --app_name " + set_app_name
    os.system(set_command)
    
    set_app_name = "PostgreSQL"
    set_command = "python auto_app_install.py --app_name " + set_app_name
    os.system(set_command)
