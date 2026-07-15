# Databricks notebook source
# SILVER LAYER - TRANSFORM
from pyspark.sql.functions import *

# STEP 1 : Read Bronze Table
df = spark.table("bronze_taxi_trips")
display(df)

# COMMAND ----------

# Create pickup_date for partitioning

df = df.withColumn(
    "pickup_date",
    to_date(col("tpep_pickup_datetime"))
)

# Calculate trip duration in seconds

df = df.withColumn(
    "trip_duration",
    unix_timestamp(col("tpep_dropoff_datetime"))
    -
    unix_timestamp(col("tpep_pickup_datetime"))
)

# COMMAND ----------

# Data Quality checks
invalid_df = df.filter(
    (col("fare_amount") < 0) |
    (col("trip_duration") <= 0) |
    (col("PULocationID").isNull()) |
    (col("DOLocationID").isNull())
)

display(invalid_df)

# COMMAND ----------

# Create clean dataset
clean_df = df.filter(
    (col("fare_amount") >= 0) &
    (col("trip_duration") > 0) &
    (col("PULocationID").isNotNull()) &
    (col("DOLocationID").isNotNull())
)

display(clean_df)

# COMMAND ----------

print(f"Total Records : {df.count()}")
print(f"Valid Records : {clean_df.count()}")
print(f"Invalid Records : {invalid_df.count()}")

# COMMAND ----------

clean_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_clean_trips")

invalid_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_quarantine_trips")

print("Silver tables created successfully.")

# COMMAND ----------

