"""
Spark Session Configuration
Centralized Spark configuration for the Instacart recommendation project.
"""

from pyspark.sql import SparkSession


def get_spark_session(app_name="InstacartRecs", driver_memory="8g", executor_memory="4g"):
    """
    Create and configure a Spark session.
    
    Args:
        app_name (str): Name of the Spark application
        driver_memory (str): Driver memory allocation (e.g., "4g")
        executor_memory (str): Executor memory allocation (e.g., "2g")
    
    Returns:
        SparkSession: Configured Spark session
    """
    spark = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.driver.memory", driver_memory)
        .config("spark.executor.memory", executor_memory)
        .config("spark.sql.shuffle.partitions", "200")
        .config("spark.default.parallelism", "8")
        .getOrCreate()
    )
    
    # Set log level to reduce verbosity
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def stop_spark_session(spark):
    """
    Stop the Spark session and release resources.
    
    Args:
        spark (SparkSession): Spark session to stop
    """
    if spark:
        spark.stop()
