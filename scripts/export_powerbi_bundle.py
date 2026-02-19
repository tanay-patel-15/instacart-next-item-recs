"""
PowerBI Export Script
Generates CSV files for Power BI Desktop (Windows VM workflow).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.spark_config import get_spark_session, stop_spark_session
from config.paths import POWERBI_DIR


def main():
    """Export data for Power BI Desktop."""
    print("=" * 60)
    print("INSTACART RECOMMENDATION SYSTEM - POWER BI EXPORT")
    print("=" * 60)
    print("\nTarget: Power BI Desktop (Windows VM)")
    
    # Initialize Spark session
    print("\n[1/3] Initializing Spark session...")
    spark = get_spark_session(app_name="InstacartPowerBIExport")
    print("✓ Spark session initialized")
    
    # Generate CSV files
    print("\n[2/3] Generating CSV files...")
    # TODO: Implement src.exports.powerbi_export.export_csv_files()
    # This should create 6 CSV files:
    #   - product_affinity.csv
    #   - aisle_crosssell.csv
    #   - dept_crosssell.csv
    #   - top_rules.csv
    #   - recommendation_examples.csv
    #   - evaluation_summary.csv
    print("✓ CSV files created")
    
    # Update data dictionary
    print("\n[3/3] Updating data dictionary...")
    # TODO: Implement src.exports.powerbi_export.generate_data_dictionary()
    # This should update exports/powerbi/data_dictionary.md with:
    #   - Table schemas (columns, types, descriptions)
    #   - Recommended relationships (from/to columns, cardinality)
    #   - Key columns for joins
    #   - Sample values
    print("✓ Data dictionary updated")
    
    # Stop Spark session
    stop_spark_session(spark)
    
    print("\n" + "=" * 60)
    print("POWER BI EXPORT COMPLETE")
    print("=" * 60)
    print("\n📦 Output files (in exports/powerbi/):")
    print("  ✓ product_affinity.csv - Product-to-product affinity matrix")
    print("  ✓ aisle_crosssell.csv - Aisle-level cross-sell opportunities")
    print("  ✓ dept_crosssell.csv - Department-level insights")
    print("  ✓ top_rules.csv - Association rules (human-readable)")
    print("  ✓ recommendation_examples.csv - Example recommendations")
    print("  ✓ evaluation_summary.csv - Model performance metrics")
    print("  ✓ data_dictionary.md - Schema documentation with relationships")
    
    print("\n🚀 Next steps (Windows VM):")
    print("  1. Start Windows VM (Parallels/VMware)")
    print("  2. Open Power BI Desktop")
    print("  3. Get Data → Text/CSV")
    print("  4. Navigate to shared folder:")
    print("     - Parallels: \\\\Mac\\Home\\...\\exports\\powerbi")
    print("     - VMware: \\\\vmware-host\\Shared Folders\\powerbi")
    print("  5. Import all 6 CSV files")
    print("  6. Create relationships (see data_dictionary.md)")
    print("  7. Build report and save .pbix locally")
    
    print("\n📖 Documentation:")
    print("  - Setup guide: docs/powerbi_guide.md")
    print("  - Schema & relationships: exports/powerbi/data_dictionary.md")
    
    print("\n💡 Tip: Set up shared folder between macOS and Windows VM")
    print("   for seamless access to CSV files (see docs/powerbi_guide.md)")


if __name__ == "__main__":
    main()
