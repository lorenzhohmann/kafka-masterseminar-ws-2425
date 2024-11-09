from flask import Flask, render_template, request, jsonify
from confluent_kafka import Producer, Consumer, KafkaError
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

KAFKA_BOOTSTRAP_SERVERS = "localhost:9099"

producer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'linger.ms': 10
}

consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': 'flask-group',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
    'fetch.min.bytes': 1,
    'fetch.wait.max.ms': 10
}

producer = Producer(producer_conf)
consumer = Consumer(consumer_conf)

def consume_messages():
    consumer.subscribe(["test-topic"])
    print("Consumer is running and listening on the topic 'test-topic'...")
    
    while True:
        try:
            msg = consumer.poll(timeout=0.1)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    continue

            message_decoded = msg.value().decode('utf-8')
            print(f"New message received: {message_decoded}")
            socketio.emit('new_message', {'message': message_decoded})

        except Exception as e:
            print(f"Error consuming messages: {e}")
            pass 

socketio.start_background_task(consume_messages)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify(error="Message is required."), 400

    try:
        producer.produce("test-topic", value=message, callback=delivery_report)
        producer.poll(0)
        return jsonify(success=True)
    except Exception as e:
        print(f"Error sending message: {e}")
        return jsonify(error="Failed to send message."), 500

def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
