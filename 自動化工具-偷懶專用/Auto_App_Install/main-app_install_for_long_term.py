"""
用來安裝長時間測試App的腳本
"""
import sys
import os
import configparser
import threading

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

#子執行續
def os_command(input:str="echo hellow world") -> None:
    """僅僅用來執行cmd

    Args:
        input (str, optional): 輸入cmd指令. Defaults to "hellow world".
    """
    os.system(str(input))

if __name__ == "__main__":
    threading_seed = []
    set_app_name = "SQL Server"
    set_command = "python auto_app_install.py --app_name \"" + set_app_name +  "\" --name_space test-for-long-1 --suf \"\" "
    print("set_command =",set_command)
    #os.system(set_command)
    threading_seed.append(threading.Thread(target = os_command, args = (set_command,)))
    threading_seed[len(threading_seed) - 1].start()

    set_app_name = "Jenkins"
    set_command = "python auto_app_install.py --app_name \"" + set_app_name +  "\" --name_space test-for-jenkins --suf \"\" "
    print("set_command =",set_command)
    #os.system(set_command)
    #jenkins_test =  threading.Thread(target = os_command, args = (set_command,))
    #jenkins_test.start()
    threading_seed.append(threading.Thread(target = os_command, args = (set_command,)))
    threading_seed[len(threading_seed) - 1].start()

    set_app_name = "Redmine"
    set_command = "python auto_app_install.py --app_name " + set_app_name + " --name_space test-for-long-3 --suf \"\" "
    #os.system(set_command)
    #redmine_test =  threading.Thread(target = os_command, args = (set_command,))
    #redmine_test.start()
    threading_seed[len(threading_seed) - 1].join()
    threading_seed.append(threading.Thread(target = os_command, args = (set_command,)))
    threading_seed[len(threading_seed) - 1].start()

    set_app_name = "PostgreSQL"
    set_command = "python auto_app_install.py --app_name " + set_app_name + " --name_space test-for-long-2 --suf \"\" "
    #os.system(set_command)
    #postgresql_test =  threading.Thread(target = os_command, args = (set_command,))
    #postgresql_test.start()
    threading_seed.append(threading.Thread(target = os_command, args = (set_command,)))
    threading_seed[len(threading_seed) - 1].start()
