import pathlib
from google.cloud import storage
import os

"""
    Authenticate with Google Cloud Platform first
    4. Option: `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS` 
    with `export GOOGLE_APPLICATION_CREDENTIALS=$PWD/.credentials/.google-cloud.json`
"""


def upload_files_to_gcs(
    source_file_path: str, blob_name: str, bucket_name: str | None = None
):
    """Uploads a Parquet file to Google Cloud Storage."""
    storage_client = storage.Client(project=os.getenv("GCP_PROJECT_ID"))
    bucket = storage_client.get_bucket(bucket_name or get_env("GCP_BUCKET_NAME"))
    for file_path in pathlib.Path(source_file_path).glob(pattern="*.parquet"):
        if file_path.suffix == ".parquet":
            upload_file_to_gcs(file_path, blob_name, bucket)


def upload_file_to_gcs(file_path: pathlib.Path, blob_name: str, bucket: str):
    blob = f"{blob_name}/{file_path.name}"
    blob = bucket.blob(blob_name=blob)
    print(blob)
    blob.upload_from_filename(file_path)


def get_env(environment_variable: str):
    if (env := os.getenv(environment_variable)) is None:
        raise ValueError(f"{environment_variable} not defined.")
    return env
