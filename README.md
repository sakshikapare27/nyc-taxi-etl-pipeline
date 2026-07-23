The Scenario
Your organization has been commissioned by a city planning committee to analyze taxi usage patterns to optimize urban traffic flow. You are provided with a multi-year archive of raw trip records. The data is massive, stored in Parquet format, and includes noisy timestamps, GPS coordinates, and varied fare structures.

 Overview
The goal is to build an ETL (Extract, Transform, Load) pipeline using Apache Spark in Databricks. The pipeline reads raw NYC Taxi trip data from Parquet files, transforms it for analysis, creates an analytical data model (Star Schema), and loads it into Delta tables for reliable querying and dashboards.
Tools Used – 
1.	Databricks 
2.	Apache Spark 
3.	 Delta Lake 
4.	 Parquet Files 
5.	 Spark SQL


	 Setup

1.	  Create a Volume in Databricks (taxi_data).
2.	  Upload the Parquet file
3.	  Open a Databricks notebook and run the pipeline code

  Pipline Setup
1. Bronze Layer (Extract)
•	Uploaded the Parquet file into a Databricks Volume (dbfs:/Volumes/workspace/default/taxi_data/...).
•	Read the file into a Spark DataFrame (df).
•	Displayed sample records and printed schema.
•	Saved raw data into a Delta table (bronze_taxi_trips).
This preserves the original dataset. If later transformations fail, I can always return to the raw source.


2. Silver Layer (Transform)
•	Converted pickup and dropoff times into proper timestamps.
•	New columns:
o	pickup_date (for partitioning and date analysis).
o	trip_duration_sec (dropoff − pickup).
•	Applied data quality checks:
o	Negative fare amounts.
o	Trip duration ≤ 0.
•	Separated invalid records into a quarantine table (silver_quarantine_trips).
•	Stored cleaned records in silver_clean_trips.

 Bad data should not be used for reporting. Quarantining invalid records allows later review without deleting them.


3. Gold Layer (Load + Modeling)
•	Created a Star Schema:
o	Fact Table: gold_fact_trips (fare, distance, passenger count, trip duration, etc.).
o	Dimension Tables:
	gold_dim_date (date, year, month, weekday).
	gold_dim_geography (pickup location and dropoff location).
•	Partitioned fact table by pickup_date.
Star Schema is a standard warehouse design. It simplifies queries and improves performance.    Partitioning ensures queries only scan relevant dates instead of the entire dataset.

	Dashboards
A Databricks dashboard was created to demonstrate analytical capabilities. 
The dashboard includes: 
1. Average Fare Trend 
2. Total Revenue 
3. Top Pickup Locations 
4. Average Trip Duration 
 These visualizations query the Gold layer. Because the Fact table is partitioned by     pickup_date, date-based dashboard queries only scan the required partitions.    

	Conclusion
The pipeline ingests raw Parquet files, validates and cleans the data, isolates invalid records, creates a Star Schema, optimizes query performance through partitioning, and delivers analytics-ready tables for reporting and dashboards.
