# Data Dictionary

## Raw Data Schema (Kaggle Dataset)

### orders.csv
| Column | Type | Description |
|--------|------|-------------|
| order_id | int | Unique order identifier |
| user_id | int | Unique user identifier |
| eval_set | string | Which evaluation set this order belongs to (prior, train, test) |
| order_number | int | Order sequence number for this user (1 = first order) |
| order_dow | int | Day of week (0-6) |
| order_hour_of_day | int | Hour of day (0-23) |
| days_since_prior_order | float | Days since previous order (null for first order) |

### order_products__prior.csv & order_products__train.csv
| Column | Type | Description |
|--------|------|-------------|
| order_id | int | Foreign key to orders.csv |
| product_id | int | Foreign key to products.csv |
| add_to_cart_order | int | Order in which product was added to cart |
| reordered | int | 1 if reordered, 0 if first time |

### products.csv
| Column | Type | Description |
|--------|------|-------------|
| product_id | int | Unique product identifier |
| product_name | string | Product name |
| aisle_id | int | Foreign key to aisles.csv |
| department_id | int | Foreign key to departments.csv |

### aisles.csv
| Column | Type | Description |
|--------|------|-------------|
| aisle_id | int | Unique aisle identifier |
| aisle | string | Aisle name |

### departments.csv
| Column | Type | Description |
|--------|------|-------------|
| department_id | int | Unique department identifier |
| department | string | Department name |

---

## Processed Data Schema

### baskets.parquet
| Column | Type | Description |
|--------|------|-------------|
| user_id | int | User identifier |
| order_id | int | Order identifier |
| basket | array<int> | Array of product_ids in this basket |
| basket_size | int | Number of items in basket |
| order_number | int | Order sequence number |
| order_dow | int | Day of week |
| order_hour_of_day | int | Hour of day |

### product_stats.parquet
| Column | Type | Description |
|--------|------|-------------|
| product_id | int | Product identifier |
| product_name | string | Product name |
| aisle | string | Aisle name |
| department | string | Department name |
| total_orders | int | Number of orders containing this product |
| reorder_rate | float | Fraction of orders where product was reordered |
| popularity_rank | int | Rank by total_orders (1 = most popular) |

### aisle_dept_rollups.parquet
| Column | Type | Description |
|--------|------|-------------|
| aisle_id | int | Aisle identifier |
| aisle | string | Aisle name |
| department | string | Department name |
| total_orders | int | Number of orders containing items from this aisle |
| avg_basket_size | float | Average items per basket from this aisle |
| top_products | array<string> | Top 5 products in this aisle |

---

## Model Outputs

### association_rules.parquet
| Column | Type | Description |
|--------|------|-------------|
| antecedent | array<int> | Product IDs in the "if" part of rule |
| consequent | array<int> | Product IDs in the "then" part of rule |
| confidence | float | P(consequent \| antecedent) |
| lift | float | confidence / P(consequent) |
| support | float | Fraction of baskets containing both antecedent and consequent |

### top_recommendations.parquet
| Column | Type | Description |
|--------|------|-------------|
| user_id | int | User identifier |
| order_id | int | Order identifier (test set) |
| basket | array<int> | Partial basket (input) |
| recommended_product_id | int | Recommended product |
| score | float | Recommendation score |
| rank | int | Rank within top-K (1 = highest score) |
| rule_used | string | Rule that generated this recommendation |

### evaluation_metrics.json
```json
{
  "hit_rate_at_5": float,
  "hit_rate_at_10": float,
  "coverage": float,
  "avg_diversity": float,
  "baseline_hit_rate_at_5": float,
  "lift_over_baseline": float
}
```

---

## PowerBI Export Schema

See `exports/powerbi/data_dictionary.md` for PowerBI-specific schemas.
