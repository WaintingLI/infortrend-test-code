'''
用來當作輸出Terminal文字為彩色的範本
'''
from colorama import init, Fore, Style
from time import sleep
import sys
import os




#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))


#讀取檔案參數與全域變數
'''
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
OPENCART_IP = cf.get("APP_Info","OpenCart_ip")
ADMIN_USERNAME = cf.get("APP_Info","Admin_Username")
ADMIN_PASSWORD = cf.get("APP_Info","Admin_Password")
#獲取使用者1資訊
USER1_FIRST_NAME = cf.get("User1","First_Name")
USER1_LAST_NAME = cf.get("User1","Last_Name")
USER1_E_MAIL = cf.get("User1","E-Mail")
USER1_PASSWORD = cf.get("User1","Password")
#獲取使用者2資訊
USER2_FIRST_NAME = cf.get("User2","First_Name")
USER2_LAST_NAME = cf.get("User2","Last_Name")
USER2_E_MAIL = cf.get("User2","E-Mail")
USER2_PASSWORD = cf.get("User2","Password")
#Chekcout時，所需要的資料
ADDRESS = cf.get("CheckOut","Address")
CITY = cf.get("CheckOut","City")
POST_CODE = cf.get("CheckOut","Post_Code")
'''








if __name__ == "__main__":
    #初始化文字顯示自色的程式
    init()
    print(Fore.LIGHTCYAN_EX,"LIGHTCYAN_EX")
    print(Fore.LIGHTWHITE_EX,"LIGHTWHITE_EX")
    print(Fore.LIGHTBLACK_EX,"LIGHTBLACK_EX")
    print(Fore.LIGHTGREEN_EX,"LIGHTGREEN_EX")
    print(Fore.LIGHTMAGENTA_EX,"LIGHTMAGENTA_EX")
    print(Fore.LIGHTRED_EX,"LIGHTRED_EX")
    print(Fore.LIGHTYELLOW_EX,"LIGHTYELLOW_EX")
    print(Fore.BLACK,"BLACK")
    print(Fore.YELLOW,"YELLOW")
    print(Fore.BLUE,"BLUE")
    print(Fore.CYAN,"CYAN")
    print(Fore.GREEN,"GREEN")
    print(Fore.MAGENTA,"MAGENTA")
    print(Fore.RED,"RED")
    print(Fore.WHITE,"WHITE")
    print(Fore.LIGHTWHITE_EX)
    print("前面有先告顏色的字樣")
    print(Style.RESET_ALL)
    print("Style.RESET_ALL這一串指令會將輸出的字串變為正常")