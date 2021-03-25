import json
import logging
import os
from time import sleep

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)


class ClickStreamProducer:
    """Push Kafka for messages and write to Cassandra."""

    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_SERVERS"),
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
        self.topic = os.getenv("KAFKA_TOPIC")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kafka_producer.flush()

    def send(self):
        """Connect to Kafka and  push message to Topic"""
        for e in range(200):
            item = {"item": e}
            self.kafka_producer.send(self.topic, item)
            print(e)
            sleep(1)


if __name__ == "__main__":
    ClickStreamProducer().send()
