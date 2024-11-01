"""
用來獲取可以使用的Load Balancer IP     
"""
import sys
import os
import configparser
import datetime
import paramiko
import logging_config
import string_2_ascii
from paramiko.ssh_exception import SSHException

#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))


#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
NODE_IP = cf.get("Cluster_Info","Node_ip")
IP_START = cf.get("Cluster_Info","Avaible_IP_Start")
IP_END = cf.get("Cluster_Info","Avaible_IP_End")

def connect_kubectl_ip(connect_ip:str='172.24.128.111',set_command:str='kubectl get service -n test-for-long-1') -> list:
    """透過底層來獲取相對於Command的資料

    Args:
        connect_ip (str, optional): 要連線的機器底層IP. Defaults to '172.24.128.111'.
        set_command (str, optional): 要傳送的命令. Defaults to 'kubectl get service -n test-for-long-1'.

    Returns:
        list: 回傳獲得的命令
    """
    SSH_USERNAME = "root"
    SSH_PASSWORD = "ABcd_1234"
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname='HOST_NAME', username="USER_NAME", password="PASSWORD")
    ssh.connect(hostname=connect_ip, username=SSH_USERNAME, password=SSH_PASSWORD,timeout=1)

    #stdin, stdout, stderr = ssh.exec_command('ls -l')
    #stdin, stdout, stderr = ssh.exec_command('kubectl get service --all-namespaces | grep "172.24.128."  | awk \'{print $5}\'')
    #stdin, stdout, stderr = ssh.exec_command('kubectl get service -n test-for-long-1')
    stdin, stdout, stderr = ssh.exec_command(set_command)
    #sftp = ssh.open_sftp()
    #localpath = 'srcFile.txt'
    #remotepath = '/folder/srcFile.txt'
    #sftp.get(remotepath,localpath)

    #sftp.close()
    #print("stdin= \n",stdin.read())
    #print("===================================")
    #print("stdout= \n",str(stdout.read(), encoding='utf-8'))
    get_data = str(stdout.read(), encoding='utf-8')
    #print(get_data)
    get_datas = get_data.split('\n')

    ssh.close()
    return get_datas

def all_node_to_connect_k8s(dilver_command:str='kubectl get service -n test-for-long-1') -> list:
    """會嘗試連線底層的Node,如果那台Node無法連線,會連下到另一台,直到所有Node都連線完

    Args:
        dilver_command (str, optional): 要傳送的命令. Defaults to 'kubectl get service -n test-for-long-1'.

    Returns:
        list: 獲得的資料
    """

    #從ini文件中獲取所有可以連線到Node底層的IP
    node_list = NODE_IP.replace(" ","").split(",")
    get_terminal_data =[]
    for node_ip in node_list:
        #print("node_ip=",node_ip)
        try:
            logging_config.debug(f" connect node_ip ={node_ip}")
            get_terminal_data = connect_kubectl_ip(node_ip,dilver_command)
            #print("get_cluster_used_ip =",get_cluster_used_ip)
            break
        except TimeoutError:
            logging_config.info(f"Node Connect {node_ip} Fail(TimeoutError)(com)")
        except SSHException:
            logging_config.info(f"Node Connect {node_ip} Fail(SSHException)(com)")
    else:
        logging_config.critical("All node ip can not connect ")
        logging_config.critical("======node_list-Start======== ")
        for node_ip in node_list:
            logging_config.critical(f"=={node_ip}==")
        logging_config.critical("======node_list-End======== ")
        return None
    return get_terminal_data

def get_app_ip_data(app_name:str="sqlserver",app_at_namespace:str="test-for-long-1"):
    
    #獲得該Name Space 下的所有App資料(未整理)
    transfer_command = "kubectl get service -n " + app_at_namespace
    get_meta_data = all_node_to_connect_k8s(transfer_command)
    if get_meta_data == None:
        return None
    #將資料整理為2x2陣列形式(已移除所有空格)
    data_array = []
    for meta in get_meta_data:
        #防止沒有資料
        if meta == "":
            continue
        meta_alpha_list = meta.split("  ")
        meta_array =[]
        for meta_meta in meta_alpha_list:
            get_str = meta_meta.replace("  ","")
            if get_str != "":
                meta_array.append(get_str)
        data_array.append(meta_array)

    #獲取相對應的App Ip
    #'NAME', ' TYPE', ' CLUSTER-IP', 'EXTERNAL-IP', 'PORT(S)', 'AGE'
    #master_node_ip_command = "docker exec -ti rc kubectl cluster-info | grep \"Kubernetes control plane\""
    master_node_ip_command = "docker exec rc kubectl cluster-info | grep \"Kubernetes control plane\""
    get_str_data = all_node_to_connect_k8s(master_node_ip_command)

    #return data_array
    #get_master_node_ip = get_str_data[]
    print("get_master_node_ip =",get_str_data)
    for item_2 in get_str_data:
        if item_2 == "":
            continue
        print("item_2=",str(item_2)[str(item_2).find("https://"):str(item_2).rfind(":")])
    return get_str_data
            

if __name__ == "__main__":
    command = "kubectl get storageclass"
    get_list = all_node_to_connect_k8s(command)
    for item in get_list:
        if str(item).find("(default)") > 0:
            print(item[0:str(item).find("(default)")])
            string_2_ascii.string_to_hex(item[0:str(item).find("(default)")].replace(" ",""))
