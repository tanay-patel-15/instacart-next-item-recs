"""
Baseline Model Module
Popularity-based baseline for comparison.
"""

from pyspark.sql import DataFrame


def create_popularity_baseline(train_df: DataFrame, top_k: int = 10):
    """
    Create popularity-based baseline recommendations.
    
    Args:
        train_df (DataFrame): Training baskets
        top_k (int): Number of recommendations
    
    Returns:
        DataFrame: Top-K most popular products
    """
    # TODO: Implement popularity baseline
    # - Compute product popularity (reorder rate)
    # - Return top-K most popular products
    
    raise NotImplementedError("Popularity baseline not yet implemented")
