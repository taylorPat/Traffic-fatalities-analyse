import pyspark
from pyspark.sql import SparkSession, DataFrame, types
from pyspark.sql.functions import to_timestamp, col, round, year, month, dayofweek


def create_parquet_files(
    temporary_dir: str, csv_file_path: str, schema: types.StructType
):
    spark_session = _create_spark_session()
    df = spark_session.read.option("header", "true").schema(schema).csv(csv_file_path)

    df = _rename_columns(df=df)
    df = _format_datatime(df=df)
    df = _add_columns(df=df)
    return _save_as_parquet(df=df, repartition=12, temporary_dir=temporary_dir)


def _create_spark_session():
    return SparkSession.builder.master("local[*]").appName("test").getOrCreate()


def _rename_columns(df: DataFrame) -> DataFrame:
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


def _format_datatime(df: DataFrame) -> DataFrame:
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


def _add_columns(df: DataFrame) -> DataFrame:
    return (
        df.withColumn("year", year(col("start_datetime")))
        .withColumn("month", month(col("start_datetime")))
        .withColumn("day_of_week", dayofweek(col("start_datetime")))
    )


def _save_as_parquet(df: DataFrame, repartition: int, temporary_dir: str):
    print("Save as parquet files...")
    parquet_file_dir = f"{temporary_dir}/parquet"
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
    ).write.parquet(parquet_file_dir, mode="overwrite")
    return parquet_file_dir
