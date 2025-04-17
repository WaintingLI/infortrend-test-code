"""
測試Cliclkhouse是否安裝正常
"""
import sys
import traceback
import os
import configparser
from argparse import ArgumentParser
import clickhouse_connect
import clickhouse_connect.driver
import clickhouse_connect.driver.exceptions


#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
#CLICKHOUSE_IP = cf.get("Clickhouse_Info","Clickhouse_ip")
#CLICKHOUSE_IP_PORT = cf.getint("Clickhouse_Info","Clickhouse_ip_port")
USER = cf.get("Clickhouse_Info","User")
USER_PASSWORD = cf.get("Clickhouse_Info","Password")
DATABASE = cf.get("Clickhouse_Info","Database")

def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="Clickhouse Example")
    parser.add_argument(
        "--ip",
        type=str,
        default="172.24.128.165",
        metavar="N",
        help="input ipv4",
    )
    parser.add_argument(
        "--port",
        type=str,
        default="8123",
        metavar="N",
        help="input ip port",
    )
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments

if __name__ == "__main__":
    args = create_args()
    client = clickhouse_connect.get_client(
        host=args.ip,
        port=args.port,
        username=USER,
        password=USER_PASSWORD,
        connect_timeout=30
        )
    client.command("CREATE DATABASE IF NOT EXISTS " + DATABASE)
    #print(client.command("SHOW DATABASES"))
    client.close()
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_IP,
            port=CLICKHOUSE_IP_PORT,
            username=USER,
            password=USER_PASSWORD,
            database=DATABASE)
        #print(type(client.command("SHOW DATABASES")))
        print(client.command("drop database " + DATABASE))
        client.close()
    except clickhouse_connect.driver.exceptions.DatabaseError  as e:
        traceback.print_exc()
        print("Test Fail")
        sys.exit(1)
    print("Test PASS")
