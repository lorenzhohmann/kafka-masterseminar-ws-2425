import json
import time
import random
from kafka import KafkaProducer

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9099',
    key_serializer=lambda k: k.encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# List of possible URLs, HTTP methods, status codes, and user-agents
urls = ['/index.html', '/about.html', '/contact.html', '/products.html']
http_methods = ['GET', 'POST', 'PUT', 'DELETE']
status_codes = [200, 301, 404, 500]
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
]

# Generate a random HTTP log entry
def generate_http_log():
    client_ip = f"192.168.1.{random.randint(1, 255)}"
    timestamp = time.strftime('%d/%b/%Y:%H:%M:%S +0000', time.gmtime())
    method = random.choice(http_methods)
    url = random.choice(urls)
    status_code = random.choice(status_codes)
    user_agent = random.choice(user_agents)

    # Generate log entry as a dictionary
    log_data = {
        'client_ip': client_ip,
        'timestamp': timestamp,
        'method': method,
        'url': url,
        'status_code': status_code,
        'user_agent': user_agent,
    }
    return log_data, client_ip

# Send HTTP logs to Kafka
def send_http_logs():
    try:
        while True:
            log_data, key = generate_http_log()
            print(f"Sending HTTP log: {log_data} with key: {key}")
            
            # Send the log data to Kafka with the client IP as the key
            future = producer.send('http_logs', key=key, value=log_data)
            
            # Get metadata (partition and offset) after sending the message
            record_metadata = future.get(timeout=10)
            
            # Print the partition and offset information
            print(f"Message sent to partition {record_metadata.partition} with offset {record_metadata.offset}")
            print("")
            
            producer.flush()
            time.sleep(1)  # Simulate a new log entry every 0.2 seconds
    except KeyboardInterrupt:
        print("Data sending stopped.")
    finally:
        producer.close()

# Start sending HTTP logs
send_http_logs()
