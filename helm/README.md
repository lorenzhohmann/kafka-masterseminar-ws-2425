# Helm Chart to deploy Apache Kafka in Kubernetes

## Install

```shell
helm upgrade kafka-cluster . --namespace kafka --create-namespace
```

## Uninstall

```shell
helm uninstall kafka-cluster --namespace kafka
```

