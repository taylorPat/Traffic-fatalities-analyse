# Architecture

## Workflow

### 1. Get data from source and save it into destination storage

- Source: [FARS Dataset](https://www.nhtsa.gov/file-downloads?p=nhtsa/downloads/FARS/)
- Source file format: _.csv_
- Destination: Google Cloud Storage Bucket "FARS_csv"
- Destination file format: _.csv_

Iteration 1:

- Understand the pattern of the source file locations
- Use a jupyter notebook for dowloading one dataset (make use of a tool from the zoomcamp like dlt)
- Examine the dataset (What columns does it have, what are the values, what are the types of the values, should some types be transformed,...)
- Upload the dataset to the destination location

Iteration 2:

- Automate the download of the data by using a template derived from the pattern found in iteration 1

Iteration 3:

- Orchestrate a workflow using Kestra

### 2. Take the data from the destination storage and change the file format

- Source: Google Cloud Storage Bucket "FARS_csv"
- Source file format: _.csv_

- Destination: Google Cloud Storage Bucket "FARS_parquet"
- Destination file format: _.parquet_

Iteration 1:

- Use a jupyter notebook for transforming the _.csv_ files into _.parquet_ files
- Consider mapping the column types if necessary, drop columns, insert columns, adapt columns, ...
- Make use of Apache Spark

Iteration 2:

- Orchestrate a workflow using Kestra

Iteration 3:

- Think about Google dataproc
