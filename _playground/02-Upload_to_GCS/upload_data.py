import pathlib
from google.cloud import storage
import os

def upload_parquet_to_gcs(
    source_file_path: str, blob_name: str, bucket_name: str | None = None
):
    """Uploads a Parquet file to Google Cloud Storage."""
    storage_client = storage.Client(project=os.getenv("GCP_PROJECT_ID"))
    bucket = storage_client.get_bucket(bucket_name or os.getenv("GCP_BUCKET_NAME"))
    for file_path in pathlib.Path(source_file_path).iterdir():
        blob = f"{blob_name}/{file_path.name}"
        blob = bucket.blob(blob_name=blob)
        print(blob)
        blob.upload_from_filename(file_path)


if __name__ == "__main__":
    upload_parquet_to_gcs(
        source_file_path="/home/patrick/Traffic-fatalities-analyse/parking-transactions",
        blob_name="parquet",
    )
