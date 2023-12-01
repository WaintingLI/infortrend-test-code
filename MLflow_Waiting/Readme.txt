Windows Client

1.
#1. 安裝python依賴套件(cmd請先cd移動到跟requirements.txt同一層的資料夾)：pip3 install -r requirements.txt
#2. 安裝git套件，到"https://git-scm.com/download/win"去安裝，因為ML flow的Module會使用到，安裝完可以到Cmd(命令提示字元)輸入"git --version"，有沒有安裝成功


2.
config.ini檔案需和.py執行檔放在同一資料夾下，並依照需求更改內容。
請安裝完成"Ml flow"後，在"config.ini"中，修改"Mlflow_ip"要等於Mlflow網址，確定瀏覽器可以連上ML flow的網頁後，就可以開始測試了


3.
jenkins執行的command是mlflow_auto_test.py的路徑
jenkins的time out時間，請改為"1200000"，大約等20分鐘