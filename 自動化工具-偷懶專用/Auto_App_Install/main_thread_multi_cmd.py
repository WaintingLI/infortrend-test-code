"""
測試用
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
    print("###Command### => ",input)
    os.system(str(input))

if __name__ == "__main__":
    threading_seed = []
    try:
        while True:
            set_command = input("CMD:")
            threading_seed.append(threading.Thread(target = os_command, args = (set_command,)))
            threading_seed[len(threading_seed) - 1].start()
    except KeyboardInterrupt:
        print("END PROCEDURE")
