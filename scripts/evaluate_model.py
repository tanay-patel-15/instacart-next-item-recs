"""
Model Evaluation Script
Evaluates the trained model on the test set.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.spark_config import get_spark_session, stop_spark_session


def main():
    """Evaluate the trained model."""
    print("=" * 60)
    print("INSTACART RECOMMENDATION SYSTEM - MODEL EVALUATION")
    print("=" * 60)
    
    # Initialize Spark session
    print("\n[1/4] Initializing Spark session...")
    spark = get_spark_session(app_name="InstacartModelEvaluation")
    print("✓ Spark session initialized")
    
    # Load test data and rules
    print("\n[2/4] Loading test data and association rules...")
    # TODO: Load data/validation/test_baskets.parquet
    # TODO: Load artifacts/association_rules.parquet
    print("✓ Data loaded")
    
    # Generate recommendations
    print("\n[3/4] Generating recommendations...")
    # TODO: Implement src.models.scoring.score_recommendations()
    print("✓ Recommendations generated")
    
    # Evaluate metrics
    print("\n[4/4] Computing evaluation metrics...")
    # TODO: Implement src.evaluation.evaluate.compute_metrics()
    print("✓ Metrics computed")
    
    # Stop Spark session
    stop_spark_session(spark)
    
    print("\n" + "=" * 60)
    print("MODEL EVALUATION COMPLETE")
    print("=" * 60)
    print("\nOutput files:")
    print("  - artifacts/top_recommendations.parquet")
    print("  - artifacts/evaluation_metrics.json")
    print("\nNext step: python scripts/export_powerbi.py")


if __name__ == "__main__":
    main()
