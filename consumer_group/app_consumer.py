from kafka import KafkaConsumer
import json
import socketio
import sys
import uuid

sio = socketio.Client()
sio.connect('http://localhost:5000')

consumer_id = sys.argv[1] if len(sys.argv) > 1 else f"consumer_{uuid.uuid4().hex[:6]}"

consumer = KafkaConsumer(
    'http_logs',
    bootstrap_servers='10.32.6.195:9099',
    group_id='log_consumer_group',
    key_deserializer=lambda k: k.decode('utf-8'),
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

def consume_logs():
    for message in consumer:
        log_data = {
            'log': message.value,
            'partition': message.partition,
            'offset': message.offset,
            'consumer_id': consumer_id
        }
        sio.emit('new_log', log_data)

if __name__ == '__main__':
    consume_logs()
