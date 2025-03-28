"""
用來獲取可以使用的Load Balancer IP     
"""
import sys
import os
import configparser
import datetime
import paramiko
import logging_config
from paramiko import SSHException
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

def get_kubectl_ip(connect_ip:str='172.24.128.111') -> list:
    """_summary_
    用來獲取k8s底層所使用的IP
    Args:
        Connect_ip (str, optional): 請輸入要連線的機器. Defaults to '172.24.128.111'.

    Returns:
        list: 從該主機獲得的k8s IP
    """
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname='HOST_NAME', username="USER_NAME", password="PASSWORD")
    ssh.connect(hostname=connect_ip, username="root", password="ABcd_1234",timeout=1)

    #stdin, stdout, stderr = ssh.exec_command('ls -l')
    stdin, stdout, stderr = ssh.exec_command('kubectl get service --all-namespaces | awk \'{print $5}\' | grep -v "none"')
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

def get_available_cluster_ip(will_set_ip:str="172.24.128.170") -> str:
    """輸入一個想要設定的IP,如果該IP可以使用,會返回該IP,如果不可以使用,會返回一個可以使用的IP

    Args:
        will_set_ip (str, optional): 輸入一個想要設定的IP. Defaults to "172.24.128.170".

    Returns:
        str: 確定可以使用的IP
    """
    check_ip = will_set_ip.replace(" ","")

    #所有可用的IP
    temp_ip_list = []
    #真正可以使用的IP
    available_ip_list = []

    #獲取所有可用的IP
    get_start_ip = IP_START.replace(" ","").split(".")
    get_range = int(IP_END.replace(" ","").split(".")[3]) - int(get_start_ip[3]) + 1
    for i in range(get_range):
        temp_ip_list.append(str(get_start_ip[0] + "." + get_start_ip[1] + "." + get_start_ip[2] + "." + str(int(get_start_ip[3]) + i)))
    #print('temp_ip_list =',temp_ip_list)
    #print("Node_ip=",Node_ip.replace(" ",""),type(Node_ip))

    #從ini文件中獲取所有可以連線到Node底層的IP
    node_list = NODE_IP.replace(" ","").split(",")
    get_cluster_used_ip =[]
    for node_ip in node_list:
        #print("node_ip=",node_ip)
        try:
            get_cluster_used_ip = get_kubectl_ip(node_ip)
            #print("get_cluster_used_ip =",get_cluster_used_ip)
            break
        except TimeoutError:
            logging_config.info(f"Node Connect {node_ip} Fail(TimeoutError)")
        except SSHException:
            logging_config.info(f"Node Connect {node_ip} Fail(SSHException)")
    else:
        logging_config.critical("All node ip can not connect ")
        logging_config.critical("======node_list-Start======== ")
        for node_ip in node_list:
            logging_config.critical(f"=={node_ip}==")
        logging_config.critical("======node_list-End======== ")
        return None

    for get_available_ip in temp_ip_list:
        for used_ip in get_cluster_used_ip:
            if used_ip == get_available_ip:
                break
        else:
            available_ip_list.append(get_available_ip)
    if len(available_ip_list) < 1:
        return None
    get_check_ip = check_ip.replace(" ","")
    for item in available_ip_list:
        if item == get_check_ip:
            return item
    else:
        return available_ip_list[0]


if __name__ == "__main__":
    print(get_available_cluster_ip("172.24.120.121"))
