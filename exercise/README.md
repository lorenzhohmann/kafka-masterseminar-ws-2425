# Exercise

## Setup
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
export KAFKA_GW="10.32.6.171:9099"
```

## Create a topic
```bash
# Create a topic
./kafka-topics.sh --bootstrap-server $KAFKA_GW --create --topic topic-name
```

## Write messages
```bash
# Write messages to the topic
./kafka-console-producer.sh --bootstrap-server $KAFKA_GW --topic topic-name
```

```bash
# Write messages with a key to the topic
./kafka-console-producer.sh --bootstrap-server $KAFKA_GW --topic topic-name --property "parse.key=true" --property "key.separator=:"
```

## Read messages
```bash
# Read new messages from the topic
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GW --topic topic-name
```

```bash
# Read all messages from the topic
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GW --topic topic-name --from-beginning
```

## Cleanup
```bash
# Stop the Kafka container
docker stop kafka-cli
```