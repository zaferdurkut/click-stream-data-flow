# Click Stream Data Flow
To build it:
```sh
docker-compose up --build
```

### list of topics on kafka container
```sh
./opt/kafka_2.13-2.7.0/bin/kafka-topics.sh --list --zookeeper zookeeper:2181
```

### kafka stream data on kafka container
```sh
./opt/kafka_2.13-2.7.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic click_stream --from-beginning
```

