from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from kafka import KafkaConsumer
import threading

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers='10.32.6.195:9099',
    key_deserializer=lambda k: k.decode('utf-8') if k else None,
    value_deserializer=lambda v: v.decode('utf-8') if v else None,
    auto_offset_reset='earliest'
)

def consume_logs():
    print(consumer)
    for message in consumer:
        log_data = {
            'log': message.value,
            'partition': message.partition,
            'offset': message.offset,
            'key': message.key
        }

        socketio.emit('new_log', log_data, namespace='/')

@app.route('/')
def index():
    return render_template('index.html')

def start_consumer():
    socketio.start_background_task(target=consume_logs)

if __name__ == '__main__':
    threading.Thread(target=start_consumer).start()
    socketio.run(app, host='0.0.0.0', port=5000)
