"""測試Vault用
"""

# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

import sys
import os
import configparser
import hvac



#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
VAULT_IP = cf.get("Vault_Info","Vault_ip")
ROOT_TOKEN = cf.get("Vault_Info","Root_token")
SECRET_ENGINE = cf.get("Vault_Info","Sectret_engine")



if __name__ == "__main__":
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
