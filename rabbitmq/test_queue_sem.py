from kombu import Connection, Exchange, Queue

media_exchange = Exchange('sem', 'topic', durable=True)
video_queue = Queue('queue_sem_report_task', exchange=media_exchange, routing_key='')

# connections
with Connection('amqp://guochen:1111@192.168.2.154//') as conn:

    # produce
    # producer = conn.Producer(serializer='json')
    producer = conn.Producer()
    print producer.publish('{"id": "149207840858ef4f48cdb60"}',
        retry=True,
        retry_policy={
            'interval_start': 0, # First retry immediately,
            'interval_step': 2,  # then increase by 2s for every retry.
            'interval_max': 30,  # but don't exceed 30s between retries.
            'max_retries': 30,   # give up after 30 tries.
        },
        exchange=media_exchange,
        declare=[video_queue])

