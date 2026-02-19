# Instacart Next-Item Recommendation System

A data science project that creates explainable "next item" recommendations for grocery baskets using the Instacart Market Basket Analysis dataset, leveraging PySpark for scalable data processing and PowerBI for executive storytelling.

## 📋 Project Overview

This project implements an association rule mining approach (FP-Growth) to recommend the next items customers are likely to add to their grocery baskets. The system:

- Processes ~3.4M orders from 200K+ users
- Discovers product affinity patterns using PySpark MLlib
- Generates explainable recommendations with confidence scores
- Provides interactive PowerBI dashboards for business insights

**Key Features:**
- Scalable data processing with PySpark
- FP-Growth association rule mining
- Offline evaluation with Hit-Rate@K metrics
- PowerBI-ready exports for executive storytelling
- Explainable recommendations (rule-based)

## 🏗️ Project Structure

```
instacart-next-item-recs/
├── README.md                          # This file
├── cursor.md                          # Implementation plan
├── environment.yml                    # Conda environment
├── requirements.txt                   # Python dependencies
├── config/                            # Configuration files
├── data/                              # Data directory (gitignored)
│   ├── raw/                          # Raw Instacart CSV files
│   ├── processed/                    # Cleaned parquet files
│   └── validation/                   # Train/test split
├── src/                               # Source code
│   ├── data/                         # Data ingestion & transformation
│   ├── models/                       # Recommendation logic
│   ├── evaluation/                   # Offline evaluation
│   └── exports/                      # PowerBI export logic
├── notebooks/                         # Jupyter notebooks
├── scripts/                           # Executable scripts
├── tests/                             # Unit tests
├── artifacts/                         # Model outputs (gitignored)
├── exports/powerbi/                   # PowerBI-ready files
└── docs/                              # Documentation
```

## 🚀 Setup Instructions

### Prerequisites

- **macOS**: Python 3.10+, Conda (recommended) or pip, 16GB+ RAM for PySpark
- **Windows VM**: Parallels Desktop or VMware Fusion with Windows 10/11
- **Power BI Desktop**: Free download (install in Windows VM, no sign-in required)

### Option 1: Conda Environment (Recommended)

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate instacart-recs

# Verify installation
python -c "import pyspark; print(f'PySpark {pyspark.__version__} installed successfully')"
```

### Option 2: pip + venv

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pyspark; print(f'PySpark {pyspark.__version__} installed successfully')"
```

## 📊 Data Download

### Method 1: Kaggle API (Recommended)

```bash
# Install Kaggle CLI
pip install kaggle

# Configure Kaggle credentials (get from https://www.kaggle.com/settings)
# Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle competitions download -c instacart-market-basket-analysis

# Extract to data/raw/
unzip instacart-market-basket-analysis.zip -d data/raw/
```

### Method 2: Manual Download

1. Visit: https://www.kaggle.com/c/instacart-market-basket-analysis/data
2. Download all CSV files
3. Place in `data/raw/` directory

**Required files:**
- `orders.csv`
- `order_products__prior.csv`
- `order_products__train.csv`
- `products.csv`
- `aisles.csv`
- `departments.csv`

## 🏃 How to Run

### Step 1: Data Ingestion & Transformation (ETL)

```bash
python scripts/run_etl.py
```

**Output:**
- `data/processed/baskets.parquet`
- `data/processed/product_stats.parquet`
- `data/processed/aisle_dept_rollups.parquet`
- `data/validation/train_baskets.parquet`
- `data/validation/test_baskets.parquet`

**Expected runtime:** 10-15 minutes

### Step 2: Train FP-Growth Model

```bash
python scripts/train_model.py
```

**Output:**
- `artifacts/association_rules.parquet` (≥1000 rules)

**Expected runtime:** 5-10 minutes

### Step 3: Evaluate Model

```bash
python scripts/evaluate_model.py
```

**Output:**
- `artifacts/top_recommendations.parquet`
- `artifacts/evaluation_metrics.json`

**Expected metrics:**
- Hit-Rate@5: ≥15%
- Hit-Rate@10: ≥25%
- Coverage: ≥50%

**Expected runtime:** 5-10 minutes

### Step 4: Export for Power BI Desktop

```bash
python scripts/export_powerbi_bundle.py
```

**Output:**
- `exports/powerbi/*.csv` (6 CSV files for Power BI Desktop)
- `exports/powerbi/data_dictionary.md` (Schema documentation with relationships)

**Expected runtime:** 2-5 minutes

### Step 5: Build Dashboard in Power BI Desktop (Windows VM)

1. **Start Windows VM** (Parallels/VMware)
2. **Open Power BI Desktop** (no sign-in required)
3. **Import CSV files**: Get Data → Text/CSV
   - Navigate to shared folder (e.g., `\\Mac\Home\...\exports\powerbi`)
   - Import all 6 CSV files
4. **Create relationships**: See `exports/powerbi/data_dictionary.md` for details
5. **Build report**: Create 5 pages with visuals (see `docs/powerbi_guide.md`)
6. **Save locally**: File → Save As → `instacart_recommendations_dashboard.pbix`

**See `docs/powerbi_guide.md` for detailed step-by-step instructions**

### Run All Steps (End-to-End)

```bash
# Run complete pipeline
bash scripts/run_all.sh

# Or manually:
python scripts/run_etl.py && \
python scripts/train_model.py && \
python scripts/evaluate_model.py && \
python scripts/export_powerbi_bundle.py
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_data_quality.py
```

## 📈 Power BI Dashboard (Windows VM Workflow)

### Setup: macOS + Windows VM

**Architecture**:
- **macOS**: Run PySpark pipeline, generate CSV exports
- **Windows VM**: Run Power BI Desktop for visualization only
- **Shared Folder**: Seamless data transfer between macOS and VM

### Quick Start

1. **On macOS**: Generate CSV exports
   ```bash
   python scripts/export_powerbi_bundle.py
   ```

2. **In Windows VM**: Open Power BI Desktop
   - Get Data → Text/CSV
   - Navigate to shared folder
   - Import all 6 CSV files

3. **Build report**:
   - Create relationships (see `data_dictionary.md`)
   - Build 5 report pages
   - Save .pbix locally (no sign-in required)

### Report Structure

The dashboard includes 5 pages:
1. **Executive Summary** - KPIs and overview
2. **Product Affinity** - Which products are bought together
3. **Cross-Sell by Aisle** - Aisle-level recommendations
4. **Department Insights** - Strategic category view
5. **Model Performance** - Validation metrics and examples

### Data Refresh

When you re-run the pipeline:
1. **On macOS**: Re-run `python scripts/export_powerbi_bundle.py`
2. **In Windows VM**: Open .pbix → Home → Refresh
3. CSV files are automatically reloaded from shared folder

**See `docs/powerbi_guide.md` for detailed setup and VM configuration.**

## 🔧 Configuration

### Spark Settings

Edit `config/spark_config.py` to tune memory settings:

```python
# Default settings (for 16GB RAM)
spark = SparkSession.builder \
    .appName("InstacartRecs") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()
```

### Model Hyperparameters

Edit `config/model_params.yaml`:

```yaml
fp_growth:
  min_support: 0.01
  min_confidence: 0.3
  min_lift: 1.5

scoring:
  top_k: 10
  popularity_weight: 0.2
```

## 📝 Development Workflow

### Code Formatting

```bash
# Format code with black
black src/ scripts/ tests/

# Check linting
flake8 src/ scripts/ tests/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🐛 Troubleshooting

### PySpark Memory Errors

**Error:** `java.lang.OutOfMemoryError`

**Solution:**
```bash
# Reduce Spark memory in config/spark_config.py
spark.config("spark.driver.memory", "2g")

# Or sample data for development
df = df.sample(fraction=0.1)
```

### Slow FP-Growth Training

**Solution:**
```bash
# Increase min_support in config/model_params.yaml
min_support: 0.02  # (from 0.01)
```

### PowerBI File Too Large

**Solution:**
```bash
# Limit exports in scripts/export_powerbi.py
top_rules = rules.limit(10000)  # Top 10K rules only
```

## 📚 Documentation

- **Implementation Plan:** `cursor.md`
- **Data Dictionary:** `docs/data_dictionary.md`
- **Methodology:** `docs/methodology.md`
- **PowerBI Guide:** `docs/powerbi_guide.md`

## 🎯 Evaluation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Hit-Rate@5 | ≥15% | % of test baskets with ≥1 correct recommendation in top-5 |
| Hit-Rate@10 | ≥25% | % of test baskets with ≥1 correct recommendation in top-10 |
| Coverage | ≥50% | % of unique products that appear in recommendations |
| Diversity | ≥3 aisles | Average number of unique aisles in top-10 recommendations |

## 🤝 Contributing

This is a portfolio project. For questions or suggestions, please open an issue.

## 📄 License

This project uses the Instacart Market Basket Analysis dataset, which is available under Instacart's terms of use.

## 🙏 Acknowledgments

- **Dataset:** Instacart (via Kaggle)
- **Tech Stack:** PySpark, MLlib, PowerBI
- **Inspiration:** Association rule mining for retail recommendations

## 📧 Contact

For questions about this project, please refer to the documentation in `docs/` or open an issue.

---

**Project Status:** ✅ Milestone 0 Complete - Repository scaffold ready

**Next Steps:** Download Instacart dataset and run ETL pipeline
