Windows Client

1. 安裝python依賴套件(cmd請先cd移動到跟requirements.txt同一層的資料夾)：pip install -r requirements.txt


2. 請將此App執行到操作SOP的步驟8



3. config.ini檔案需和.py執行檔放在同一資料夾下，並依照需求更改內容。
請先確認以下內容:
[config.ini] Project name與Project Key 不要與Jira Software專案中重複



[補充說明:由於ini會自動更新，以下是config.ini說明]

[APP_Info]

JiraSoftware_ip = http://jira-test.k8s.local/
#JiraSoftware_ip 請輸入可以接到JiraSoftware_ip的網路位置

Admin_Username = admin
#請填入在"Set up administrator account"頁面中的Username

Admin_Password = admin123
#請填入在"Set up administrator account"頁面中的Password

Admin_E-Mail = abc@example.com
#請填入在"Set up administrator account"頁面中的Email address

[Project]
Project_Name = test
#請輸入一個要用來測試的專案名稱

Project_Key = TEST
#請輸入一個要用來測試的專案Key Name







