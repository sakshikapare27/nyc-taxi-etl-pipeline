# Databricks notebook source
# Verify that all Bronze, Silver, and Gold tables were created successfully
display(spark.sql("SHOW TABLES"))


# COMMAND ----------

# Average fare per day
display(
    spark.sql("""

    SELECT
        pickup_date,
        AVG(fare_amount) AS average_fare

    FROM gold_fact_trips

    GROUP BY pickup_date

    ORDER BY pickup_date

""")
)

# COMMAND ----------

# Total Revenue
display(
    spark.sql("""

    SELECT
        pickup_date,
        SUM(total_amount) AS total_revenue

    FROM gold_fact_trips

    GROUP BY pickup_date

    ORDER BY pickup_date

""")
)

# COMMAND ----------

# Total pickup locations
display(
    spark.sql("""

    SELECT
        PULocationID,
        COUNT(*) AS total_trips

    FROM gold_fact_trips

    GROUP BY PULocationID

    ORDER BY total_trips DESC

    LIMIT 10

""")
)

# COMMAND ----------

# Average trip duration
display(
    spark.sql("""

    SELECT
        PULocationID,
        AVG(trip_duration) AS avg_trip_duration

    FROM gold_fact_trips

    GROUP BY PULocationID

    ORDER BY avg_trip_duration DESC

    LIMIT 10

""")
)


# COMMAND ----------

