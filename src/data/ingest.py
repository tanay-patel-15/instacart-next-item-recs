"""
Data Ingestion Module
Load raw CSV files into Spark DataFrames with schema validation.
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    FloatType,
)
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.paths import (
    RAW_ORDERS,
    RAW_ORDER_PRODUCTS_PRIOR,
    RAW_ORDER_PRODUCTS_TRAIN,
    RAW_PRODUCTS,
    RAW_AISLES,
    RAW_DEPARTMENTS,
)


def get_orders_schema():
    """Define schema for orders.csv."""
    return StructType(
        [
            StructField("order_id", IntegerType(), False),
            StructField("user_id", IntegerType(), False),
            StructField("eval_set", StringType(), True),
            StructField("order_number", IntegerType(), False),
            StructField("order_dow", IntegerType(), True),
            StructField("order_hour_of_day", IntegerType(), True),
            StructField("days_since_prior_order", FloatType(), True),
        ]
    )


def get_order_products_schema():
    """Define schema for order_products__*.csv."""
    return StructType(
        [
            StructField("order_id", IntegerType(), False),
            StructField("product_id", IntegerType(), False),
            StructField("add_to_cart_order", IntegerType(), True),
            StructField("reordered", IntegerType(), True),
        ]
    )


def get_products_schema():
    """Define schema for products.csv."""
    return StructType(
        [
            StructField("product_id", IntegerType(), False),
            StructField("product_name", StringType(), False),
            StructField("aisle_id", IntegerType(), False),
            StructField("department_id", IntegerType(), False),
        ]
    )


def get_aisles_schema():
    """Define schema for aisles.csv."""
    return StructType(
        [
            StructField("aisle_id", IntegerType(), False),
            StructField("aisle", StringType(), False),
        ]
    )


def get_departments_schema():
    """Define schema for departments.csv."""
    return StructType(
        [
            StructField("department_id", IntegerType(), False),
            StructField("department", StringType(), False),
        ]
    )


def load_csv_with_schema(spark: SparkSession, file_path: Path, schema: StructType, name: str):
    """
    Load a CSV file with explicit schema validation.
    
    Args:
        spark (SparkSession): Active Spark session
        file_path (Path): Path to CSV file
        schema (StructType): Expected schema
        name (str): Table name (for logging)
    
    Returns:
        DataFrame: Loaded DataFrame
    """
    print(f"  Loading {name}...")
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = spark.read.csv(str(file_path), header=True, schema=schema)
    
    row_count = df.count()
    col_count = len(df.columns)
    
    print(f"    ✓ {name}: {row_count:,} rows, {col_count} columns")
    
    return df


def load_raw_data(spark: SparkSession):
    """
    Load all raw CSV files from data/raw/ into Spark DataFrames.
    
    Args:
        spark (SparkSession): Active Spark session
    
    Returns:
        dict: Dictionary of DataFrames keyed by table name
            - orders: Orders DataFrame
            - order_products_prior: Prior order products DataFrame
            - order_products_train: Train order products DataFrame
            - products: Products DataFrame
            - aisles: Aisles DataFrame
            - departments: Departments DataFrame
    """
    print("\n" + "=" * 60)
    print("LOADING RAW DATA")
    print("=" * 60)
    
    dataframes = {}
    
    # Load orders
    dataframes["orders"] = load_csv_with_schema(
        spark, RAW_ORDERS, get_orders_schema(), "orders.csv"
    )
    
    # Load order products (prior)
    dataframes["order_products_prior"] = load_csv_with_schema(
        spark, RAW_ORDER_PRODUCTS_PRIOR, get_order_products_schema(), "order_products__prior.csv"
    )
    
    # Load order products (train)
    dataframes["order_products_train"] = load_csv_with_schema(
        spark, RAW_ORDER_PRODUCTS_TRAIN, get_order_products_schema(), "order_products__train.csv"
    )
    
    # Load products
    dataframes["products"] = load_csv_with_schema(
        spark, RAW_PRODUCTS, get_products_schema(), "products.csv"
    )
    
    # Load aisles
    dataframes["aisles"] = load_csv_with_schema(
        spark, RAW_AISLES, get_aisles_schema(), "aisles.csv"
    )
    
    # Load departments
    dataframes["departments"] = load_csv_with_schema(
        spark, RAW_DEPARTMENTS, get_departments_schema(), "departments.csv"
    )
    
    print("\n✓ All raw data loaded successfully")
    print("=" * 60)
    
    return dataframes


def validate_schemas(dataframes: dict):
    """
    Validate that loaded DataFrames have expected schemas.
    
    Args:
        dataframes (dict): Dictionary of DataFrames
    
    Returns:
        bool: True if all schemas are valid
    """
    print("\n" + "=" * 60)
    print("VALIDATING SCHEMAS")
    print("=" * 60)
    
    expected_columns = {
        "orders": ["order_id", "user_id", "eval_set", "order_number", "order_dow", "order_hour_of_day", "days_since_prior_order"],
        "order_products_prior": ["order_id", "product_id", "add_to_cart_order", "reordered"],
        "order_products_train": ["order_id", "product_id", "add_to_cart_order", "reordered"],
        "products": ["product_id", "product_name", "aisle_id", "department_id"],
        "aisles": ["aisle_id", "aisle"],
        "departments": ["department_id", "department"],
    }
    
    all_valid = True
    
    for table_name, expected_cols in expected_columns.items():
        df = dataframes[table_name]
        actual_cols = df.columns
        
        if actual_cols == expected_cols:
            print(f"  ✓ {table_name}: Schema valid")
        else:
            print(f"  ✗ {table_name}: Schema mismatch")
            print(f"    Expected: {expected_cols}")
            print(f"    Actual: {actual_cols}")
            all_valid = False
    
    if all_valid:
        print("\n✓ All schemas validated successfully")
    else:
        print("\n✗ Schema validation failed")
    
    print("=" * 60)
    
    return all_valid
