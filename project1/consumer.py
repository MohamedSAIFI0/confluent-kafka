from kafka import KafkaConsumer
import json
import time

consumer = KafkaConsumer(
    'learning-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="learning-group",
    value_desrializer = lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print(message)