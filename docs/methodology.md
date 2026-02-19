# Methodology

## Overview

This project uses **association rule mining** (FP-Growth algorithm) to discover product affinity patterns in grocery baskets and generate explainable "next item" recommendations.

---

## 1. FP-Growth Algorithm

### What is FP-Growth?

FP-Growth (Frequent Pattern Growth) is an efficient algorithm for mining frequent itemsets without candidate generation. It discovers patterns like:

> "Customers who buy {milk, eggs} are 80% likely to also buy bread"

### Key Concepts

- **Support**: Fraction of transactions containing an itemset
  - Example: If {milk, eggs} appears in 5% of baskets, support = 0.05

- **Confidence**: Conditional probability P(consequent | antecedent)
  - Example: P(bread | {milk, eggs}) = 0.80 means 80% of baskets with milk and eggs also contain bread

- **Lift**: Ratio of confidence to baseline probability
  - Lift = confidence / P(consequent)
  - Lift > 1: Positive correlation (items bought together more than random)
  - Lift = 1: No correlation
  - Lift < 1: Negative correlation

### Why FP-Growth?

- **Scalable**: Handles millions of transactions efficiently
- **No candidate generation**: Faster than Apriori algorithm
- **Built into Spark MLlib**: Production-ready implementation
- **Explainable**: Rules are human-readable

---

## 2. Data Processing Pipeline

### Stage 1: Data Ingestion
- Load 6 CSV files from Kaggle dataset
- Validate schemas
- Initial data quality checks

### Stage 2: Data Cleaning
- Remove null values
- Remove duplicate orders
- Filter invalid records (e.g., empty baskets)

### Stage 3: Feature Engineering
- **Basket Creation**: Group products by (user_id, order_id)
- **Product Statistics**: Compute popularity, reorder rates
- **Aisle/Department Rollups**: Aggregate by category

### Stage 4: Train/Test Split
- **Strategy**: Temporal split
  - Last order per user → test set
  - All prior orders → train set
- **Rationale**: Mimics real-world scenario (predict next order)

---

## 3. Model Training

### FP-Growth Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| min_support | 0.01 | Include itemsets in ≥1% of baskets |
| min_confidence | 0.3 | Rules with ≥30% conditional probability |
| min_lift | 1.5 | Only positive correlations (50% above random) |

### Training Process

1. Convert baskets to array format: `[product_id_1, product_id_2, ...]`
2. Train FP-Growth model on training baskets
3. Extract association rules
4. Filter rules by confidence and lift thresholds
5. Save rules to `artifacts/association_rules.parquet`

---

## 4. Recommendation Scoring

### Scoring Logic

For a given partial basket `B = {product_1, product_2, ...}`:

1. **Match Rules**: Find all rules where `antecedent ⊆ B`
2. **Score Candidates**: For each candidate product `p`:
   ```
   score(p) = max(rule_confidence × rule_lift) + popularity_prior(p)
   ```
3. **Rank**: Sort candidates by score descending
4. **Select Top-K**: Return top-K recommendations (default K=10)

### Popularity Prior

To avoid recommending only niche products, we add a popularity prior:

```
popularity_prior(p) = 0.2 × reorder_rate(p)
```

This ensures popular products (e.g., bananas, milk) are considered even if no strong rules match.

---

## 5. Offline Evaluation

### Metrics

#### 1. Hit-Rate@K
**Definition**: % of test baskets where at least one recommended item appears in the ground truth.

**Calculation**:
```
Hit-Rate@K = (# baskets with ≥1 hit in top-K) / (# total test baskets)
```

**Target**: Hit-Rate@5 ≥ 15%, Hit-Rate@10 ≥ 25%

#### 2. Coverage
**Definition**: % of unique products that appear in at least one recommendation.

**Calculation**:
```
Coverage = (# unique products recommended) / (# total products)
```

**Target**: ≥ 50% (avoid recommending only popular items)

#### 3. Diversity
**Definition**: Average number of unique aisles in top-K recommendations.

**Calculation**:
```
Diversity = avg(# unique aisles in top-K per basket)
```

**Target**: ≥ 3 aisles per top-10 recommendation

#### 4. Lift over Baseline
**Definition**: Improvement over popularity-based baseline.

**Calculation**:
```
Lift = Hit-Rate@K (rule-based) - Hit-Rate@K (baseline)
```

**Target**: ≥ 5 percentage points improvement

### Baseline Model

**Popularity Baseline**: Recommend top-K most popular products (by reorder rate) for all baskets.

This baseline is simple but effective. Our rule-based model should outperform it to demonstrate value.

---

## 6. Explainability

### Why Explainability Matters

- **Trust**: Stakeholders understand why recommendations are made
- **Debugging**: Easy to identify nonsensical rules
- **Business Insights**: Discover cross-sell opportunities

### How We Achieve Explainability

1. **Rule-Based**: Each recommendation traces back to a specific rule
2. **Human-Readable Rules**: 
   ```
   {Organic Bananas, Organic Strawberries} → Organic Avocado
   Confidence: 0.42, Lift: 2.1
   ```
3. **PowerBI Visualizations**: Interactive exploration of rules and affinities

---

## 7. Limitations & Future Work

### Current Limitations

1. **No User Personalization**: All users with the same basket get same recommendations
2. **No Sequential Patterns**: Doesn't consider order sequence (e.g., breakfast → lunch → dinner)
3. **No Time-Based Features**: Ignores time of day, day of week
4. **Cold Start**: No recommendations for new products

### Future Enhancements

1. **Hybrid Model**: Combine rules + collaborative filtering (ALS)
2. **Sequential Pattern Mining**: Use PrefixSpan for order sequences
3. **User Features**: Incorporate user-level features (order frequency, avg basket size)
4. **Time-Based Weighting**: Weight recent orders higher
5. **Diversity Penalty**: Penalize recommendations from same aisle

---

## 8. References

- **FP-Growth Paper**: Han et al. (2000) "Mining Frequent Patterns without Candidate Generation"
- **Spark MLlib Documentation**: https://spark.apache.org/docs/latest/ml-frequent-pattern-mining.html
- **Instacart Dataset**: https://www.kaggle.com/c/instacart-market-basket-analysis
