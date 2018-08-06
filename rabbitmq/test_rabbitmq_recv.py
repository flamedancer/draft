#!/usr/bin/env python
import sys
if len(sys.argv) < 2:
    import pika
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    channel.queue_declare(queue='hello')
    
    def callback(ch, method, properties, body):
        try:
            print(" [x] Received %r" % int(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:        
            raise e
                       
    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=False)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

else:

    from kombu import Connection, Exchange, Queue
    
    media_exchange = Exchange('welog', 'topic', durable=True)
    video_queue = Queue('welog', exchange=media_exchange, routing_key='welog')
    
    def process_media(body, message):
        print body
        message.ack()
    
    
    # connections
    with Connection('amqp://guest:guest@localhost//') as conn:
        # consume
        with conn.Consumer(video_queue, callbacks=[process_media]) as consumer:
            # Process messages and handle events on all channels
            while True:
                conn.drain_events()
    
        
