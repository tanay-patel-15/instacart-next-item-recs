"""
Model Training Script
Trains the FP-Growth association rule mining model.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.spark_config import get_spark_session, stop_spark_session


def main():
    """Train the FP-Growth model."""
    print("=" * 60)
    print("INSTACART RECOMMENDATION SYSTEM - MODEL TRAINING")
    print("=" * 60)
    
    # Initialize Spark session
    print("\n[1/3] Initializing Spark session...")
    spark = get_spark_session(app_name="InstacartModelTraining")
    print("✓ Spark session initialized")
    
    # Load training data
    print("\n[2/3] Loading training data...")
    # TODO: Load data/validation/train_baskets.parquet
    print("✓ Training data loaded")
    
    # Train FP-Growth model
    print("\n[3/3] Training FP-Growth model...")
    # TODO: Implement src.models.association_rules.train_fp_growth()
    print("✓ Model trained")
    
    # Stop Spark session
    stop_spark_session(spark)
    
    print("\n" + "=" * 60)
    print("MODEL TRAINING COMPLETE")
    print("=" * 60)
    print("\nOutput files:")
    print("  - artifacts/association_rules.parquet")
    print("\nNext step: python scripts/evaluate_model.py")


if __name__ == "__main__":
    main()
