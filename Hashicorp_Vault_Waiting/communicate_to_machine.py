"""
用來獲取可以使用的Load Balancer IP     
"""
import sys
import os
import configparser
import paramiko
from paramiko.ssh_exception import SSHException

#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))


#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
NODE_IP = cf.get("Cluster_Info","Node_ip")


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
    #date = datetime.datetime.now().strftime("%Y-%m-%d")

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
            get_terminal_data = connect_kubectl_ip(node_ip,dilver_command)
            #print("get_cluster_used_ip =",get_cluster_used_ip)
            break
        except TimeoutError:
            print(f"Node Connect {node_ip} Fail(TimeoutError)(com)")
        except SSHException:
            print(f"Node Connect {node_ip} Fail(SSHException)(com)")
    else:
        print("All node ip can not connect ")
        print("======node_list-Start======== ")
        for node_ip in node_list:
            print(f"=={node_ip}==")
        print("======node_list-End======== ")
        return None
    return get_terminal_data

def get_app_ip_data(app_name:str="sqlserver",app_at_namespace:str="test-for-long-1"):
    """獲取該App的ip資訊

    Args:
        app_name (str, optional): app名稱. Defaults to "sqlserver".
        app_at_namespace (str, optional): app所在Name Space. Defaults to "test-for-long-1".

    Returns:
        str: 所讀取的資料
    """
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

def check_app_deployed(app_name:str="sqlserver",app_namespace:str="test-for-app-1") -> bool:
    """確認App是否已經安裝,主要是用來防範自動化安裝App時,遇到App沒有成功安裝的問題
    Args:
        app_name (str, optional): 安裝App的名稱. Defaults to "sqlserver".
        app_namespace (str, optional): 安裝App的Name Space. Defaults to "test-for-app-1".

    Returns:
        bool: True代表有安裝;False代表沒有
    """
    sned_command = "helm list --deployed -n " + \
                    str(app_namespace) + " | grep \"" + str(app_name) + "\""
    get_answer = all_node_to_connect_k8s(sned_command)
    #print("get_answer =",get_answer,type(get_answer))
    if not get_answer or get_answer == ['']:
        return False
    else:
        return True

def get_vault_root_token(app_name:str="vault",app_namespace:str="test-for-app-1") -> str| None:
    """用來找尋Vault的 root token
    Args:
        app_name (str, optional): 輸入vault安裝時所設定的名稱. Defaults to "vault".
        app_namespace (str, optional): Vault所在的Name Space. Defaults to "test-for-app-1".

    Returns:
        str| None: 找尋到的root Token,沒有找到折返回None
    """
    #kubectl get configmap -n test-for-app-test vault-n-keys-configmap -o yaml | grep root_token
    sned_command = "kubectl get configmap -n " + str(app_namespace) + " " + str(app_name).replace(" ","") + "-keys-configmap -o yaml | grep root_token"
    #print("sned_command=",sned_command)
    get_answer = all_node_to_connect_k8s(sned_command)
    #print("get_answer =",get_answer,type(get_answer))
    if not get_answer or get_answer == ['']:
        return None
    else:
        for item in get_answer:
            if item:
                get_str = str(item).replace(" ","")
                #print(get_str)
                if get_str.find("root_token") >= 0:
                    #會顯示"root_token":""
                    return get_str[get_str.find("root_token")+13:len(get_str)-1]
        return None


if __name__ == "__main__":
    #print(check_app_deployed("vault-n","test-for-app-test"))
    #kubectl get configmap -n test-for-app-test vault-n-keys-configmap -o yaml | grep root_token
    if  get_vault_root_token("vault-n","test-for-app-test"):
        print("pass")
    else:
        print("Nothing")
    sys.exit(0)
