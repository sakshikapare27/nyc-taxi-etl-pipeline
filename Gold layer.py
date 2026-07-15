# Databricks notebook source
# GOLD LAYER
# STAR SCHEMA
from pyspark.sql.functions import *

# STEP 1 : Read Clean Silver Data

clean_df = spark.table("silver_clean_trips")

display(clean_df)

# COMMAND ----------

# Create Fact table
fact_trips = clean_df.select(
    "VendorID",
    "pickup_date",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
    "trip_duration",
    "payment_type"
)


# COMMAND ----------

# Create Geography dimensions
dim_geography = clean_df.select(
    "PULocationID",
    "DOLocationID"
).distinct()

# COMMAND ----------

# Create Date dimensions
dim_date = clean_df.select("pickup_date").distinct()

dim_date = (
    dim_date
    .withColumn("year", year("pickup_date"))
    .withColumn("month", month("pickup_date"))
    .withColumn("day", dayofmonth("pickup_date"))
    .withColumn("weekday", dayofweek("pickup_date"))
)

# COMMAND ----------

# Load Fact table
fact_trips.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("pickup_date") \
    .saveAsTable("gold_fact_trips")

# COMMAND ----------

# Load Geography dimensions
dim_geography.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_dim_geography")


# COMMAND ----------

# Load date dimensions
dim_date.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_dim_date")

print("Gold tables created successfully.")

# COMMAND ----------

