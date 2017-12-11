#!/usr/bin/env python
import pika
import sys
if len(sys.argv) == 2:

    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.2.154'))
    channel = connection.channel()
    
    # channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=sys.argv[1])
    print(" [x] Sent '%s!'" % sys.argv[1])
    
    connection.close()
    
    

else:

    from kombu import Connection, Exchange, Queue
    
    media_exchange = Exchange('welog', 'topic', durable=True)
    video_queue = Queue('welog', exchange=media_exchange, routing_key='')

    # connections
    with Connection('amqp://guochen:1111@192.168.2.154//') as conn:
    
        # produce
        producer = conn.Producer(serializer='json')
        print producer.publish({'edm_id': 10},
                          exchange=media_exchange,
                          declare=[video_queue])
    
