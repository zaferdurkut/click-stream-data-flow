import os
import json
import io
import kafka
import logging
import avro.io

logging.basicConfig(level=logging.INFO)


def read_data(msg: str, schema: dict):
    bytes_reader = io.BytesIO(msg.value)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    return reader.read(decoder)


class ClickStreamConsumer:
    """Listen Kafka for messages and write to Cassandra."""

    kafka_consumer = None
    click_stream = None

    def __init__(self):
        self.set_kafka_consumer()

    def set_kafka_consumer(self):
        """Set consumer"""
        try:
            self.kafka_consumer = kafka.KafkaConsumer(
                os.getenv("KAFKA_TOPIC"),
                group_id=os.getenv("KAFKA_CONSUMER_GROUP"),
                bootstrap_servers=os.getenv("KAFKA_SERVERS"),
            )
        except kafka.errors.NoBrokersAvailable:
            raise ConnectionError("Queue connection lost.")

    def run(self):
        """Connect to Kafka and  write message to Cassandra (Consuming data)"""
        for msg in self.kafka_consumer:
            # data = read_data(msg, self.kafka_schema)
            logging.info(msg)
            print("aldim")


ClickStreamConsumer().run()
