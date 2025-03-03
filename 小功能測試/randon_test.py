"""
使用亂數創造名稱
"""

import random


if __name__ == "__main__":
        #使用亂數來創造名字
        string_nuber = 8
        print_string = ""
        get_str_list = random.sample('1234567890zyxwvutsrqponmlkjihgfedcba',string_nuber)
        for number in range(string_nuber):
                print_string = print_string + get_str_list[number]
                return_pvc_name = "app_pvc_name"+"-"+print_string
        print(return_pvc_name)
