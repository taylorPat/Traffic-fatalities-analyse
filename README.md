# Parking transactions analysis

# TODO: IaC with terraform

## TLDR;
This project analyzes US parking transaction data to identify patterns in weekday and monthly transaction distributions, providing insights to optimize parking policies and infrastructure.

**Tools used within this project**  
🐍 Python for defining pipeline scripts  
🔥 Apache Spark for data batch processing and transformation  
☁️ Google Cloud Storage as Data Lake for storing .parquet files  
🏗️ Google Cloud BigQuery as Data Warehouse  
📊 Google Looker Studio for visualization

**Dataset**  
[Parking Transaction](https://www.kaggle.com/datasets/aniket0712/parking-transactions) dataset.

**Output**  
> [!NOTE]
> The dashboard can be found [here](https://lookerstudio.google.com/reporting/f80ea899-3c74-466c-8167-719864046e90)

![alt text](attachments/dashboard.png)


## Problem Description

The goal of this data engineering project is to analyze parking transaction data across the United States in order to identify patterns and trends related to parking behaviors. The dataset consists of transaction records, including timestamps and other relevant metadata, such as location and transaction amount whereby the location and transactin amount have not been considered until now (but can be added in another iteration). The project focuses on providing insights into the temporal distribution of parking transactions, specifically across weekdays and months of the year.

**Two key visualizations will be generated to support this analysis:**

- Weekday Distribution of Transactions: This plot will display the relative distribution of parking transactions across different weekdays, helping to understand which days of the week experience the highest and lowest parking activity. This could reveal insights into peak parking demand on specific weekdays and assist cities or businesses in optimizing parking policies, pricing models, or enforcement strategies.

- Monthly Transaction Distribution: This plot will visualize the number of parking transactions by month throughout the year, offering insights into seasonal trends and fluctuations in parking demand. This analysis will help in understanding whether parking transactions tend to increase during certain months (e.g., summer or holiday periods) and can assist in predicting future demand patterns.

By analyzing these two visualizations, the project aims to uncover temporal trends in parking behavior across different regions, ultimately providing actionable insights that can inform urban planning, parking infrastructure development, and policy decisions to better serve users and optimize parking resources.

## Technical details
### Cloud
The project is developed inside Google Cloud Platform leveraging Google Cloud Storage as data lake and Google BigQuery as data warehouse.

### Data ingestion
There is an end-to-end pipeline ([end_to_end.py](/pipelines/end_to_end.py)) which includes:
- Downloading the data from kaggle as _.csv_ file to a temporary directory
- Reading the _.csv_ file with spark, renaming and adding columns, formating datetime colums, creating and applying a schema and saving the dataframe as _.parquet_ files using repartition in a temporary directory
- Uploading the _.parquet_ files to Google Cloud Storage
- Inserting the data from Google Cloud Storage to Google Big Query table called _parking_

> [!HINT]  
> The **[end_to_end.py](/pipelines/end_to_end.py)** pipeline combines **[fetch_and_upload_to_gcs.py](/pipelines/fetch_and_upload_to_gcs.py)** pipeline wich is responsible for uploading data to Google Cloud Storage and **[move_to_gbq.py](/pipelines/move_to_gbq.py)** which moves the data to Google BigQuery.

### Data warehouse
Based on the _parking_ table two further tables are created using partition in order to make optimize the queries for upstream queries.

For the left tile in the dashboard which shows the relative distribution of the parking transactions over the weekdays a partition by the day_of_week column (which was extracted from the start_datetime column using pyspark inside the pipeline and defines the days of the week as integer) was implemented because the tile uses just the information about the days of the week.
```sql
-- Partition by weekday
CREATE OR REPLACE TABLE `traffic-fatalities-455213.parking_transactions.parking_partition_by_weekday`
PARTITION BY
  RANGE_BUCKET(day_of_week, GENERATE_ARRAY(1, 7, 1))
AS
SELECT
    *,
    CASE 
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 1 THEN 'Sunday'
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 2 THEN 'Monday'
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 3 THEN 'Tuesday'
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 4 THEN 'Wednesday'
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 5 THEN 'Thursday'
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 6 THEN 'Friday'
      WHEN EXTRACT(DAYOFWEEK FROM start_datetime) = 7 THEN 'Saturday'
    END AS day_of_week_str,
FROM
    `traffic-fatalities-455213.parking_transactions.parking`;
```

For the tiles on the right side which shows the amount of transactions over the different month a partition by the month column (which was extracted from the start_datetime column using pyspark inside the pipeline and defines the month as integer) was considered reasonable because the data is sorted by month.
```sql
-- Partition by month
CREATE OR REPLACE TABLE `traffic-fatalities-455213.parking_transactions.parking_partition_by_month`
PARTITION BY
  RANGE_BUCKET(month, GENERATE_ARRAY(1, 12, 1))
AS
SELECT *  FROM `traffic-fatalities-455213.parking_transactions.parking`;
```

### Transformations

### Dashboard

### Reproducibility