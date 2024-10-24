"""
用來安裝All Service Type的腳本
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

def all_service_type_app_install(app_name:str="SQL Server", have_cluster_type_flag:bool=False, only_one_flag:bool=False) -> None:
    """安裝所有Service Type的App

    Args:
        app_name (str, optional): 要安裝的App名稱. Defaults to "SQL Server"
        have_cluster_type_flag (bool, optional): 是否有Cluster Type. Defaults to False.
        only_one_flag: (bool, optional): 該App是否在叢集中,只能存在一個. Defaults to False.
    """
    set_app_name = str(app_name)
    set_namespace = "test-for-balancer"
    set_service_type = 'LoadBalancer'
    set_suf = "balancer"
    set_command = "python auto_app_install.py --app_name \"" + set_app_name +  "\" --name_space "+ set_namespace +" --suf \" " + set_suf + "\" --service_type \""+ set_service_type +"\""
    print("set_command =",set_command)
    #os.system(set_command)
    balancer_ =  threading.Thread(target = os_command, args = (set_command,))
    balancer_.start()
    if not only_one_flag:   
        set_namespace = "test-for-node"
        set_service_type = 'NodePort'
        set_suf = "node"
        set_command = "python auto_app_install.py --app_name \"" + set_app_name +  "\" --name_space "+ set_namespace +" --suf \" " + set_suf + "\" --service_type \""+ set_service_type +"\""
        print("set_command =",set_command)
        #os.system(set_command)
        node_ =  threading.Thread(target = os_command, args = (set_command,))
        node_.start()
        
        if have_cluster_type_flag:
            set_namespace = "test-for-cluster"
            set_service_type = 'ClusterIP'
            set_suf = "cluster"
            set_command = "python auto_app_install.py --app_name \"" + set_app_name +  "\" --name_space "+ set_namespace +" --suf \" " + set_suf + "\" --service_type \""+ set_service_type +"\""
            print("set_command =",set_command)
            #os.system(set_command)
            cluster_ =  threading.Thread(target = os_command, args = (set_command,))
            cluster_.start()


if __name__ == "__main__":
    service_type_list = ['LoadBalancer','NodePort','ClusterIP']
    #all_service_type_app_install("Redmine")
    #all_service_type_app_install(have_cluster_type_flag=True)
