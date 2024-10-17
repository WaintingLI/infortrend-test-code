'''
用來當作瀏覽器的範本
'''
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
    #file_path = "demo.json"
    App_index = "App Config/"
    file_path = "demo_app.json"
    if not os.path.isfile(App_index+file_path):
        print(App_index+file_path,"is not found")
        #return
    print("PASS")
    get_app_list = []
    get_app_json_config ={}
    with open("App_install_list.txt","r",encoding="utf-8") as f:
        get_str = f.readline()
        while get_str != None and get_str !='':
            get_app_list.append(get_str.rstrip("\n"))
            get_str = f.readline()
    print("get_app_list=",get_app_list)
    for app_name_item in get_app_list:
        get_file_path = App_index + app_name_item + ".json"
        if not os.path.isfile(get_file_path):
            print(get_file_path,"is not found")
            continue
        with open(App_index + app_name_item + ".json","r",encoding="utf-8") as f:
            get_app_json_config = dict(json.load(f))
        print("get_app_json_config =",get_app_json_config)
    sys.exit(0)    
    
    with open(file_path,"r",encoding="utf-8") as f:
        a = dict(json.load(f))
        
        for i in a:
            pass
            #print(i,a[i])
        #b = a['info']
        #print(a['config'])
        #print(b)
        #print(a['config']['role']['9270590']['isControlPlane'])
        #print(a['config']['cluster']['time']['ntp']['pollingInterval'],type(a['config']['cluster']['time']['ntp']['pollingInterval']))
        #print(isinstance(a['config']['cluster']['time']['ntp']['pollingInterval'],str))
        print(a.get("asd",False))
        print(type(a['General']))
        print(type(a['Storage']))
        print(a['Service'].keys())
        print(type(a['Service']['App Image Service Type *']))
    
    test_dict = {"Service":{"App Image Service Type *":"LoadBalancer","aaaaaaaaaaaaaaaa":"1111111111"}}
    
    print("test_dict[\"Service\"].keys() =",type(list(test_dict["Service"].keys())),list(test_dict["Service"].keys())[0])
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
            
    