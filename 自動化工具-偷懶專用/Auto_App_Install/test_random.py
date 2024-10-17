'''
測試用
'''
import random
from time import sleep
import json
import sys
import os
import configparser




#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))





if __name__ == "__main__":
    string_nuber = 8
    print_string = ""
    
    get_str_list = random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',string_nuber)
    for i in range(string_nuber):
        print_string = print_string + get_str_list[i]
    print("print_string =>",print_string)