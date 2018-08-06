import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
exchange = channel.exchange_declare(exchange='logs',
                                    exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'hello world'

channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(' [x] send %r' % message)

connection.close()


