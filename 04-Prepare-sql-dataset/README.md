```sql
-- create partition
CREATE OR REPLACE TABLE `traffic-fatalities-455213.parking_transactions.parking_partitioned` 
PARTITION BY 
  DATE(start_datetime)
AS
SELECT
    *
FROM
    `traffic-fatalities-455213.parking_transactions.parking`;

-- create partition and cluster
-- did not create partitions
CREATE OR REPLACE TABLE `traffic-fatalities-455213.parking_transactions.parking_partitioned_3` 
PARTITION BY 
  DATE(start_datetime)
CLUSTER BY
  month
AS
SELECT
    *
FROM
    `traffic-fatalities-455213.parking_transactions.parking`;

-- did not work
CREATE OR REPLACE TABLE `traffic-fatalities-455213.parking_transactions.parking_partitioned` 
PARTITION BY 
--DATE(start_datetime)  -- Partitioning by the date part of the start_datetime column
--DATE(EXTRACT(YEAR FROM start_datetime), EXTRACT(MONTH FROM start_datetime), 1)
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