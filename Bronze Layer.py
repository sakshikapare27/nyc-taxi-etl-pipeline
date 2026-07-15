# Databricks notebook source
df = spark.read.parquet(
    "/Volumes/workspace/default/taxi_data/yellow_tripdata_2026-05.parquet"
)

display(df)

# COMMAND ----------

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

print(df.count())

# COMMAND ----------

# Save raw data as Bronze Delta table

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("bronze_taxi_trips")

print("Bronze table created successfully.")

# COMMAND ----------

