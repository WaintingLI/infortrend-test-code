import sys
import pygsheets
import time
import datetime



def update_work_overtime_date(Set_Date:str = "1800~1900") -> None:
    """_summary_
    自動將加班時間填到對應Google表單
    Args:
        Set_Date (str, optional): 輸入加班時間. Defaults to "1800~1900".
    """
    #獲取Google帳戶權限
    gc = pygsheets.authorize(service_file='./請填入自己的帳戶權限檔案')

    #要填寫的Google表單
    sht = gc.open_by_url(
    '輸入要填寫的Google表單'
    )

    print("============開始上傳============")
    wks_list = sht.worksheets()
    print(wks_list)


    #選取by順序
    wks = sht[0]
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



    #收尋日期
    Get_today = datetime.date.today().strftime("%m/01")
    Month = 'A'
    Read_date = wks.cell(Month+'2')
    while  Read_date.value != Get_today:
        deta_data = ord(Month) + 2
        Month = chr(deta_data)
        Read_date = wks.cell(Month+'2')
    #print("Month =>",Month)
    #收尋今天日期
    Get_today = datetime.date.today().strftime("%m/%d")
    day_counter = 2
    for i in range(32):
        Read_date = wks.cell(Month+str(day_counter))
        if Read_date.value == Get_today:
            break
        else:
            day_counter = day_counter  + 1

    #上傳資料
    #print("day_counter",day_counter)
    Delta_data = ord(Month) + 1
    Set_month = chr(Delta_data)
    if day_counter < 34:
        wks.update_value(Set_month + str(day_counter), Set_Date)
    else:
        print("沒有找到相對應的日期")
        print("Month=>",Month,";day_counter=>",day_counter)
    print("===========資料上傳完畢===========")

def update_workovertime_schedule() -> None:
    """自動將今天的加班登記到加班表上
    """
    gc = pygsheets.authorize(service_file='./test-api-420102-4e4919f94ad4.json')

    sht = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1qZeUnR9gE40jNu30aSoceIws7XQGzsrZKLb1XJsoEgI/edit?gid=560492456#gid=560492456'
    )

    #print(datetime.date.today().strftime("%#m/%#d"))
    
    
    
    
    try:
        wks_list = sht.worksheets('title',datetime.date.today().strftime("%#m/%#d"))
        #檢查自否有相同日期
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

if __name__  == "__main__":
    gc = pygsheets.authorize(service_file='./test-api-420102-4e4919f94ad4.json')

    sht = gc.open_by_url(
    '輸入要填寫的表單'
    )


    wks_list = sht.worksheets()
    print(wks_list)

    #選取by順序
    wks = sht[0]
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



    #收尋日期
    Get_today = datetime.date.today().strftime("%m/01")
    Month = 'A'
    Read_date = wks.cell(Month+'2')
    while  Read_date.value != Get_today:
        deta_data = ord(Month) + 2
        Month = chr(deta_data)
        Read_date = wks.cell(Month+'2')
    #print("Month =>",Month)
    #收尋今天日期
    Get_today = datetime.date.today().strftime("%m/%d")
    day_counter = 2
    for i in range(32):
        Read_date = wks.cell(Month+str(day_counter))
        if Read_date.value == Get_today:
            break
        else:
            day_counter = day_counter  + 1

    #上傳資料
    #print("day_counter",day_counter)
    Delta_data = ord(Month) + 1
    Set_month = chr(Delta_data)
    if day_counter < 34:
        wks.update_value(Set_month + str(day_counter), "1800~1900")
    else:
        print("沒有找到相對應的日期")
        print("Month=>",Month,";day_counter=>",day_counter)
