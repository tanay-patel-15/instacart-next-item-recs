# Power BI Data Dictionary

This document describes the schema for Power BI Desktop exports (Windows VM workflow).

## Export Format

**Format**: Individual CSV files (6 files total)  
**Location**: `exports/powerbi/`  
**Platform**: Power BI Desktop (Windows VM)  
**Workflow**: PySpark on macOS → CSV exports → Power BI Desktop in VM

---

## 1. product_affinity.csv

**Purpose**: Product-to-product affinity matrix showing which products are frequently bought together.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| product_a | string | First product name | "Organic Bananas" |
| product_b | string | Second product name | "Organic Avocado" |
| co_occurrence_count | int | Number of baskets containing both products | 1523 |
| confidence | float | P(product_b \| product_a) | 0.42 |
| lift | float | Confidence / P(product_b) | 2.1 |
| support | float | Fraction of baskets with both products | 0.015 |

**Use Cases**:
- Identify strong product pairs for bundling
- Create product affinity heatmaps
- Recommend complementary products

---

## 2. aisle_crosssell.csv

**Purpose**: Aisle-level cross-sell opportunities showing which aisles have strong affinity.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| aisle_from | string | Source aisle | "fresh fruits" |
| aisle_to | string | Target aisle | "yogurt" |
| top_products | string | Top 3 products in target aisle (comma-separated) | "Greek Yogurt, Organic Yogurt, Low Fat Yogurt" |
| avg_lift | float | Average lift across all rules from source to target aisle | 2.3 |
| rule_count | int | Number of rules supporting this cross-sell | 45 |
| avg_confidence | float | Average confidence across rules | 0.38 |

**Use Cases**:
- Store layout optimization
- Cross-aisle promotions
- Category management insights

---

## 3. dept_crosssell.csv

**Purpose**: Department-level cross-sell opportunities for strategic planning.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| department_from | string | Source department | "produce" |
| department_to | string | Target department | "dairy eggs" |
| top_products | string | Top 3 products in target department | "Organic Milk, Cage Free Eggs, Greek Yogurt" |
| avg_lift | float | Average lift across all rules | 1.8 |
| rule_count | int | Number of rules supporting this cross-sell | 120 |
| avg_confidence | float | Average confidence across rules | 0.35 |
| avg_basket_size | float | Average basket size for this department pair | 12.4 |

**Use Cases**:
- Strategic category planning
- Department-level promotions
- Executive dashboards

---

## 4. top_rules.csv

**Purpose**: Top association rules in human-readable format.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| rule_id | int | Unique rule identifier | 1 |
| antecedent | string | "If" part of rule (comma-separated products) | "Organic Bananas, Organic Strawberries" |
| consequent | string | "Then" part of rule (product name) | "Organic Avocado" |
| confidence | float | P(consequent \| antecedent) | 0.42 |
| lift | float | Confidence / P(consequent) | 2.1 |
| support | float | Fraction of baskets with both | 0.015 |
| aisle_from | string | Aisle of antecedent products | "fresh fruits" |
| aisle_to | string | Aisle of consequent product | "fresh fruits" |
| department_from | string | Department of antecedent | "produce" |
| department_to | string | Department of consequent | "produce" |

**Use Cases**:
- Explore specific rules
- Validate rule quality
- Generate business insights

---

## 5. recommendation_examples.csv

**Purpose**: Concrete examples of recommendations for validation and storytelling.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| example_id | int | Unique example identifier | 1 |
| basket_items | string | Items in partial basket (comma-separated) | "Organic Bananas, Organic Milk, Cage Free Eggs" |
| recommended_items | string | Top-5 recommended items (comma-separated) | "Organic Avocado, Greek Yogurt, Organic Strawberries, Organic Spinach, Organic Blueberries" |
| rule_used | string | Rule that generated top recommendation | "{Organic Bananas, Organic Milk} → Organic Avocado" |
| confidence | float | Confidence of rule used | 0.42 |
| lift | float | Lift of rule used | 2.1 |
| basket_size | int | Number of items in basket | 3 |
| num_recommendations | int | Number of recommendations generated | 5 |

**Use Cases**:
- Validate recommendation quality
- Create storytelling examples
- User acceptance testing

---

## 6. evaluation_summary.csv

**Purpose**: Model performance metrics for validation page.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| metric_name | string | Name of metric | "hit_rate_at_5" |
| metric_value | float | Value of metric | 0.18 |
| target_value | float | Target threshold | 0.15 |
| baseline_value | float | Baseline model value | 0.12 |
| lift_over_baseline | float | Improvement over baseline | 0.06 |

**Metrics Included**:
- `hit_rate_at_5`: Hit-Rate@5 (target: 0.15)
- `hit_rate_at_10`: Hit-Rate@10 (target: 0.25)
- `coverage`: Product coverage (target: 0.50)
- `avg_diversity`: Avg unique aisles in top-10 (target: 3.0)

**Use Cases**:
- Model validation
- Performance dashboards
- Compare to baseline

---

## Data Relationships (for Power BI Service)

### Primary Keys
- `product_affinity`: Composite key (product_a, product_b)
- `aisle_crosssell`: Composite key (aisle_from, aisle_to)
- `dept_crosssell`: Composite key (department_from, department_to)
- `top_rules`: rule_id
- `recommendation_examples`: example_id
- `evaluation_summary`: metric_name

### Recommended Relationships

**Create these in Power BI Service Model view**:

1. **top_rules → aisle_crosssell**
   - From: `top_rules[aisle_from]`
   - To: `aisle_crosssell[aisle_from]`
   - Cardinality: Many-to-Many
   - Cross-filter: Both directions

2. **top_rules → dept_crosssell**
   - From: `top_rules[department_from]`
   - To: `dept_crosssell[department_from]`
   - Cardinality: Many-to-Many
   - Cross-filter: Both directions

3. **product_affinity → top_rules** (optional, for advanced filtering)
   - From: `product_affinity[product_a]`
   - To: `top_rules[antecedent]`
   - Cardinality: Many-to-Many
   - Cross-filter: Both directions

**Note**: Many-to-many relationships are fully supported in Power BI Service.

---

## Data Quality Notes

1. **Null Values**: No null values should exist in any file
2. **Duplicates**: No duplicate rows (enforced by primary keys)
3. **Lift Values**: All lift values should be ≥ 1.5 (filtered during export)
4. **Confidence Values**: All confidence values should be ≥ 0.3 (filtered during export)
5. **Top-N Filtering**: Only top 10,000 rules exported to keep file size manageable

---

## File Sizes (Approximate)

| File | Rows | Size |
|------|------|------|
| product_affinity.csv | ~50,000 | ~5 MB |
| aisle_crosssell.csv | ~500 | ~50 KB |
| dept_crosssell.csv | ~100 | ~10 KB |
| top_rules.csv | ~10,000 | ~2 MB |
| recommendation_examples.csv | ~1,000 | ~200 KB |
| evaluation_summary.csv | ~10 | ~1 KB |

**Total**: ~7-8 MB (easily loads into PowerBI Desktop)

---

## Refresh Strategy (Windows VM)

**Simple Refresh Workflow** (CSV files in shared folder):

1. **On macOS**: Re-run export script
   ```bash
   python scripts/export_powerbi_bundle.py
   ```

2. **In Windows VM**: Open .pbix file in Power BI Desktop
   - Click **Home** → **Refresh**
   - Power BI automatically reloads CSV files from shared folder
   - All visuals update immediately

3. **Save**: Click **File** → **Save**

**Why this works**:
- CSV files are in a shared folder accessible from Windows VM
- Power BI Desktop remembers the file paths
- No need to re-import or reconnect data sources
- Refresh is instant (just reloads CSVs)

**Alternative**: If paths break, use **Transform data** → **Data source settings** → Update file paths

---

## Questions?

For schema questions, see `docs/data_dictionary.md` for upstream data definitions.
