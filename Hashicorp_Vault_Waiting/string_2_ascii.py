'''
用來處理字串轉換為Hex十六進位值
'''
import sys
import os




#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

def string_to_hex(input_string:str) -> None:
    """將字串轉為十六進位表示
    Args:
        input_string (str): 要轉換的字串
    """
    ascii_values = []
    for character in input_string:
        ascii_values.append(hex(ord(character)))
    print(ascii_values)





if __name__ == "__main__":
    string_to_hex("Apple")
    sys.exit(0)
    file_path = "add_watcher.txt"
    if not os.path.isfile(file_path):
        print(file_path,"is not found")
        #return
    print("PASS")
    with open(file_path,"r",encoding="utf-8") as f:
        meta_data = f.readlines()
        for watcher in meta_data:
            print(watcher)
            ascii_values = []
            for character in watcher.rstrip("\n"):
                ascii_values.append(hex(ord(character)))
            print(ascii_values)
                #[87, 97, 121, 110, 101, 32, 67, 104, 111, 117, 10]
                #[87, 97, 121, 110, 101, 32, 67, 104, 111, 117]
    