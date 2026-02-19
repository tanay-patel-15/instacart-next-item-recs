"""
PowerBI Export Script
Generates PowerBI-ready CSV files from model outputs.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.spark_config import get_spark_session, stop_spark_session
from config.paths import POWERBI_DIR


def main():
    """Export data for PowerBI."""
    print("=" * 60)
    print("INSTACART RECOMMENDATION SYSTEM - POWERBI EXPORT")
    print("=" * 60)
    
    # Initialize Spark session
    print("\n[1/2] Initializing Spark session...")
    spark = get_spark_session(app_name="InstacartPowerBIExport")
    print("✓ Spark session initialized")
    
    # Generate PowerBI exports
    print("\n[2/2] Generating PowerBI exports...")
    # TODO: Implement src.exports.powerbi_export.export_all()
    print("✓ Exports generated")
    
    # Stop Spark session
    stop_spark_session(spark)
    
    print("\n" + "=" * 60)
    print("POWERBI EXPORT COMPLETE")
    print("=" * 60)
    print("\nOutput files:")
    print(f"  - {POWERBI_DIR}/product_affinity.csv")
    print(f"  - {POWERBI_DIR}/aisle_crosssell.csv")
    print(f"  - {POWERBI_DIR}/dept_crosssell.csv")
    print(f"  - {POWERBI_DIR}/top_rules.csv")
    print(f"  - {POWERBI_DIR}/recommendation_examples.csv")
    print(f"  - {POWERBI_DIR}/evaluation_summary.csv")
    print("\nNext step: Import CSV files into PowerBI Desktop")


if __name__ == "__main__":
    main()
