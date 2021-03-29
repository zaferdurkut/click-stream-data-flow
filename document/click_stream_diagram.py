from diagrams import Cluster, Diagram
from diagrams.onprem.analytics import Spark
from diagrams.onprem.client import Client
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Hive
from diagrams.generic.storage import Storage


# Documentation: https://diagrams.mingrammer.com/docs/getting-started/installation#quick-start
with Diagram("Click Stream Architecture", show=False):
    with Cluster("Docker Compose"):
        producer = Client("Procuder")

        kafdrop = Client("Kafdrop UI")

        with Cluster("Kafka"):
            click_stream_topics = [Kafka("Click Stream"), Kafka("Click Stream Metadata")]

        consumer = Client("Consumer")

        with Cluster("Spark"):
            spark_master = Spark("master")
            spark_worker_1 = Spark("worker-1")
            spark_worker_2 = Spark("worker-2")

        parquet = Storage("Parquet File")

        click_stream_topics >> kafdrop
        producer >> click_stream_topics
        click_stream_topics >> consumer
        consumer >> spark_master >> parquet
