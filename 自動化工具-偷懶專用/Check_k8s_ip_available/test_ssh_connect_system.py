import os
import paramiko 
import datetime


def Get_kubectl_ip(Connect_ip:str='172.24.128.111',Ip_mask:str='172.24.128') -> list:
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
    ssh.connect(hostname=Connect_ip, username="root", password="admin")
    
    #stdin, stdout, stderr = ssh.exec_command('ls -l')
    #stdin, stdout, stderr = ssh.exec_command('timeout 10s tcpdump -c 100  -i trunk_6_ dst 172.24.128.140 and dst port 3306')
    stdin, stdout, stderr = ssh.exec_command('kubectl get service --all-namespaces | grep "' + f"{Ip_mask}"  +'"  | awk \'{print $5}\'')
    #stdin, stdout, stderr = ssh.exec_command('kubectl get service --all-namespaces | grep "172.24.128."  | awk \'{print $5}\'')
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
    '''
    print('==========================')
    for i in get_data:
        print(ord(i),end=' ')
    print('==========================')
    
    for i,item in enumerate(get_datas):
        print(i,'=>',item)
    for item in get_datas:
        if item == '172.24.128.140':
            print("找到",item)
        else:
            print("Nothing")
    '''

    ssh.close()
    return get_datas
    
    
    
    


if __name__ == '__main__':
    Get_kubectl_ip('172.24.128.111')
