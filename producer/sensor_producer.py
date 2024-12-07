import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='10.32.6.171:9099',
    key_serializer=lambda k: k.encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_sensor_data():
    sensor_id = f"sensor_{random.randint(1, 11)}"
    return {
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 60.0), 2),
        'pressure': round(random.uniform(900.0, 1100.0), 2),
    }, sensor_id

def send_sensor_data():
    try:
        while True:
            data, key = generate_sensor_data()
            print(f"Sending sensor data: {data} with key: {key}")
            future = producer.send('sensor_data', key=key, value=data)
            
            record_metadata = future.get(timeout=10)
            
            print(f"Message sent to partition {record_metadata.partition} with offset {record_metadata.offset}")
            print("")
            
            producer.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Data sending stopped.")
    finally:
        producer.close()

send_sensor_data()
