"""
這是一份運來自動測試RabbitMQ的程式
"""
import os
import sys
import configparser
import time
from argparse import ArgumentParser
import pika

#切換命令提示字元到Python檔案所在的目錄
#檢查當前工作路徑是否在Python檔案的所在地，如果是就不會切換目錄
if os.path.dirname(sys.argv[0]):
    os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
RABBITMQ_IP = cf.get("APP_Info","RabbitMQ_ip")
PORT = cf.getint("APP_Info","Port")
USERNAME = cf.get("APP_Info","Username")
PASSWORD = cf.get("APP_Info","Password")



def create_args():
    '''
    創造Argument，對於使用命令列來說，創造相對應的參數，如果沒有輸入參數，那就全部採取預設值
    '''
    parser = ArgumentParser(description="RabbitMQ sender example")
    parser.add_argument(
        "-m",
        default='Hello World!',
        metavar='message',
        dest="msg",
        help="RabbitMQ sender message (default: \"Hello World!\")",)

    parser.add_argument(
        "-queue",
        default='hello',
        metavar='queue',
        dest="queue",
        help="RabbitMQ sender queue (default: \"hello\")",)

    parser.add_argument(
        "-host",
        default=RABBITMQ_IP,
        metavar='host',
        dest="host",
        help="RabbitMQ sender host (default: \"172.27.117.151\")",)

    parser.add_argument(
        "-u",
        default=USERNAME,
        metavar='username',
        dest="user",
        help="RabbitMQ sender username (default: \"admin\")",)

    parser.add_argument(
        "-pwd",
        default=PASSWORD,
        metavar='password',
        dest="pwd",
        help="RabbitMQ sender password (default: \"admin123\")",)

    parser.add_argument(
        "-p",
        type=int,
        default=PORT,
        metavar='port',
        dest="port",
        help="RabbitMQ sender port number (default: \"5672\")",)

    args_para = parser.parse_args()
    return args_para


if __name__ == '__main__':
    args = create_args()


    credentials = pika.PlainCredentials(args.user, args.pwd)
    connection_params = pika.ConnectionParameters(
        host=args.host,
        port=args.port,
        credentials=credentials
    )


    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel() # start a connection to rabbitmq server

    # declare a queue(if the queue is exist, it will not be created again)
    channel.queue_declare(queue=args.queue)
    channel.basic_publish(exchange = '',
                        routing_key = args.queue, # the queue name
                        body = args.msg ) # the message content

    print(f"[x] Sent {args.msg}")
    connection.close() # close the connection

    #等待五秒
    print("等待五秒來緩衝時間")
    for i in range(5):
        print(5-i)
        time.sleep(1)


    #開始準備接收資料
    print("準備開始接收資料")

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel() # start a connection to rabbitmq server

    method, properties, body=channel.basic_get(queue=args.queue)

    RECIEVCE_MESSAGE = str(body,'utf-8')

    if method:
        #print(method, properties, body)
        #檢查接收字串是否符合上傳字串
        if(RECIEVCE_MESSAGE == args.msg):
            print("RabbitMQ test result is PASS")
        else:
            print(f"Error Message - {body}")
        channel.basic_ack(method.delivery_tag)
    else:
        print('No message returned')
        sys.exit(1)

    connection.close() # close the connection
