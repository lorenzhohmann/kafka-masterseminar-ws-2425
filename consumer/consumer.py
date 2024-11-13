# consumer.py
import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'http_logs',  # Name des Kafka Topics
    bootstrap_servers='localhost:9099',
    group_id='log_consumer_group',  # Consumer-Gruppe
    key_deserializer=lambda k: k.decode('utf-8'),
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def consume_logs():
    for message in consumer:
        yield message.value  # Die Nachricht wird als Generator zurückgegeben

# Ein einfacher Consumer, der Nachrichten in der Konsole anzeigt
def display_logs():
    try:
        for message in consume_logs():
            print(f"Received message: {message}")
    except KeyboardInterrupt:
        print("Consumer stopped.")
    finally:
        consumer.close()
