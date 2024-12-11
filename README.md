# Kafka Übung 18.12.2024


## Setup
```bash
# Kafka CLI Container starten
docker run -d --add-host=conduktor-gateway:10.32.6.195 --name kafka-cli apache/kafka:latest
```

```bash
# Kafka CLI aufrufen
docker exec --workdir /opt/kafka/bin/ -it kafka-cli sh
```

```bash
# Kafka Umgebungsvariable setzen
export KAFKA_GW="10.32.6.195:9099"
```


## Nachrichten veröffentlichen
```bash
# Nachrichten veröffentlichen
./kafka-console-producer.sh --bootstrap-server $KAFKA_GW --topic test-topic --property "parse.key=true" --property "key.separator=:"
```

```bash
# Eingabeformat
Key1:Meine erste Nachricht
Key2:Meine erste Nachricht mit Key2
Key1:Meine zweite Nachricht mit Key1
```

## Nachrichten lesen
```bash
# Neue Nachrichten lesen
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GW --topic test-topic
```

```bash
# Alle Nachrichten lesen: Dazu Parameter `--from-beginning` anhängen
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GW --topic test-topic --from-beginning
```

## Cleanup
```bash
# Kafka CLI Container stoppen und löschen
docker stop kafka-cli -t 0 && docker rm kafka-cli
```