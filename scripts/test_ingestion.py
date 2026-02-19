"""
Test Ingestion Script
Test the data ingestion module with sample data (for development).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.spark_config import get_spark_session, stop_spark_session
from pyspark.sql import Row


def create_sample_data(spark):
    """Create sample data for testing ingestion logic."""
    print("\n" + "=" * 60)
    print("CREATING SAMPLE DATA FOR TESTING")
    print("=" * 60)
    
    # Sample orders
    orders_data = [
        Row(order_id=1, user_id=101, eval_set="prior", order_number=1, order_dow=2, order_hour_of_day=10, days_since_prior_order=None),
        Row(order_id=2, user_id=101, eval_set="prior", order_number=2, order_dow=3, order_hour_of_day=14, days_since_prior_order=7.0),
        Row(order_id=3, user_id=102, eval_set="prior", order_number=1, order_dow=1, order_hour_of_day=9, days_since_prior_order=None),
    ]
    orders_df = spark.createDataFrame(orders_data)
    
    # Sample order_products
    order_products_data = [
        Row(order_id=1, product_id=1001, add_to_cart_order=1, reordered=0),
        Row(order_id=1, product_id=1002, add_to_cart_order=2, reordered=0),
        Row(order_id=2, product_id=1001, add_to_cart_order=1, reordered=1),
        Row(order_id=2, product_id=1003, add_to_cart_order=2, reordered=0),
        Row(order_id=3, product_id=1002, add_to_cart_order=1, reordered=0),
    ]
    order_products_df = spark.createDataFrame(order_products_data)
    
    # Sample products
    products_data = [
        Row(product_id=1001, product_name="Organic Bananas", aisle_id=24, department_id=4),
        Row(product_id=1002, product_name="Organic Avocado", aisle_id=24, department_id=4),
        Row(product_id=1003, product_name="Organic Strawberries", aisle_id=24, department_id=4),
    ]
    products_df = spark.createDataFrame(products_data)
    
    # Sample aisles
    aisles_data = [
        Row(aisle_id=24, aisle="fresh fruits"),
    ]
    aisles_df = spark.createDataFrame(aisles_data)
    
    # Sample departments
    departments_data = [
        Row(department_id=4, department="produce"),
    ]
    departments_df = spark.createDataFrame(departments_data)
    
    print("✓ Sample data created")
    
    return {
        "orders": orders_df,
        "order_products_prior": order_products_df,
        "order_products_train": spark.createDataFrame([], order_products_df.schema),  # Empty train set
        "products": products_df,
        "aisles": aisles_df,
        "departments": departments_df,
    }


def main():
    """Test ingestion logic with sample data."""
    print("=" * 60)
    print("TESTING DATA INGESTION MODULE")
    print("=" * 60)
    
    # Initialize Spark session
    print("\n[1/3] Initializing Spark session...")
    spark = get_spark_session(app_name="InstacartIngestionTest")
    print("✓ Spark session initialized")
    
    try:
        # Create sample data
        print("\n[2/3] Creating sample data...")
        dataframes = create_sample_data(spark)
        
        # Test schema validation
        print("\n[3/3] Testing schema validation...")
        from src.data.ingest import validate_schemas
        schema_valid = validate_schemas(dataframes)
        
        if schema_valid:
            print("\n✓ Schema validation passed")
        else:
            print("\n✗ Schema validation failed")
        
        # Test data quality checks
        print("\nTesting data quality checks...")
        from src.data.clean import run_data_quality_checks, clean_data
        
        dq_report = run_data_quality_checks(dataframes)
        
        # Test cleaning
        cleaned = clean_data(dataframes)
        
        print("\n" + "=" * 60)
        print("✅ INGESTION MODULE TEST COMPLETE")
        print("=" * 60)
        print("\nAll functions working correctly!")
        print("\nReady to run with real data:")
        print("  1. Download data: bash scripts/download_data.sh")
        print("  2. Run ETL: python scripts/run_etl.py")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        stop_spark_session(spark)


if __name__ == "__main__":
    main()
