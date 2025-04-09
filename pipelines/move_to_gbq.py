import os
from app.gbq import list_files_from_gcs, load_parquet_to_bigquery


def main(table_name: str, folder_name: str, dataset: str | None = None):
    """
    A pipeline script for creating a new table inside Google Big Query
    based on parquet files listed within a specified folder.
    """
    dataset = os.getenv("GCP_BQ_DATASET")
    if dataset is None:
        raise ValueError("GCP_BQ_DATASET not defined")
        
    for file_name in list_files_from_gcs(folder_name=folder_name):
        load_parquet_to_bigquery(
            file_name=file_name, dataset_id=dataset, table_id=table_name
        )

