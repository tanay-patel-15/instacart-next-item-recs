"""
Centralized Path Definitions
All file paths used in the project are defined here.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VALIDATION_DATA_DIR = DATA_DIR / "validation"

# Raw data files
RAW_ORDERS = RAW_DATA_DIR / "orders.csv"
RAW_ORDER_PRODUCTS_PRIOR = RAW_DATA_DIR / "order_products__prior.csv"
RAW_ORDER_PRODUCTS_TRAIN = RAW_DATA_DIR / "order_products__train.csv"
RAW_PRODUCTS = RAW_DATA_DIR / "products.csv"
RAW_AISLES = RAW_DATA_DIR / "aisles.csv"
RAW_DEPARTMENTS = RAW_DATA_DIR / "departments.csv"

# Processed data files
PROCESSED_BASKETS = PROCESSED_DATA_DIR / "baskets.parquet"
PROCESSED_PRODUCT_STATS = PROCESSED_DATA_DIR / "product_stats.parquet"
PROCESSED_AISLE_DEPT_ROLLUPS = PROCESSED_DATA_DIR / "aisle_dept_rollups.parquet"

# Validation data files
TRAIN_BASKETS = VALIDATION_DATA_DIR / "train_baskets.parquet"
TEST_BASKETS = VALIDATION_DATA_DIR / "test_baskets.parquet"

# Artifacts directory
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
ASSOCIATION_RULES = ARTIFACTS_DIR / "association_rules.parquet"
TOP_RECOMMENDATIONS = ARTIFACTS_DIR / "top_recommendations.parquet"
EVALUATION_METRICS = ARTIFACTS_DIR / "evaluation_metrics.json"

# Exports directory
EXPORTS_DIR = PROJECT_ROOT / "exports"
POWERBI_DIR = EXPORTS_DIR / "powerbi"

# PowerBI export files
POWERBI_BUNDLE = POWERBI_DIR / "powerbi_bundle.xlsx"  # Main export for Power BI Service
POWERBI_PRODUCT_AFFINITY = POWERBI_DIR / "product_affinity.csv"
POWERBI_AISLE_CROSSSELL = POWERBI_DIR / "aisle_crosssell.csv"
POWERBI_DEPT_CROSSSELL = POWERBI_DIR / "dept_crosssell.csv"
POWERBI_TOP_RULES = POWERBI_DIR / "top_rules.csv"
POWERBI_RECOMMENDATION_EXAMPLES = POWERBI_DIR / "recommendation_examples.csv"
POWERBI_EVALUATION_SUMMARY = POWERBI_DIR / "evaluation_summary.csv"

# Config files
CONFIG_DIR = PROJECT_ROOT / "config"
MODEL_PARAMS = CONFIG_DIR / "model_params.yaml"


def ensure_directories():
    """Create all necessary directories if they don't exist."""
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        VALIDATION_DATA_DIR,
        ARTIFACTS_DIR,
        POWERBI_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print("✓ All directories created/verified")


if __name__ == "__main__":
    ensure_directories()
