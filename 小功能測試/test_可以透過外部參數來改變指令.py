import pika
from argparse import ArgumentParser

def create_args():
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
        default='172.27.117.151',
        metavar='host',
        dest="host",
        help="RabbitMQ sender host (default: \"172.27.117.151\")",)

    parser.add_argument(
        "-u",
        default='admin',
        metavar='username',
        dest="user",
        help="RabbitMQ sender username (default: \"admin\")",)

    parser.add_argument(
        "-pwd",
        default='admin123',
        metavar='password',
        dest="pwd",
        help="RabbitMQ sender password (default: \"admin123\")",)

    parser.add_argument(
        "-p",
        type=int,
        default=5672,
        metavar='port',
        dest="port",
        help="RabbitMQ sender port number (default: \"5672\")",)

    args = parser.parse_args()
    return args


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

    channel.queue_declare(queue=args.queue) # declare a queue(if the queue is exist, it will not be created again)
    channel.basic_publish(exchange = '',
                        routing_key = args.queue, # the queue name
                        body = args.msg ) # the message content

    print(f"[x] Sent {args.msg}")
    connection.close() # close the connection