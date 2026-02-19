# Instacart Next-Item Recommendation System
## Implementation Plan & Architecture

**Project Goal**: Build a data science project that creates explainable "next item" recommendations for grocery baskets using the Instacart Market Basket Analysis dataset, leveraging PySpark for scalable data processing and PowerBI for executive storytelling.

---

## 1. Project Architecture Overview

### 1.1 Proposed Folder Structure

```
instacart-next-item-recs/
├── README.md                          # Project overview, setup, and run instructions
├── cursor.md                          # This implementation plan (for Cursor context)
├── .gitignore                         # Git ignore patterns
├── environment.yml                    # Conda environment specification
├── requirements.txt                   # Python dependencies (pip fallback)
├── pyproject.toml                     # Poetry configuration (optional)
│
├── config/                            # Configuration files
│   ├── spark_config.py               # Spark session configuration
│   ├── paths.py                      # Centralized path definitions
│   └── model_params.yaml             # Model hyperparameters (FP-Growth settings)
│
├── data/                              # Data directory (gitignored except .gitkeep)
│   ├── raw/                          # Raw Instacart CSV files from Kaggle
│   │   ├── .gitkeep
│   │   ├── orders.csv
│   │   ├── order_products__prior.csv
│   │   ├── order_products__train.csv
│   │   ├── products.csv
│   │   ├── aisles.csv
│   │   └── departments.csv
│   ├── processed/                    # Cleaned, transformed parquet files
│   │   ├── orders_clean.parquet
│   │   ├── baskets.parquet          # Basket-level aggregations
│   │   ├── product_stats.parquet    # Product popularity, reorder rates
│   │   └── aisle_dept_rollups.parquet
│   └── validation/                   # Train/test split for evaluation
│       ├── train_baskets.parquet
│       └── test_baskets.parquet
│
├── src/                               # Source code
│   ├── __init__.py
│   ├── data/                         # Data ingestion and transformation
│   │   ├── __init__.py
│   │   ├── ingest.py                # Load raw CSVs into Spark DataFrames
│   │   ├── clean.py                 # Data quality checks and cleaning
│   │   ├── transform.py             # Feature engineering (baskets, rollups)
│   │   └── split.py                 # Train/test split logic
│   ├── models/                       # Recommendation logic
│   │   ├── __init__.py
│   │   ├── association_rules.py     # FP-Growth model training
│   │   ├── scoring.py               # Candidate ranking (rules + priors)
│   │   └── baseline.py              # Popularity baseline for comparison
│   ├── evaluation/                   # Offline evaluation
│   │   ├── __init__.py
│   │   ├── metrics.py               # Hit-rate@K, coverage, diversity
│   │   └── evaluate.py              # Run evaluation pipeline
│   └── exports/                      # PowerBI export logic
│       ├── __init__.py
│       └── powerbi_export.py        # Generate aggregated CSV/parquet for PowerBI
│
├── notebooks/                         # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_association_rules_analysis.ipynb
│   └── 03_recommendation_examples.ipynb
│
├── scripts/                           # Executable scripts
│   ├── run_etl.py                    # End-to-end ETL pipeline
│   ├── train_model.py                # Train FP-Growth and generate rules
│   ├── evaluate_model.py             # Run offline evaluation
│   └── export_powerbi.py             # Export PowerBI-ready files
│
├── tests/                             # Unit and integration tests
│   ├── __init__.py
│   ├── test_data_quality.py         # Data validation tests
│   ├── test_transform.py            # Transformation logic tests
│   └── test_scoring.py              # Recommendation scoring tests
│
├── artifacts/                         # Model outputs (gitignored)
│   ├── association_rules.parquet    # FP-Growth rules (antecedent, consequent, confidence, lift)
│   ├── top_recommendations.parquet  # Top-K recs per basket scenario
│   └── evaluation_metrics.json      # Offline metrics (hit-rate, coverage, etc.)
│
├── exports/                           # PowerBI-ready exports
│   └── powerbi/
│       ├── data_dictionary.md       # Schema documentation for PowerBI
│       ├── product_affinity.csv     # Product-to-product affinity matrix
│       ├── aisle_crosssell.csv      # Aisle-level cross-sell opportunities
│       ├── dept_crosssell.csv       # Department-level cross-sell
│       ├── top_rules.csv            # Top association rules (human-readable)
│       ├── recommendation_examples.csv  # Example baskets + recommendations
│       └── evaluation_summary.csv   # Model performance summary
│
└── docs/                              # Documentation
    ├── data_dictionary.md            # Dataset schema and field descriptions
    ├── methodology.md                # Recommendation approach explanation
    └── powerbi_guide.md              # PowerBI report setup instructions
```

---

## 2. Tech Stack & Rationale

### 2.1 Core Technologies

| Technology | Version | Purpose | Rationale |
|------------|---------|---------|-----------|
| **Python** | 3.10+ | Primary language | Wide data science ecosystem, PySpark compatibility |
| **PySpark** | 3.5.0 | Distributed data processing | Scalable joins/aggregations for large Instacart dataset (~3M orders) |
| **Spark MLlib** | (bundled) | FP-Growth algorithm | Built-in association rule mining, optimized for Spark |
| **Pandas** | 2.1+ | Small data manipulation | Export generation, notebook exploration |
| **PyArrow** | 14.0+ | Parquet I/O | Fast columnar storage for intermediate data |
| **PowerBI Desktop** | Latest | Visualization & storytelling | Business-friendly, interactive dashboards |
| **Jupyter** | Latest | Exploratory analysis | Interactive data exploration and validation |

### 2.2 Development & Environment

| Tool | Purpose |
|------|---------|
| **Conda** | Environment management (preferred for Spark) |
| **Poetry** (optional) | Dependency management alternative |
| **pytest** | Unit testing framework |
| **black** | Code formatting |
| **flake8** | Linting |
| **pre-commit** | Git hooks for code quality |

### 2.3 Why PySpark for Local Development?

- **Scalability**: Instacart dataset has ~3.4M orders, ~200K users, ~50K products. PySpark handles this efficiently even on a laptop.
- **Lazy Evaluation**: Optimizes query plans automatically.
- **MLlib FP-Growth**: Production-ready association rule mining without external libraries.
- **Parquet Support**: Efficient columnar storage reduces memory footprint.

---

## 3. Dependencies

### 3.1 Python Packages (requirements.txt)

```
# Core Data Processing
pyspark==3.5.0
pandas==2.1.4
numpy==1.26.2
pyarrow==14.0.1

# Data Validation
great-expectations==0.18.8  # Optional: data quality checks

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
tqdm==4.66.1

# Notebook & Visualization
jupyter==1.0.0
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0

# Testing & Quality
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.1
flake8==7.0.0
pre-commit==3.6.0

# Export
openpyxl==3.1.2  # Excel export if needed
```

### 3.2 Conda Environment (environment.yml)

```yaml
name: instacart-recs
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pyspark=3.5.0
  - pandas=2.1.4
  - numpy=1.26.2
  - pyarrow=14.0.1
  - jupyter=1.0.0
  - matplotlib=3.8.2
  - seaborn=0.13.0
  - pytest=7.4.3
  - black=23.12.1
  - flake8=7.0.0
  - pip
  - pip:
      - pyyaml==6.0.1
      - python-dotenv==1.0.0
      - tqdm==4.66.1
      - plotly==5.18.0
      - pytest-cov==4.1.0
      - pre-commit==3.6.0
```

---

## 4. Data Flow Architecture

### 4.1 High-Level Pipeline

```
┌─────────────────┐
│  Kaggle Dataset │
│   (6 CSV files) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              STAGE 1: DATA INGESTION                    │
│  - Load CSVs into Spark DataFrames                      │
│  - Schema validation                                     │
│  - Initial data quality checks                          │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│         STAGE 2: DATA CLEANING & TRANSFORMATION         │
│  - Remove nulls, duplicates                             │
│  - Join orders + products + aisles + departments        │
│  - Create basket-level view (user_id, order_id, items)  │
│  - Compute product stats (popularity, reorder rate)     │
│  - Aisle/department rollups                             │
│  Output: processed/*.parquet                            │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│            STAGE 3: TRAIN/TEST SPLIT                    │
│  - Temporal split: last order per user = test           │
│  - Prior orders = train                                 │
│  Output: validation/*.parquet                           │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│          STAGE 4: ASSOCIATION RULE MINING               │
│  - FP-Growth on train baskets                           │
│  - Filter rules: min_confidence=0.3, min_lift=1.5       │
│  - Generate rule table: {X,Y} -> Z, confidence, lift    │
│  Output: artifacts/association_rules.parquet            │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│         STAGE 5: RECOMMENDATION SCORING                 │
│  - For each test basket (partial):                      │
│    1. Match applicable rules                            │
│    2. Score candidates by rule confidence × lift        │
│    3. Add popularity prior (aisle/dept reorder rate)    │
│    4. Rank top-K items                                  │
│  Output: artifacts/top_recommendations.parquet          │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│            STAGE 6: OFFLINE EVALUATION                  │
│  - Metrics: Hit-Rate@5, Hit-Rate@10, Coverage           │
│  - Baseline: Popularity-based recommendations           │
│  - Compare rule-based vs. baseline                      │
│  Output: artifacts/evaluation_metrics.json              │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│           STAGE 7: POWERBI EXPORT                       │
│  - Aggregate rules by aisle/department                  │
│  - Create product affinity matrix (top pairs)           │
│  - Export recommendation examples                       │
│  - Generate data dictionary                             │
│  Output: exports/powerbi/*.csv                          │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              POWERBI DASHBOARD                          │
│  - Interactive visualizations                           │
│  - Executive storytelling                               │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Key Data Transformations

#### Input Schema (Kaggle CSVs)
- `orders.csv`: order_id, user_id, order_number, order_dow, order_hour_of_day, days_since_prior_order
- `order_products__prior.csv`: order_id, product_id, add_to_cart_order, reordered
- `order_products__train.csv`: (same schema as prior)
- `products.csv`: product_id, product_name, aisle_id, department_id
- `aisles.csv`: aisle_id, aisle
- `departments.csv`: department_id, department

#### Intermediate Tables
1. **baskets.parquet**: user_id, order_id, basket (array of product_ids), basket_size, order_number
2. **product_stats.parquet**: product_id, product_name, aisle, department, total_orders, reorder_rate, popularity_rank
3. **aisle_dept_rollups.parquet**: aisle/department-level aggregations (avg basket size, top products)

#### Output Tables (PowerBI)
1. **product_affinity.csv**: product_a, product_b, co_occurrence_count, lift, confidence
2. **aisle_crosssell.csv**: aisle_from, aisle_to, top_products, avg_lift
3. **top_rules.csv**: rule_id, antecedent (readable), consequent (readable), confidence, lift, support
4. **recommendation_examples.csv**: basket_items, recommended_items, rule_used, confidence

---

## 5. Detailed Implementation Plan

### 5.1 Milestones & Timeline (MVP in 5 days)

#### **Day 1: Environment Setup & Data Ingestion**
- [ ] Set up conda environment with PySpark
- [ ] Download Instacart dataset from Kaggle
- [ ] Create folder structure
- [ ] Implement `src/data/ingest.py`: Load CSVs into Spark
- [ ] Implement `src/data/clean.py`: Basic data quality checks
- [ ] Write `scripts/run_etl.py` (Stage 1-2)
- [ ] Validate: All CSVs load successfully, schema matches expectations

#### **Day 2: Data Transformation & Feature Engineering**
- [ ] Implement `src/data/transform.py`:
  - Join orders + products + aisles + departments
  - Create basket-level view (groupBy user_id, order_id)
  - Compute product statistics (popularity, reorder rate)
  - Aisle/department rollups
- [ ] Implement `src/data/split.py`: Temporal train/test split
- [ ] Save processed data to `data/processed/` and `data/validation/`
- [ ] Validate: Spot-check basket structure, verify split logic

#### **Day 3: Association Rule Mining**
- [ ] Implement `src/models/association_rules.py`:
  - FP-Growth model training (MLlib)
  - Hyperparameters: min_support=0.01, min_confidence=0.3
  - Extract rules with lift > 1.5
- [ ] Implement `src/models/baseline.py`: Popularity-based recommender
- [ ] Write `scripts/train_model.py`
- [ ] Save rules to `artifacts/association_rules.parquet`
- [ ] Validate: Inspect top rules, verify lift calculations

#### **Day 4: Recommendation Scoring & Evaluation**
- [ ] Implement `src/models/scoring.py`:
  - Match rules to partial baskets
  - Score candidates (rule confidence × lift + popularity prior)
  - Rank top-K items
- [ ] Implement `src/evaluation/metrics.py`: Hit-Rate@K, coverage, diversity
- [ ] Implement `src/evaluation/evaluate.py`: Run evaluation on test set
- [ ] Write `scripts/evaluate_model.py`
- [ ] Save metrics to `artifacts/evaluation_metrics.json`
- [ ] Validate: Hit-Rate@5 > 15% (target), coverage > 50%

#### **Day 5: PowerBI Export & Documentation**
- [ ] Implement `src/exports/powerbi_export.py`:
  - Aggregate rules by aisle/department
  - Create product affinity matrix
  - Generate recommendation examples
- [ ] Write `scripts/export_powerbi.py`
- [ ] Create `exports/powerbi/data_dictionary.md`
- [ ] Update `README.md` with setup and run instructions
- [ ] Validate: All CSV files load into PowerBI successfully

### 5.2 Post-MVP Enhancements (Days 6-10)

#### **Stretch Goal 1: Advanced Scoring**
- [ ] Incorporate user-level features (order frequency, avg basket size)
- [ ] Time-based weighting (recent orders weighted higher)
- [ ] Diversity penalty (avoid recommending same aisle)

#### **Stretch Goal 2: PowerBI Dashboard**
- [ ] Build interactive PowerBI report (see Section 6)
- [ ] Add slicers (department, aisle, time of day)
- [ ] Create drill-through pages for product details

#### **Stretch Goal 3: Model Improvements**
- [ ] Experiment with sequential pattern mining (PrefixSpan)
- [ ] Add collaborative filtering (ALS) for user-based recs
- [ ] Ensemble: Combine rules + CF + popularity

#### **Stretch Goal 4: Production Readiness**
- [ ] Dockerize the pipeline
- [ ] Add logging and monitoring
- [ ] Create CI/CD pipeline (GitHub Actions)

---

## 6. PowerBI Deliverables Plan

### 6.1 Report Structure (5 Pages)

#### **Page 1: Executive Summary**
**Purpose**: High-level KPIs and project overview

**Visuals**:
- Card: Total products analyzed
- Card: Total association rules discovered
- Card: Model hit-rate@5
- Card: Coverage (% of products recommended)
- Clustered bar chart: Top 10 product pairs by lift
- Text box: Project description and methodology summary

**Slicers**: None (overview page)

---

#### **Page 2: Product Affinity Analysis**
**Purpose**: Explore which products are bought together

**Visuals**:
- Matrix: Product affinity heatmap (top 20×20 products by co-occurrence)
- Table: Top 50 product pairs (product_a, product_b, lift, confidence, support)
- Scatter plot: Confidence vs. Lift (bubble size = support)
- Slicer: Department filter
- Slicer: Minimum lift threshold (slider)

**Narrative**: "Customers who buy X are Y% more likely to buy Z"

---

#### **Page 3: Cross-Sell Opportunities by Aisle**
**Purpose**: Identify aisle-level cross-sell strategies

**Visuals**:
- Treemap: Aisle-to-aisle affinity (size = lift, color = confidence)
- Stacked bar chart: Top 10 aisle pairs by transaction count
- Table: Aisle cross-sell recommendations (aisle_from, aisle_to, top_products, avg_lift)
- Slicer: Source aisle filter

**Narrative**: "Shoppers in the 'Fresh Fruits' aisle should be recommended items from 'Yogurt' (lift=2.3)"

---

#### **Page 4: Department-Level Insights**
**Purpose**: Strategic view for category managers

**Visuals**:
- Sankey diagram: Department-to-department flow (based on rules)
- Clustered column chart: Avg basket size by department
- Line chart: Reorder rate by department
- Table: Department cross-sell summary
- Slicer: Department filter

**Narrative**: "Dairy department has highest reorder rate (68%) and strong affinity with Produce"

---

#### **Page 5: Recommendation Examples & Model Performance**
**Purpose**: Show concrete examples and validate model quality

**Visuals**:
- Table: Example baskets + recommendations (basket_items, recommended_items, rule_used, confidence)
- Gauge: Hit-Rate@5 vs. target (15%)
- Gauge: Hit-Rate@10 vs. target (25%)
- Clustered bar chart: Model vs. baseline performance
- Line chart: Coverage by top-K (K=1 to 20)

**Slicers**: None (validation page)

**Narrative**: "Our rule-based model achieves 18% hit-rate@5, outperforming popularity baseline by 6 percentage points"

---

### 6.2 Data Connections

PowerBI will connect to the following CSV files in `exports/powerbi/`:

1. `product_affinity.csv` → Page 2
2. `aisle_crosssell.csv` → Page 3
3. `dept_crosssell.csv` → Page 4
4. `top_rules.csv` → Pages 2, 3, 4
5. `recommendation_examples.csv` → Page 5
6. `evaluation_summary.csv` → Page 5

### 6.3 Design Guidelines

- **Color Palette**: Use Instacart brand colors (green #43B02A, white, gray)
- **Fonts**: Segoe UI (default), bold for headers
- **Interactivity**: Enable cross-filtering between visuals
- **Tooltips**: Add custom tooltips with rule details
- **Bookmarks**: Create bookmarks for key insights (e.g., "Top 5 Cross-Sell Opportunities")

---

## 7. Validation & Evaluation Plan

### 7.1 Data Quality Checks (Automated)

**Script**: `tests/test_data_quality.py`

```python
def test_no_null_product_ids():
    """Ensure no null product_ids in baskets"""
    assert baskets_df.filter(col("product_id").isNull()).count() == 0

def test_basket_size_reasonable():
    """Baskets should have 1-100 items"""
    assert baskets_df.filter((col("basket_size") < 1) | (col("basket_size") > 100)).count() == 0

def test_train_test_no_overlap():
    """Train and test sets should not overlap"""
    train_users = set(train_df.select("user_id").distinct().collect())
    test_users = set(test_df.select("user_id").distinct().collect())
    assert len(train_users.intersection(test_users)) == 0  # Temporal split, same users OK but different orders
```

**Run**: `pytest tests/test_data_quality.py`

---

### 7.2 Offline Evaluation Metrics

**Script**: `scripts/evaluate_model.py`

**Metrics**:

1. **Hit-Rate@K**: % of test baskets where at least one recommended item was actually purchased
   - Target: Hit-Rate@5 ≥ 15%, Hit-Rate@10 ≥ 25%

2. **Coverage**: % of unique products that appear in at least one recommendation
   - Target: ≥ 50% (avoid recommending only popular items)

3. **Diversity**: Average intra-list diversity (unique aisles in top-K)
   - Target: ≥ 3 aisles per top-10 recommendation

4. **Lift over Baseline**: Improvement over popularity-based recommender
   - Target: ≥ 5 percentage points improvement in hit-rate

**Baseline**: Recommend top-K most popular products (by reorder rate)

**Run**: `python scripts/evaluate_model.py`

**Output**: `artifacts/evaluation_metrics.json`

```json
{
  "hit_rate_at_5": 0.18,
  "hit_rate_at_10": 0.27,
  "coverage": 0.62,
  "avg_diversity": 3.4,
  "baseline_hit_rate_at_5": 0.12,
  "lift_over_baseline": 0.06
}
```

---

### 7.3 Manual Validation Steps

1. **Spot-Check Rules**:
   - Inspect `artifacts/association_rules.parquet`
   - Verify rules make intuitive sense (e.g., {milk, eggs} → bread)
   - Check for nonsensical rules (flag for investigation)

2. **Recommendation Examples**:
   - Review `exports/powerbi/recommendation_examples.csv`
   - Validate that recommendations are relevant to basket context
   - Test edge cases (single-item baskets, large baskets)

3. **PowerBI Load Test**:
   - Import all CSV files into PowerBI Desktop
   - Verify relationships are auto-detected correctly
   - Test slicers and cross-filtering
   - Confirm visuals render without errors

---

### 7.4 Sanity Checks

- [ ] Total number of rules > 1000 (sufficient coverage)
- [ ] Average rule confidence > 0.3 (quality threshold)
- [ ] Top 10 products by popularity match domain knowledge (e.g., bananas, milk)
- [ ] Aisle affinity makes sense (e.g., pasta → pasta sauce)
- [ ] No products with 100% reorder rate (data leakage check)

---

## 8. Risks & Mitigations

### 8.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Spark memory errors on laptop** | Medium | High | Use Spark config to limit memory (4GB driver, 2GB executor), sample data for development, use parquet compression |
| **FP-Growth too slow** | Low | Medium | Tune min_support (start at 0.01), parallelize across partitions, use Spark UI to profile |
| **Poor model performance (hit-rate < 10%)** | Medium | High | Implement multiple baselines, tune hyperparameters, add popularity priors, consider hybrid approach |
| **PowerBI file size too large** | Low | Medium | Aggregate data before export, use parquet instead of CSV, limit to top-N rules/products |
| **Data quality issues (nulls, duplicates)** | Medium | Medium | Implement automated data quality tests, add cleaning steps, document assumptions |

### 8.2 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Recommendations not actionable** | Medium | High | Focus on explainability (show rules), provide aisle-level insights, include confidence scores |
| **Stakeholders don't understand metrics** | Medium | Medium | Use business-friendly language in PowerBI, add tooltips, create executive summary page |
| **Model bias toward popular items** | High | Medium | Track coverage metric, add diversity penalty, report long-tail performance separately |

### 8.3 Data Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Dataset outdated (2017 data)** | High | Low | Acknowledge in documentation, focus on methodology (transferable to new data) |
| **Train/test leakage** | Low | High | Implement strict temporal split, add unit tests to verify no overlap |
| **Insufficient test data** | Low | Medium | Ensure test set has ≥10K baskets, stratify by basket size if needed |

---

## 9. Definition of Done

### 9.1 Code Deliverables

- [ ] All scripts in `scripts/` run end-to-end without errors
- [ ] `README.md` includes:
  - Project overview
  - Setup instructions (conda environment)
  - Data download instructions (Kaggle API or manual)
  - Run instructions for each script
  - Expected outputs
- [ ] `cursor.md` (this document) saved at repo root
- [ ] All code follows PEP 8 (validated with `black` and `flake8`)
- [ ] Unit tests pass (`pytest tests/`)
- [ ] Git history is clean (meaningful commit messages)

### 9.2 Data Deliverables

- [ ] `data/processed/` contains:
  - `baskets.parquet`
  - `product_stats.parquet`
  - `aisle_dept_rollups.parquet`
- [ ] `data/validation/` contains:
  - `train_baskets.parquet`
  - `test_baskets.parquet`
- [ ] `artifacts/` contains:
  - `association_rules.parquet` (≥1000 rules)
  - `top_recommendations.parquet`
  - `evaluation_metrics.json`
- [ ] `exports/powerbi/` contains all 6 CSV files + data dictionary

### 9.3 Model Performance

- [ ] Hit-Rate@5 ≥ 15%
- [ ] Hit-Rate@10 ≥ 25%
- [ ] Coverage ≥ 50%
- [ ] Lift over baseline ≥ 5 percentage points
- [ ] All metrics documented in `evaluation_metrics.json`

### 9.4 PowerBI Deliverables

- [ ] All 5 pages implemented as designed
- [ ] Data loads without errors
- [ ] Slicers and cross-filtering work correctly
- [ ] Report tells a coherent story (executive summary → details → validation)
- [ ] `docs/powerbi_guide.md` includes setup instructions

### 9.5 Documentation

- [ ] `docs/data_dictionary.md` documents all schemas
- [ ] `docs/methodology.md` explains:
  - FP-Growth algorithm
  - Scoring logic
  - Evaluation approach
- [ ] `exports/powerbi/data_dictionary.md` explains PowerBI tables
- [ ] Code comments explain non-obvious logic
- [ ] Jupyter notebooks include markdown explanations

### 9.6 Reproducibility

- [ ] Fresh clone of repo + environment setup runs successfully
- [ ] All paths are relative or configurable (no hardcoded absolute paths)
- [ ] Data download instructions are clear
- [ ] Scripts can be run in any order (or dependencies are documented)
- [ ] Outputs are deterministic (or random seed is set)

---

## 10. Next Steps (Post-Planning)

Once this plan is approved, the implementation will proceed in the following order:

1. **Environment Setup** (Day 1 morning)
   - Create conda environment
   - Download Instacart dataset
   - Set up folder structure

2. **Data Pipeline** (Day 1-2)
   - Implement ingestion, cleaning, transformation
   - Create train/test split
   - Validate data quality

3. **Model Training** (Day 3)
   - Implement FP-Growth
   - Generate association rules
   - Implement baseline

4. **Evaluation** (Day 4)
   - Implement scoring logic
   - Run offline evaluation
   - Validate metrics

5. **PowerBI Export** (Day 5)
   - Generate aggregated tables
   - Create data dictionary
   - Test PowerBI load

6. **Documentation & Polish** (Day 5 afternoon)
   - Update README
   - Write methodology docs
   - Final testing

7. **PowerBI Dashboard** (Post-MVP)
   - Build interactive report
   - Add storytelling elements
   - User testing

---

## 11. Open Questions (for User Review)

> [!IMPORTANT]
> Please review the following questions and provide feedback:

1. **Data Access**: Do you already have the Instacart dataset downloaded, or should the setup instructions include Kaggle API authentication?

2. **Compute Resources**: What are your laptop specs (RAM, CPU cores)? This will help tune Spark memory settings. (Assumption: 16GB RAM, 4 cores)

3. **PowerBI License**: Do you have PowerBI Desktop installed? (Free version is sufficient for local development)

4. **Timeline Flexibility**: The 5-day MVP timeline is aggressive. Is there flexibility to extend to 7-10 days if needed?

5. **Evaluation Targets**: Are the hit-rate targets (15%@5, 25%@10) acceptable, or do you have different expectations?

6. **Stretch Goals Priority**: Which post-MVP enhancement is most important to you? (Advanced scoring, PowerBI dashboard, model improvements, or production readiness)

---

## 12. Assumptions

- Instacart dataset is publicly available and can be downloaded from Kaggle
- Development machine has ≥16GB RAM and ≥4 CPU cores
- PowerBI Desktop is available (free download)
- No cloud deployment required (local development only)
- Python 3.10+ is acceptable
- User is familiar with basic PySpark and PowerBI concepts
- Git is installed and configured
- Jupyter notebooks are optional (for exploration, not required for pipeline)

---

**Plan Version**: 1.0  
**Last Updated**: 2026-02-16  
**Status**: Ready for Review
