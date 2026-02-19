"""
Data Cleaning Module
Data quality checks and cleaning operations.
"""

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, when, isnan


def check_nulls(df: DataFrame, table_name: str, key_columns: list):
    """
    Check for null values in key columns.
    
    Args:
        df (DataFrame): DataFrame to check
        table_name (str): Name of table (for logging)
        key_columns (list): List of columns that should not have nulls
    
    Returns:
        dict: Null counts per column
    """
    print(f"\n  Checking nulls in {table_name}...")
    
    null_counts = {}
    has_nulls = False
    
    for col_name in key_columns:
        null_count = df.filter(col(col_name).isNull()).count()
        null_counts[col_name] = null_count
        
        if null_count > 0:
            print(f"    ⚠️  {col_name}: {null_count:,} null values")
            has_nulls = True
    
    if not has_nulls:
        print(f"    ✓ No nulls in key columns")
    
    return null_counts


def check_duplicates(df: DataFrame, table_name: str, key_columns: list):
    """
    Check for duplicate records based on key columns.
    
    Args:
        df (DataFrame): DataFrame to check
        table_name (str): Name of table (for logging)
        key_columns (list): List of columns that form the primary key
    
    Returns:
        int: Number of duplicate records
    """
    print(f"\n  Checking duplicates in {table_name}...")
    
    total_rows = df.count()
    distinct_rows = df.select(key_columns).distinct().count()
    duplicates = total_rows - distinct_rows
    
    if duplicates > 0:
        print(f"    ⚠️  {duplicates:,} duplicate records found")
    else:
        print(f"    ✓ No duplicates found")
    
    return duplicates


def check_row_counts(dataframes: dict):
    """
    Sanity check row counts against expected ranges.
    
    Args:
        dataframes (dict): Dictionary of DataFrames
    
    Returns:
        bool: True if all row counts are reasonable
    """
    print("\n  Sanity checking row counts...")
    
    expected_ranges = {
        "orders": (1_000_000, 10_000_000),  # ~3.4M expected
        "order_products_prior": (10_000_000, 50_000_000),  # ~32M expected
        "order_products_train": (100_000, 5_000_000),  # ~1.3M expected
        "products": (10_000, 100_000),  # ~50K expected
        "aisles": (100, 500),  # ~134 expected
        "departments": (10, 50),  # ~21 expected
    }
    
    all_valid = True
    
    for table_name, (min_rows, max_rows) in expected_ranges.items():
        actual_rows = dataframes[table_name].count()
        
        if min_rows <= actual_rows <= max_rows:
            print(f"    ✓ {table_name}: {actual_rows:,} rows (within expected range)")
        else:
            print(f"    ⚠️  {table_name}: {actual_rows:,} rows (expected {min_rows:,} to {max_rows:,})")
            all_valid = False
    
    return all_valid


def run_data_quality_checks(dataframes: dict):
    """
    Run comprehensive data quality checks on raw data.
    
    Args:
        dataframes (dict): Dictionary of raw DataFrames
    
    Returns:
        dict: Data quality report
    """
    print("\n" + "=" * 60)
    print("DATA QUALITY CHECKS")
    print("=" * 60)
    
    dq_report = {
        "nulls": {},
        "duplicates": {},
        "row_counts_valid": False,
        "overall_pass": False,
    }
    
    # Check nulls in key columns
    print("\n[1/3] Checking for null values in key columns...")
    dq_report["nulls"]["orders"] = check_nulls(
        dataframes["orders"], "orders", ["order_id", "user_id", "order_number"]
    )
    dq_report["nulls"]["order_products_prior"] = check_nulls(
        dataframes["order_products_prior"], "order_products_prior", ["order_id", "product_id"]
    )
    dq_report["nulls"]["order_products_train"] = check_nulls(
        dataframes["order_products_train"], "order_products_train", ["order_id", "product_id"]
    )
    dq_report["nulls"]["products"] = check_nulls(
        dataframes["products"], "products", ["product_id", "product_name"]
    )
    dq_report["nulls"]["aisles"] = check_nulls(
        dataframes["aisles"], "aisles", ["aisle_id", "aisle"]
    )
    dq_report["nulls"]["departments"] = check_nulls(
        dataframes["departments"], "departments", ["department_id", "department"]
    )
    
    # Check duplicates
    print("\n[2/3] Checking for duplicate records...")
    dq_report["duplicates"]["orders"] = check_duplicates(
        dataframes["orders"], "orders", ["order_id"]
    )
    dq_report["duplicates"]["order_products_prior"] = check_duplicates(
        dataframes["order_products_prior"], "order_products_prior", ["order_id", "product_id"]
    )
    dq_report["duplicates"]["order_products_train"] = check_duplicates(
        dataframes["order_products_train"], "order_products_train", ["order_id", "product_id"]
    )
    dq_report["duplicates"]["products"] = check_duplicates(
        dataframes["products"], "products", ["product_id"]
    )
    dq_report["duplicates"]["aisles"] = check_duplicates(
        dataframes["aisles"], "aisles", ["aisle_id"]
    )
    dq_report["duplicates"]["departments"] = check_duplicates(
        dataframes["departments"], "departments", ["department_id"]
    )
    
    # Check row counts
    print("\n[3/3] Sanity checking row counts...")
    dq_report["row_counts_valid"] = check_row_counts(dataframes)
    
    # Overall assessment
    has_critical_nulls = any(
        sum(nulls.values()) > 0 for nulls in dq_report["nulls"].values()
    )
    has_duplicates = any(dup > 0 for dup in dq_report["duplicates"].values())
    
    dq_report["overall_pass"] = (
        not has_critical_nulls and not has_duplicates and dq_report["row_counts_valid"]
    )
    
    print("\n" + "=" * 60)
    if dq_report["overall_pass"]:
        print("✓ DATA QUALITY CHECKS PASSED")
    else:
        print("⚠️  DATA QUALITY CHECKS FAILED")
        if has_critical_nulls:
            print("  - Null values found in key columns")
        if has_duplicates:
            print("  - Duplicate records found")
        if not dq_report["row_counts_valid"]:
            print("  - Row counts outside expected ranges")
    print("=" * 60)
    
    return dq_report


def clean_data(dataframes: dict) -> dict:
    """
    Clean raw data by removing nulls, duplicates, and invalid records.
    
    Args:
        dataframes (dict): Dictionary of raw DataFrames
    
    Returns:
        dict: Dictionary of cleaned DataFrames
    """
    print("\n" + "=" * 60)
    print("CLEANING DATA")
    print("=" * 60)
    
    cleaned = {}
    
    # Clean orders - remove nulls in key columns
    print("\n  Cleaning orders...")
    orders_clean = dataframes["orders"].dropna(subset=["order_id", "user_id", "order_number"])
    orders_clean = orders_clean.dropDuplicates(["order_id"])
    print(f"    ✓ Orders: {dataframes['orders'].count():,} → {orders_clean.count():,} rows")
    cleaned["orders"] = orders_clean
    
    # Clean order_products_prior - remove nulls and duplicates
    print("\n  Cleaning order_products_prior...")
    op_prior_clean = dataframes["order_products_prior"].dropna(subset=["order_id", "product_id"])
    op_prior_clean = op_prior_clean.dropDuplicates(["order_id", "product_id"])
    print(f"    ✓ Order products (prior): {dataframes['order_products_prior'].count():,} → {op_prior_clean.count():,} rows")
    cleaned["order_products_prior"] = op_prior_clean
    
    # Clean order_products_train - remove nulls and duplicates
    print("\n  Cleaning order_products_train...")
    op_train_clean = dataframes["order_products_train"].dropna(subset=["order_id", "product_id"])
    op_train_clean = op_train_clean.dropDuplicates(["order_id", "product_id"])
    print(f"    ✓ Order products (train): {dataframes['order_products_train'].count():,} → {op_train_clean.count():,} rows")
    cleaned["order_products_train"] = op_train_clean
    
    # Clean products - remove nulls and duplicates
    print("\n  Cleaning products...")
    products_clean = dataframes["products"].dropna(subset=["product_id", "product_name"])
    products_clean = products_clean.dropDuplicates(["product_id"])
    print(f"    ✓ Products: {dataframes['products'].count():,} → {products_clean.count():,} rows")
    cleaned["products"] = products_clean
    
    # Clean aisles - remove nulls and duplicates
    print("\n  Cleaning aisles...")
    aisles_clean = dataframes["aisles"].dropna(subset=["aisle_id", "aisle"])
    aisles_clean = aisles_clean.dropDuplicates(["aisle_id"])
    print(f"    ✓ Aisles: {dataframes['aisles'].count():,} → {aisles_clean.count():,} rows")
    cleaned["aisles"] = aisles_clean
    
    # Clean departments - remove nulls and duplicates
    print("\n  Cleaning departments...")
    departments_clean = dataframes["departments"].dropna(subset=["department_id", "department"])
    departments_clean = departments_clean.dropDuplicates(["department_id"])
    print(f"    ✓ Departments: {dataframes['departments'].count():,} → {departments_clean.count():,} rows")
    cleaned["departments"] = departments_clean
    
    print("\n✓ Data cleaning complete")
    print("=" * 60)
    
    return cleaned
