"""
測試Cliclkhouse是否安裝正常
"""
import sys
import traceback
import os
import configparser
import clickhouse_connect
import clickhouse_connect.driver
import clickhouse_connect.driver.exceptions

#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
CLICKHOUSE_IP = cf.get("Clickhouse_Info","Clickhouse_ip")
CLICKHOUSE_IP_PORT = cf.getint("Clickhouse_Info","Clickhouse_ip_port")
USER = cf.get("Clickhouse_Info","User")
USER_PASSWORD = cf.get("Clickhouse_Info","Password")
DATABASE = cf.get("Clickhouse_Info","Database")


if __name__ == "__main__":
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_IP,
        port=CLICKHOUSE_IP_PORT,
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
