# Conduktor

- **E-Mail:** admin@example.com
- **Password:** admin_password

# Commands

## Create Topic

```shell
kafka-topics --create --topic test-topic --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
```



## Produce Message
```shell
kafka-console-producer --topic test-topic --bootstrap-server kafka1:9092
```



## Consume Messages

```shell
kafka-console-consumer --topic test-topic --bootstrap-server kafka1:9092 --from-beginning
```
