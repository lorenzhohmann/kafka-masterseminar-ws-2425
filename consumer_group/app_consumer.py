from kafka import KafkaConsumer
import json
import socketio
import sys
import uuid

# SocketIO-Client zum Senden der Nachrichten an die UI-Instanz
sio = socketio.Client()
sio.connect('http://localhost:5000')  # Verbindung zur UI auf Port 5000

# Eindeutige ID für jeden Consumer
consumer_id = sys.argv[1] if len(sys.argv) > 1 else f"consumer_{uuid.uuid4().hex[:6]}"

# Kafka-Consumer-Einstellungen
consumer = KafkaConsumer(
    'http_logs',
    bootstrap_servers='localhost:9099',
    group_id='log_consumer_group',
    key_deserializer=lambda k: k.decode('utf-8'),
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest'
)

# Log-Nachrichten konsumieren und an die UI-Instanz weiterleiten
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
