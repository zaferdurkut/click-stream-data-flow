import os

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("ClickStreamSparkConsumer")
    .master(os.getenv("SPARK_SERVER_HOST"))
    .getOrCreate()
)

if __name__ == "__main__":
    # reading stream data
    ds2 = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", os.getenv("KAFKA_SERVERS"))
        .option(
            "subscribe",
            f"{os.getenv('KAFKA_TOPIC')},{os.getenv('KAFKA_METADATA_TOPIC')}",
        )
        .load()
    )
    # TODO: Data Aggregation with click_stream and click_stream_metadata after write parquet

    target_parquet = (
        ds2.writeStream.format("parquet")
        .outputMode("append")
        .option("path", os.getenv("PARQUET_DESTINATION_PATH"))
        .partitionBy("col")
        .trigger(processingTime="...")
        .option("checkpointLocation", os.getenv("CHECK_POINT_LOCATION"))
        .start()
    )
    target_parquet.awaitTermination()
