from selenium.webdriver.chrome.options import Options

#加上以下設定即可關掉password leak popup -> 主要是關閉這個profile.password_manager_leak_detection
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False,
         "profile.password_manager_leak_detection":False}
options.add_experimental_option("prefs", prefs)