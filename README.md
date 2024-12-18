# Kafka Übung 18.12.2024

## Conduktor Web UI (via VPN)
http://10.32.7.81:8080/

__Login__: \
admin@example.com \
admin_password



## Kafka CLI
### Setup 
Kafka CLI Container starten
```bash
docker run -d --add-host=conduktor-gateway:10.32.6.195 --name kafka-cli apache/kafka:3.8.1
```

Kafka CLI aufrufen
```bash
docker exec --workdir /opt/kafka/bin/ -it kafka-cli sh
```

Kafka Umgebungsvariable setzen
```bash
export KAFKA_GW="10.32.6.195:9099"
```


### Nachrichten veröffentlichen
Nachrichten veröffentlichen
```bash
./kafka-console-producer.sh --bootstrap-server $KAFKA_GW --topic test-topic --property "parse.key=true" --property "key.separator=:"
```

Eingabeformat
```bash
Key1:Meine erste Nachricht
Key2:Meine erste Nachricht mit Key2
Key1:Meine zweite Nachricht mit Key1
```

### Nachrichten lesen
Neue Nachrichten lesen
```bash
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GW --topic test-topic
```

Alle Nachrichten lesen: Dazu Parameter `--from-beginning` anhängen
```bash
./kafka-console-consumer.sh --bootstrap-server $KAFKA_GW --topic test-topic --from-beginning
```

### Cleanup
Kafka CLI Container stoppen und löschen
```bash
docker stop kafka-cli -t 0 && docker rm kafka-cli
```