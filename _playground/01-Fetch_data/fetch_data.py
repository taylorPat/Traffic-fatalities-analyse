from kaggle.api.kaggle_api_extended import KaggleApi
import pyspark
from pyspark.sql import SparkSession, types, DataFrame
from pyspark.sql.functions import to_timestamp, col, round, year, month, dayofweek
import tempfile


def main(dataset_name: str):
    download_csv_file_name = "parking_transactions.csv"
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_file_path = download_csv(
            dataset_name=dataset_name,
            download_directory=temp_dir,
            download_csv_file_name=download_csv_file_name,
        )
        create_parquet_files(csv_file_path=csv_file_path)


def download_csv(
    dataset_name: str, download_directory: str, download_csv_file_name: str
) -> str:
    api = KaggleApi()
    api.authenticate()
    _ = api.dataset_download_file(
        dataset=dataset_name,
        file_name=download_csv_file_name,
        path=download_directory,
        quiet=False,
    )
    return f"{download_directory}/{download_csv_file_name}"


def create_parquet_files(csv_file_path: str):
    spark_session = create_spark_session()
    df = spark_session.read.option("header", "true").schema(SCHEMA).csv(csv_file_path)

    df = rename_columns(df=df)
    df = format_datatime(df=df)
    df = add_columns(df=df)
    save_as_parquet(df=df, repartition=12)


def create_spark_session():
    return SparkSession.builder.master("local[*]").appName("test").getOrCreate()


def rename_columns(df: DataFrame) -> DataFrame:
    print("Rename columns...")
    return (
        df.withColumnRenamed("ID", "id")
        .withColumnRenamed("Source", "source")
        .withColumnRenamed("Duration in Minutes", "duration_in_min")
        .withColumnRenamed("Amount", "amount")
        .withColumnRenamed("Kiosk ID", "kiosk_id")
        .withColumnRenamed("App Zone ID", "app_zone_id")
        .withColumnRenamed("App Zone Group", "app_zone_group")
        .withColumnRenamed("Payment Method", "payment_method")
        .withColumnRenamed("Location Group", "location")
    )


def format_datatime(df: DataFrame) -> DataFrame:
    print("Format datetime...")
    return (
        df.withColumn(
            "start_datetime", to_timestamp("Start Time", "MM/dd/yyyy hh:mm:ss a")
        )
        .withColumn("end_datetime", to_timestamp("End Time", "MM/dd/yyyy hh:mm:ss a"))
        .withColumn(
            "modification_datetime",
            to_timestamp("Last Updated", "MM/dd/yyyy hh:mm:ss a"),
        )
        .withColumn(
            "amount_per_hour", round((col("amount") / col("duration_in_min")) * 60, 2)
        )
    )


def add_columns(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("year", year(col("start_datetime")))
        .withColumn("month", month(col("start_datetime")))
        .withColumn("day_of_week", dayofweek(col("start_datetime")))
    )


def save_as_parquet(df: DataFrame, repartition: int):
    print("Save as parquet files...")
    df = df.repartition(repartition)
    df.select(
        "id",
        "source",
        "modification_datetime",
        "start_datetime",
        "end_datetime",
        "duration_in_min",
        "amount",
        "amount_per_hour",
        "year",
        "month",
        "day_of_week",
        "app_zone_id",
        "app_zone_group",
        "payment_method",
        "location",
    ).write.parquet("parking-transactions", mode="overwrite")


SCHEMA = types.StructType(
    [
        types.StructField("ID", types.IntegerType(), True),
        types.StructField("Source", types.StringType(), True),
        types.StructField("Duration in Minutes", types.FloatType(), True),
        types.StructField("Start Time", types.StringType(), True),
        types.StructField("End Time", types.StringType(), True),
        types.StructField("Amount", types.FloatType(), True),
        types.StructField("Kiosk ID", types.IntegerType(), True),
        types.StructField("App Zone ID", types.IntegerType(), True),
        types.StructField("App Zone Group", types.StringType(), True),
        types.StructField("Payment Method", types.StringType(), True),
        types.StructField("Location Group", types.StringType(), True),
        types.StructField("Last Updated", types.StringType(), True),
    ]
)


if __name__ == "__main__":
    print("Start application...")
    main(dataset_name="aniket0712/parking-transactions")
    print("Finish application...")
