"""
測試Nextcloud 上傳功能
使用lib
nc_py_api
"""
import sys
#import traceback
import random
import os
import configparser
from io import BytesIO
import nc_py_api


#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
NEXTCLOUD_IP = cf.get("Nextcloud_Info","Nextcloud_ip")
ADMIN = cf.get("Nextcloud_Info","Admin_account")
ADMIN_PASSWORD = cf.get("Nextcloud_Info","Admin_password")
DATA_SIZE = cf.getint("Nextcloud_Info","Datasize")


#使用亂數來創造名字
def create_random_name() -> str:
    """創造隨機名稱
    Returns:
        str: 8個包含數字或小寫字母的名稱
    """
    string_nuber = 8
    print_string = ""
    return_name = ""
    get_str_list = random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',string_nuber)
    for number in range(string_nuber):
        print_string = print_string + get_str_list[number]
    return_name = print_string
    return return_name

if __name__ == "__main__":
    nc_py_api.options.NPA_NC_CERT = False #關閉檢查Https憑證
    #登入Nextcloud
    nc = nc_py_api.Nextcloud(nextcloud_url=NEXTCLOUD_IP,
                             nc_auth_user=ADMIN,
                             nc_auth_pass=ADMIN_PASSWORD)
    data_buf = BytesIO()

    data_buf.seek(DATA_SIZE - 1)
    data_buf.write(b"\0")
    data_buf.seek(0)
    upload_file_name = create_random_name()
    nc.files.upload_stream( upload_file_name +".test", data_buf)
    #列出所有路徑檔案

    result = nc.files.find(["eq", "name", upload_file_name +".test"])
    if result:
        for i in result:
            print(i)
    else:
        print("Nothing")
        print("Can't find the file =>",upload_file_name,".test")
        sys.exit(1)
