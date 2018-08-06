import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

routing_keys = sys.argv[1:]
if len(routing_keys) <= 0:
    sys.stderr.write("Usage %s : need a routing_key" % sys.argv[0])
    sys.exit(1)

for routing_key in routing_keys:
    channel.queue_bind(exchange='topic_logs',
                   routing_key=routing_key,
                   queue=queue_name)

def callback(ch, method, proerties, body):
        print("%s get msg %s" % (method.routing_key, body))

channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
channel.close()
