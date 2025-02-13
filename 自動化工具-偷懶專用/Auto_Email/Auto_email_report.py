'''
用來自動化加班填寫流程
'''
from time import sleep
import sys
import os
import configparser
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders



#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地,如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))


#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
E_FLOW_ip = cf.get("APP_Info","E_FLOW_ip")








if __name__ == "__main__":
    smtp=smtplib.SMTP('192.168.99.52', 25)
    smtp.ehlo()
    #smtp.starttls(None)
    #smtp.login('Email','Password')
    #from_addr=' Email'
    from_addr='Email'
    to_addr="Email"
    html="""
    <!doctype html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>HTML mail</title>
    </head>
    <body>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif">Hi Hank,</span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif"><o:p>&nbsp;</o:p></span>
        <p></p>
        <span style="font-family:&quot;微軟正黑體&quot;,sans-serif">附件如標題所示<span lang="EN-US"><o:p></o:p></span></span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif"><o:p>&nbsp;</o:p></span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif">Thanks,<o:p></o:p></span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif">WaitingL<o:p></o:p></span>
    </body>
    </html>
    """
    #创建一个带附件的实例
    message = MIMEMultipart()
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    #message = MIMEText('Hi Hank,\n\n附件如標題所示\n\nThanks,\nWaitingL', 'plain', 'utf-8')
    #message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header(from_addr, 'utf-8')   # 发送者
    message['To'] =  Header(to_addr, 'utf-8')        # 接收者
    subject = '20250213---測試與統計項目'
    message['Subject'] = Header(subject, 'utf-8')
    #正文
    message.attach(MIMEText(html, 'html', 'utf-8'))
    
    # 构造附件1，传送当前目录下的 test.txt 文件
    '''
    att1 = MIMEText(open('測試項目統計_Waiting_20250213.xls', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="測試項目統計.xls"'
    message.attach(att1)
    '''
    att2 = MIMEBase('application','octet-stream')
    att2.set_payload(open('測試項目統計_Waiting_20250213.xls', 'rb').read())
    att2.add_header('Content-Disposition','attachment',filename=os.path.basename('測試項目統計_Waiting_20250213.xls'))
    encoders.encode_base64(att2)
    message.attach(att2)
    #status=smtp.sendmail(from_addr, to_addr, msg)#加密文件，避免私密信息被截取
    status=smtp.sendmail(from_addr, to_addr, message.as_string())
    if status=={}:
        print("郵件傳送成功!")
    else:
        print("郵件傳送失敗!")
    smtp.quit()