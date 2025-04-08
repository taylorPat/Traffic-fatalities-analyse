import tempfile

from app.download_csv_data import download_csv
from app.gcs import upload_files_to_gcs
from app.schema import SCHEMA
from app.spark_functions import create_parquet_files


def main(dataset_name: str, download_csv_file_name: str):
    """
    A pipeline script for downloading 'aniket0712/parking-transactions' dataset
    from kaggle, transform it using pyspark, save it as parquet files and upload
    those parquet files to Google Cloud Storage.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        csv_file_path = download_csv(
            dataset_name=dataset_name,
            download_directory=temp_dir,
            download_csv_file_name=download_csv_file_name,
        )
        parquet_dir = create_parquet_files(
            temporary_dir=temp_dir, csv_file_path=csv_file_path, schema=SCHEMA
        )
        upload_files_to_gcs(source_file_path=parquet_dir, blob_name="parquet")


if __name__ == "__main__":
    main(
        dataset_name="aniket0712/parking-transactions",
        download_csv_file_name="parking_transactions.csv",
    )
