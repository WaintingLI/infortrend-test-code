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
FROM_ADDR = cf.get("Email_Info","From_address")
TO_ADDR = cf.get("Email_Info","To_address")
EMAIL_SUBJECT = cf.get("Email_Info","Subject")
PATH = cf.get("Email_Info","File_path")
PREFIX = cf.get("Email_Info","File_name_prefix")
FILEEXTENSION = cf.get("Email_Info","File_name_extension")







if __name__ == "__main__":
    TODAY = datetime.date.today().strftime("%Y%m%d")
    FILE_NAME = PREFIX + TODAY + FILEEXTENSION
    # 檢查檔案是否存在
    if os.path.isfile(PATH + FILE_NAME):
        print(FILE_NAME,"檔案存在。")
    else:
        print(FILE_NAME,"XXX檔案不存在。")
        sys.exit(1)

    smtp=smtplib.SMTP('192.168.99.52', 25)
    smtp.ehlo()
    #smtp.starttls(None)
    #smtp.login('Email','Password')

    HTML="""
    <!doctype html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>HTML mail</title>
    </head>
    <body>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif">Hi XXX,</span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif"><o:p>&nbsp;</o:p></span>
        <p></p>
        <span style="font-family:&quot;微軟正黑體&quot;,sans-serif">附件如標題所示<span lang="EN-US"><o:p></o:p></span></span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif"><o:p>&nbsp;</o:p></span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif">Thanks,<o:p></o:p></span>
        <p></p>
        <span lang="EN-US" style="font-family:&quot;微軟正黑體&quot;,sans-serif">XXXXXXXX<o:p></o:p></span>
    </body>
    </html>
    """
    #创建一个带附件的实例
    message = MIMEMultipart()
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    #message = MIMEText('Hi Hank,\n\n附件如標題所示\n\nThanks,\nWaitingL', 'plain', 'utf-8')
    #message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header(FROM_ADDR, 'utf-8')   # 发送者
    message['To'] =  Header(TO_ADDR, 'utf-8')        # 接收者
    subject = TODAY + "---" +EMAIL_SUBJECT
    message['Subject'] = Header(subject, 'utf-8')
    #正文
    message.attach(MIMEText(HTML, 'html', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att2 = MIMEBase('application','octet-stream')
    att2.set_payload(open(PATH + FILE_NAME, 'rb').read())
    att2.add_header('Content-Disposition','attachment',filename=os.path.basename(FILE_NAME))
    encoders.encode_base64(att2)
    message.attach(att2)
    #status=smtp.sendmail(from_addr, to_addr, msg)#加密文件，避免私密信息被截取
    status=smtp.sendmail(FROM_ADDR, TO_ADDR, message.as_string())
    print("🎉🎉🎉 Send Email OK 🎉🎉🎉 ")
    print("From:",FROM_ADDR," >>>>>>>>>>>>>>>>>>>>> ","TO:",TO_ADDR)
    sleep(1)
    smtp.quit()
