Windows Client

1.安裝python依賴套件(cmd請先cd移動到跟requirements.txt同一層的資料夾)：pip install -r requirements.txt

2. 確認資料夾下的chromedriver.exe與當前的版本一致

3. 可以直接輸入"python open_cart_creat_customer_account.py -fn asd -fn zxc -em qazxswedc123456@example.com -pwd ADMIN1234567 -host http://opencart-test.k8s.local/"





[補充說明-相關參數]

-host  : Open Cart ip address		ex: http://opencart-test.k8s.local/
-fn    : First Name of customer account	ex: asd
-ln    : Last_Name of customer account	ex: zxc
-em    : E_Mail of customer account	ex: qazxswedc123456@example.com
-pwd   : password of customer account	ex: ADMIN1234567