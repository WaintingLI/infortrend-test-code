Windows Client

1.安裝python依賴套件(cmd請先cd移動到跟requirements.txt同一層的資料夾)：pip install -r requirements.txt

2. 確認資料夾下的chromedriver.exe與當前的版本一致

3.修改config.ini檔案，且需和.py執行檔放在同一資料夾下，並依照需求更改內容。
修改以下參數:
OpenCart_ip	=>修改為OpenCart IP網路位置
Admin_Username	=>Administration頁面的管理員帳號，通常預設是admin
Admin_Password	=>Administration頁面的管理員密碼，通常預設是admin123





[補充說明]
自動測試程式的瀏覽器，務必不要縮到最小，可能會發生錯誤。
config.ini檔案中，
User1會是在OpenCart購物頁面註冊的帳號，
User2會是在OpenCart Administration頁面新增的帳號，
CheckOut是會在進行Check out時，所需要的地址資訊，
以上這些資訊，基本上都不需要修改。

[補充說明-程式購物流程會買的東西與wish list]
會到http://opencart-test.k8s.local/en-gb/catalog/smartphone底下購物這幾個物品
1. HTC Touch HD
2. iPhone
3. Palm Treo Pro

[補充說明-程式預設的檢查，如果檢查錯誤，會終止程式]
1. 檢查網站是否可以正常連線
2. wish list沒有預期的商品
3. 沒有成立order(購物訂單)