import os
import sys
import threading
import platform
import time
from argparse import ArgumentParser
from colorama import init, Fore, Style
import test_ssh_connect_system


START_IP = 160
IP_DATA = "172.24.128."
HOLD_STRING = ""
SET_SSH_CONNECT_IP = '172.24.128.151'
#get_ip_list = test_ssh_connect_system.Get_kubectl_ip('172.24.128.111')

def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="IP test Example")
    parser.add_argument(
        "--ip",
        type=str,
        default="172.24.128.214",
        metavar="N",
        help="input ipv4",
    )
    parser.add_argument(
        "--range",
        type=int,
        default="20",
        metavar="N",
        help="input ip range",
    )
    parser.add_argument(
        "--ssh_ip",
        type=str,
        default="172.24.128.151",
        metavar="N",
        help="input connect ssh ip",
    )
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments


if __name__ == "__main__":
    init()
    args = create_args()
    get_args_ip = ""
    get_args_ip = args.ip
    SET_SSH_CONNECT_IP = args.ssh_ip
    ip_data_check = args.ip + "." + args.ssh_ip
    #檢查ip是否可以使用
    ##檢查字元是否為0~9、.
    for character in ip_data_check:
        if 48 <= ord(character) <=57 or ord(character) == 46:
            pass
        else:
            print("IP 有輸入錯誤")
            sys.exit(0)
    ##檢查ip是否超過255
    for item in ip_data_check.split("."):
        if int(item) > 255:
            print("IP 大小錯誤")
            sys.exit(0)
    ##檢查ip是否為ip v4
    if len(ip_data_check.split(".")) % 4 != 0:
        print(len(ip_data_check.split(".")))
        print("非IPv4 IP")
        sys.exit(0)


    IP_DATA = get_args_ip.split(".")[0] + "." + \
              get_args_ip.split(".")[1] + "." + \
              get_args_ip.split(".")[2] + "."
    START_IP = int(get_args_ip.split(".")[3])
    #print("IP_DATA =",IP_DATA)
    #print("START_IP =",START_IP)

    get_ip_list = test_ssh_connect_system.Get_kubectl_ip(SET_SSH_CONNECT_IP)
    print_list = []
    for i in range(0,args.range):
        GET_NUMBER = START_IP + i
        HOLD_STRING = IP_DATA + str(GET_NUMBER)
        SET_STRING=""

        for get_ip in get_ip_list:
            if HOLD_STRING == get_ip:
                SET_STRING=SET_STRING+Fore.LIGHTGREEN_EX+HOLD_STRING+": True"
                break
        else:
            SET_STRING=SET_STRING+Style.RESET_ALL+HOLD_STRING+": False"
        #print(SET_STRING)
        if i > 9:
            print_list[i%10] = print_list[i%10] + "\t" + SET_STRING
        else:
            print_list.append(SET_STRING)
    print("=====================")
    for item in print_list:
        print(item)
        
