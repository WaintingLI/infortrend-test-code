"""測試Vault用
"""

# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0
import sys
import os
import configparser
from argparse import ArgumentParser
import hvac
import communicate_to_machine




#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
VAULT_IP = cf.get("Vault_Info","Vault_ip")
ROOT_TOKEN = cf.get("Vault_Info","Root_token")
SECRET_ENGINE = cf.get("Vault_Info","Sectret_engine",fallback="hvac-kv")

def create_args():
    '''
    創造Argument,對於使用命令列來說,創造相對應的參數,如果沒有輸入參數,那就全部採取預設值
    '''
    parser = ArgumentParser(description="Vault Host example")
    parser.add_argument(
        "--ip",
        default="172.24.128.213",
        metavar='xxx.xxx.xxx.xxx',
        dest="ip",
        help="Vault Server ipv4 (default: \"172.24.128.213\")",)

    parser.add_argument(
        "--port",
        default="8200",
        metavar='xxxx',
        dest="port",
        help="Vault Server port number (default: \"8200\")",)

    parser.add_argument(
        "--app_name",
        default="None",
        metavar='vault',
        dest="app_name",
        help="Vault name (default: \"None\")",)

    parser.add_argument(
        "--app_name_space",
        default="test-for-app-01",
        metavar='test-for-app-01',
        dest="app_name_space",
        help="Vault Name Space (default: \"None\")",)

    args_para = parser.parse_args()
    return args_para


if __name__ == "__main__":
    args = create_args()
    #整理輸入的資料
    VAULT_IP = "http://" + args.ip.replace(" ","") + ":" + args.port.replace(" ","") +"/"
    if args.app_name_space == "None" or args.app_name == "None":
        print("沒有同時輸入app_name與app_name_space資料,結束Vault 測試")
        sys.exit(1)

    #獲取Root Token
    ROOT_TOKEN = communicate_to_machine.get_vault_root_token(args.app_name, args.app_name_space)
    print("ROOT TOKEN =",ROOT_TOKEN)
    if not ROOT_TOKEN:
        print("沒有獲取ROOT_TOKEN,檢查App名稱或者Name Space是否有誤")
        sys.exit(1)
    # 設定要連線的Vault相關資料
    client = hvac.Client(
        url=VAULT_IP,
        token=ROOT_TOKEN,
        verify=False,
        allow_redirects=True
    )
    #會創造一個sercet 等同於 vault secrets enable -path=hvac-kv kv
    #可以參考"https://hvac.readthedocs.io/en/stable/usage/system_backend/mount.html"
    try:
        client.sys.enable_secrets_engine(
            backend_type='kv',
            path=SECRET_ENGINE,
        )
    except hvac.exceptions.InvalidRequest as e:
        if str(e).find("path is already in use") >= 0:
            print(SECRET_ENGINE,"已經有建立")
        else:
            print("錯誤訊息",e)
    except hvac.exceptions.Forbidden as e:
        print("Root Token Error")
    #這個可以讀取
    #print(client.read(path='secret/webapp/config', wrap_ttl=None))

    #在上面創建的Secrets_engine底下,寫入資料,如果該dict已經有數值,則會被覆蓋資料
    client.write_data(path=SECRET_ENGINE+"/webapp",
                      data=dict(password='Hashi1234', username="static-user"),wrap_ttl=None)

    #讀取資料
    #回讀資料格式=>{'request_id': 'd5c48fc6-6a4b-cf2a-261a-ce0b3ddd26c9',
    # 'lease_id': '', 'renewable': False, 'lease_duration': 2764800,
    # 'data': {'password': 'Hashi1234', 'username': 'static-user'},
    # 'wrap_info': None, 'warnings': None, 'auth': None}
    read_datas = client.read(path= SECRET_ENGINE +'/webapp', wrap_ttl=None)

    #print(client.read(path='hvac-kv/webapp', wrap_ttl=None))
    #print("read_datas = ",type(read_datas))
    #print(read_datas)
    #print(read_datas["data"]["password"])

    #比對寫入與讀取資料是否一致
    if read_datas["data"]["password"] == 'Hashi1234':
        print("PASS")
    else:
        print("False")
        sys.exit(1)
