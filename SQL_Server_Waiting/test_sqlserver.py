"""
測試SQL Server是否安裝正常
"""
import configparser
import sys
import traceback
import os
import random
from argparse import ArgumentParser
import pymssql

#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
USER = cf.get("SQLserver_Info","User")
USER_PASSWORD = cf.get("SQLserver_Info","Password")

def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="SQLserver Example")
    parser.add_argument(
        "--ip",
        type=str,
        default="172.24.128.212",
        metavar="N",
        help="input ipv4",
    )
    parser.add_argument(
        "--port",
        type=str,
        default="1433",
        metavar="N",
        help="input ip port",
    )
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments

def create_database_name(base_name:str="test") -> str:
    """自動創建Database 的名稱

    Args:
        base_name (str, optional): 創建Database名稱時. Defaults to "test".

    Returns:
        str: 亂數創造的名稱
    """
    #使用亂數來創造名字
    string_nuber = 8
    print_string = ""
    return_database_name =""
    get_str_list = random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',string_nuber)
    for number in range(string_nuber):
        print_string = print_string + get_str_list[number]
        return_database_name = base_name+print_string
    return return_database_name


if __name__ == "__main__":
    args = create_args()
    #print(args.ip)
    #print(args.port)
    conn = pymssql.connect(
        server=args.ip + ":" + args.port,
        user=USER,
        password=USER_PASSWORD,
        #database='msdb',
        autocommit= True,
        as_dict=True
    )

    #創造移除旗標
    CREATE_DROP_FLAG = False
    #創造Database:
    while not CREATE_DROP_FLAG:
        DATABASE_NAME = create_database_name()
        SQL_QUERY = "CREATE DATABASE " + DATABASE_NAME + ";"
        cursor = conn.cursor()
        #conn.autocommit = True
        try:
            cursor.execute(SQL_QUERY)
            print("創建資料庫")
            CREATE_DROP_FLAG = True
        except pymssql._pymssql.OperationalError as e:
            #跟沒有加Try...exception 的訊息一樣
            traceback.print_exc()

    #檢查資料庫是否有被創建出來
    cursor.execute("SELECT name, database_id, create_date FROM sys.databases;")
    records = cursor.fetchall()
    for item in records:
        #print(item['name'])
        if item['name'] == DATABASE_NAME:
            print("找到創建的Database")

    SQL_QUERY = "DROP DATABASE " + DATABASE_NAME + ";"
    try:
        cursor.execute(SQL_QUERY)
        print("刪除資料庫")
    except pymssql._pymssql.OperationalError as e:
        #跟沒有加Try...exception 的訊息一樣
        traceback.print_exc()
    cursor.close()
    print("test pass")
