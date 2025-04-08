from app.gbq import list_files_from_gcs, load_parquet_to_bigquery


def main(dataset: str, table_name: str, folder_name: str):
    """
    A pipeline script for creating a new table inside Google Big Query
    based on parquet files listed within a specified folder.
    """
    for file_name in list_files_from_gcs(folder_name=folder_name):
        load_parquet_to_bigquery(
            file_name=file_name, dataset_id=dataset, table_id=table_name
        )


if __name__ == "__main__":
    main(dataset="parking_transactions", table_name="parking", folder_name="parquet")
