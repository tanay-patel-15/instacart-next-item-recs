"""
Evaluation Metrics Module
Compute offline evaluation metrics for recommendations.
"""

from pyspark.sql import DataFrame


def compute_hit_rate_at_k(recommendations_df: DataFrame, test_df: DataFrame, k: int = 5):
    """
    Compute Hit-Rate@K metric.
    
    Args:
        recommendations_df (DataFrame): Recommendations with scores
        test_df (DataFrame): Test baskets with ground truth
        k (int): Top-K threshold
    
    Returns:
        float: Hit-Rate@K (0.0 to 1.0)
    """
    # TODO: Implement hit-rate calculation
    # - For each test basket, check if any top-K recommendation appears in ground truth
    # - Return % of baskets with at least one hit
    
    raise NotImplementedError("Hit-rate metric not yet implemented")


def compute_coverage(recommendations_df: DataFrame, product_stats_df: DataFrame):
    """
    Compute coverage metric (% of products recommended).
    
    Args:
        recommendations_df (DataFrame): All recommendations
        product_stats_df (DataFrame): Product statistics
    
    Returns:
        float: Coverage (0.0 to 1.0)
    """
    # TODO: Implement coverage calculation
    
    raise NotImplementedError("Coverage metric not yet implemented")


def compute_diversity(recommendations_df: DataFrame):
    """
    Compute diversity metric (avg unique aisles in top-K).
    
    Args:
        recommendations_df (DataFrame): Recommendations with aisle info
    
    Returns:
        float: Average number of unique aisles per recommendation list
    """
    # TODO: Implement diversity calculation
    
    raise NotImplementedError("Diversity metric not yet implemented")
