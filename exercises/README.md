```bash
# Start the Kafka container
docker run -d --name kafka-cli apache/kafka:latest
```

```bash
# Access the Kafka container
docker exec --workdir /opt/kafka/bin/ -it kafka-cli sh
```

```bash
# Set the environment variables
export KAFKA_GATEWAY="10.32.5.177:9099"
```

```bash
# Create a topic
./kafka-topics.sh --bootstrap-server $KAFKA_GATEWAY --create --topic test-topic
```

```bash
# Write a message to the topic
./kafka-console-producer.sh --bootstrap-server $KAFKA_GATEWAY --topic test-topic

```

```bash
# Read messages from the topic
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GATEWAY --topic test-topic --from-beginning
```