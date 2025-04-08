from pipelines.fetch_and_upload_to_gcs import main as fetch_data_transform_and_upload
from pipelines.move_to_gbq import main as move_from_gcs_to_gbq

if __name__ == "__main__":
    fetch_data_transform_and_upload(
        dataset_name="aniket0712/parking-transactions",
        download_csv_file_name="parking_transactions.csv",
    )
    move_from_gcs_to_gbq(dataset="parking_transactions", table_name="parking", folder_name="parquet")