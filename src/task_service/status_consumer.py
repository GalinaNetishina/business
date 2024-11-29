from confluent_kafka import Consumer, KafkaError, KafkaException

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['status'])
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"end of {msg.topic()} [{msg.partition()}]")
            else:
                raise KafkaException(msg.error())
        else:
            task = msg.value()
            print(f'message received: \n{task}')

finally:
    consumer.close()