import sys
import pygsheets
import time
import datetime



def update_experiment_data(Firmware_Version:str, CPU_AND_RAM_DATA:str) -> None:
    """_summary_
    將資料更新到K8S overnight IO,會去尋A欄上,名叫AI的欄位,之後找尋尚未填入的格字填寫今天日期與CPU_AND_RAM_DATA
    有做當寫如列位沒有了(曾測到VM字樣),會自動新增列位
    Args:
        CPU_AND_RAM_DATA (str): 記得要將CPU與RAM的資料丟進來
    """
    #獲取Google帳戶權限
    gc = pygsheets.authorize(service_file='./請填寫自己的認證資料json')

    sht = gc.open_by_url(
    '輸入要填寫的表單'
    )


    wks_list = sht.worksheets()
    print(wks_list)

    #選取by順序
    wks = sht[1]
    print("開始")
    #get Time
    #如果是星期一,就會擷取禮拜五的時間
    if datetime.date.today().weekday() == 0:
        SET_DATE = str((datetime.date.today()-datetime.timedelta(days=3)).strftime("%Y/%m/%d") \
                       +"~"+datetime.date.today().strftime("%Y/%m/%d"))
    else:
        SET_DATE = str((datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y/%m/%d") \
                       +"~"+datetime.date.today().strftime("%Y/%m/%d"))
    print(SET_DATE)
    #get_wks_row_data = wks.get_row(82,returnas='matrix')
    #print(get_wks_row_data,type(get_wks_row_data))
    #print(np.array(get_wks_row_data),type(np.array(get_wks_row_data)))
    #test = [['1','2','3']]
    #print(test,type(test))
    #wks.update_values('A85',[get_wks_row_data])
    #wks.delete_rows(85, number=1)
    #wks.insert_rows(84,number=3,values=None, inherit=False)
    #exit(0)



    #讀取
    #Read_A = wks.cell('A40')
    Counter = 1
    Read_A = wks.cell('A1'+str(Counter))
    while(Read_A.value != 'AI'):
        #time.sleep(1)
        Counter=Counter+1
        Read_A = wks.cell('A'+str(Counter))
        print("===")
        print(Counter,"=>",Read_A.value)
    print("==============Finish=============")
    while(Read_A.value != ""):
        Counter=Counter+1
        Read_A = wks.cell('A'+str(Counter))
        print("Counter = ",Counter)
        print(Read_A.value)
        if(Read_A.value == ''):
            # Update
            wks.update_value('A'+str(Counter), SET_DATE)
            wks.update_value('B'+str(Counter), Firmware_Version)
            wks.update_value('L'+str(Counter), CPU_AND_RAM_DATA)
        if(Read_A.value =="VM"):
            ADD_ROW_NUMBER = 5
            Counter = Counter - 1
            get_temp_wks_row_data = wks.get_row(Counter,returnas='matrix')
            Counter = Counter - 1
            wks.insert_rows(Counter,number=ADD_ROW_NUMBER)
            Counter = Counter + 1
            wks.update_values('A'+str(Counter),[get_temp_wks_row_data])
            wks.delete_rows(Counter+ADD_ROW_NUMBER, number=1)
            Read_A = wks.cell('A'+str(Counter))        
    print("==============Finish-2=============")




if __name__  == "__main__":
    gc = pygsheets.authorize(service_file='./test-api-420102-4e4919f94ad4.json')

    sht = gc.open_by_url(
    '輸入要填寫的表單'
    )

    print(datetime.date.today().strftime("%#m/%#d"))
    
    
    
    
    try:
        wks_list = sht.worksheets('title',datetime.date.today().strftime("%#m/%#d"))
        
        if len(wks_list) != 1:
            print("xxxxxxx檢測到有相同的日期,所以不更新資料xxxxxxxxxxx")
            print(wks_list)
            sys.exit(0)
    except pygsheets.exceptions.WorksheetNotFound:
        print("沒有找到相關的表單,請檢察表單")
        print("xxxxxxxxxxxxxx沒有更新今天加班資料xxxxxxxxxxxxxx")
        sys.exit(0)
        
    

    #選取by順序
    #wks = sht[0]
    wks = wks_list[0]
    
    
    print("開始")
    #get Time
    #如果是星期一,就會擷取禮拜五的時間
    if datetime.date.today().weekday() == 0:
        SET_DATE = str((datetime.date.today()-datetime.timedelta(days=3)).strftime("%Y/%m/%d") \
                       +"~"+datetime.date.today().strftime("%Y/%m/%d"))
    else:
        SET_DATE = str((datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y/%m/%d") \
                       +"~"+datetime.date.today().strftime("%Y/%m/%d"))
    print(SET_DATE)
    #get_wks_row_data = wks.get_row(82,returnas='matrix')
    #print(get_wks_row_data,type(get_wks_row_data))
    #print(np.array(get_wks_row_data),type(np.array(get_wks_row_data)))
    #test = [['1','2','3']]
    #print(test,type(test))
    #wks.update_values('A85',[get_wks_row_data])
    #wks.delete_rows(85, number=1)
    #wks.insert_rows(84,number=3,values=None, inherit=False)
    #exit(0)



    #讀取
    #Read_A = wks.cell('A40')
    Counter = 1
    Read_A = wks.cell('A1'+str(Counter))
    while(Read_A.value != 'AI Team'):
        #time.sleep(1)
        Counter=Counter+1
        Read_A = wks.cell('A'+str(Counter))
        print("===")
        print(Read_A.value)
    print("==============Find AI Team=============")
    while(Read_A.value != ""):
        Counter=Counter+1
        Read_A = wks.cell('A'+str(Counter))
        print("Counter = ",Counter)
        print(Read_A.value)
        if(Read_A.value == ''):
            # Update
            #Team
            wks.update_value('A'+str(Counter), "Waiting")
            #Project
            wks.update_value('B'+str(Counter), "K8s phase2.0")
            #Test Item
            wks.update_value('C'+str(Counter), "app test")
        if(Read_A.value =="UI Team"):
            ADD_ROW_NUMBER = 5
            Counter = Counter - 1
            get_temp_wks_row_data = wks.get_row(Counter,returnas='matrix')
            Counter = Counter - 1
            wks.insert_rows(Counter,number=ADD_ROW_NUMBER)
            Counter = Counter + 1
            wks.update_values('A'+str(Counter),[get_temp_wks_row_data])
            wks.delete_rows(Counter+ADD_ROW_NUMBER, number=1)
            Read_A = wks.cell('A'+str(Counter))
    '''
    A42 = wks.cell('A42')
    A42.value
    print(A42.value,type(A42.value))
    A80 = wks.cell('A80')
    A80.value
    print(A80.value,type(A80.value))
    '''
    #匯出CSV
    #wks.export(pygsheets.ExportType.CSV)
