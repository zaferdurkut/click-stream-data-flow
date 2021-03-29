import json
import logging
import os
from time import sleep
from typing import List

import pandas as pd

from kafka import KafkaProducer
from pandas import DataFrame

from utils.utils import find_paths

logging.basicConfig(level=logging.INFO)


class ClickStreamProducer:
    """Push Kafka for messages and write to Cassandra."""

    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_SERVERS"),
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
        self.topic = os.getenv("KAFKA_TOPIC")
        self.metadata_topic = os.getenv("KAFKA_METADATA_TOPIC")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.kafka_producer.flush()

    def main(self) -> None:
        sleep(int(os.getenv("PRODUCER_DOCKER_INITIALIZE_WAIT_TIME", 60)))
        wait_time = int(os.getenv("PRODUCER_ITEM_WAIT_TIME", 0))

        csv_file_paths = ClickStreamProducer.get_csv_data(
            data_directory_from_root=os.getenv("PRODUCER_DATA_ROOT_DIRECTORY")
        )
        for csv_file_path in csv_file_paths:
            if (
                os.getenv("PRODUCER_CLICK_CSV_DATA_PREFIX") in csv_file_path
            ):  # clicks data
                click_dataframe = ClickStreamProducer.read_csv(
                    file_path_from_root=csv_file_path
                )
                for item in click_dataframe.to_dict(orient="records"):
                    sleep(wait_time)
                    self.send(topic=self.topic, item=item)
            elif (
                os.getenv("PRODUCER_CLICK_METADATA_CSV_DATA_PREFIX") in csv_file_path
            ):  # clicks metadata
                click_metadata_dataframe = ClickStreamProducer.read_csv(
                    file_path_from_root=csv_file_path
                )
                for item in click_metadata_dataframe.to_dict(orient="records"):
                    sleep(wait_time)
                    self.send(topic=self.metadata_topic, item=item)
            else:
                logging.warning(csv_file_path + " data is not matched prefix")

    def send(self, topic: str, item: dict) -> None:
        """Connect to Kafka and  push message to Topic"""

        self.kafka_producer.send(topic=topic, value=item).add_callback(
            ClickStreamProducer.on_send_success
        ).add_errback(ClickStreamProducer.on_send_error)

    @staticmethod
    def on_send_success(record_metadata):
        logging.info(
            "Topic: "
            + str(record_metadata.topic)
            + " Partition: "
            + str(record_metadata.partition)
            + " Offset: "
            + str(record_metadata.offset)
        )

    @staticmethod
    def on_send_error(excp):
        logging.error(excp)

    @staticmethod
    def get_csv_data(data_directory_from_root: str) -> List[str]:
        return find_paths(
            directory=os.getenv("PARENT_DIRECTORY_PREFIX", "../")
            + data_directory_from_root,
            suffix=os.getenv("CSV_SUFFIX", ".csv"),
        )

    @staticmethod
    def read_csv(file_path_from_root: str) -> DataFrame:
        return pd.read_csv(
            os.getenv("PARENT_DIRECTORY_PREFIX", "../") + file_path_from_root
        )


if __name__ == "__main__":
    ClickStreamProducer().main()
