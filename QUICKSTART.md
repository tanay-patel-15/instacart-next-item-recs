# Quick Start Guide

Get up and running with the Instacart Next-Item Recommendation System in 5 minutes.

---

## Step 1: Setup Environment (2 minutes)

### Option A: Conda (Recommended)

```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate instacart-recs

# Verify installation
python -c "import pyspark; print(f'✓ PySpark {pyspark.__version__} ready')"
```

### Option B: pip + venv

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pyspark; print(f'✓ PySpark {pyspark.__version__} ready')"
```

---

## Step 2: Download Data (3 minutes)

### Option A: Kaggle API 

```bash
# Install Kaggle CLI (if not already installed)
pip install kaggle

# Configure credentials (get from https://www.kaggle.com/settings)
# Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle competitions download -c instacart-market-basket-analysis

# Extract to data/raw/
unzip instacart-market-basket-analysis.zip -d data/raw/
```

### Option B: Manual Download

1. Visit: https://www.kaggle.com/c/instacart-market-basket-analysis/data
2. Download all CSV files
3. Place in `data/raw/` directory

**Required files** (6 total):
- ✓ orders.csv
- ✓ order_products__prior.csv
- ✓ order_products__train.csv
- ✓ products.csv
- ✓ aisles.csv
- ✓ departments.csv

---

## Step 3: Verify Setup

```bash
# Check data files
ls data/raw/*.csv

# Expected output:
# orders.csv
# order_products__prior.csv
# order_products__train.csv
# products.csv
# aisles.csv
# departments.csv

# Test configuration
python config/paths.py
# Expected: ✓ All directories created/verified
```

---

## Step 4: Run Pipeline (When Ready)

```bash
# Complete pipeline (all steps)
bash scripts/run_all.sh

# Or run individual steps:
python scripts/run_etl.py               # Step 1: ETL (10-15 min)
python scripts/train_model.py           # Step 2: Training (5-10 min)
python scripts/evaluate_model.py        # Step 3: Evaluation (5-10 min)
python scripts/export_powerbi_bundle.py # Step 4: Export (2-5 min)
```

## Step 5: Build Dashboard in Windows VM

```bash
# After running the pipeline:
# 1. Start Windows VM (Parallels/VMware)
# 2. Open Power BI Desktop (no sign-in needed)
# 3. Get Data → Text/CSV
# 4. Import CSV files from shared folder:
#    - Parallels: \\Mac\Home\...\exports\powerbi
#    - VMware: \\vmware-host\Shared Folders\powerbi
# 5. Create relationships (see data_dictionary.md)
# 6. Build report (see docs/powerbi_guide.md)
# 7. Save .pbix locally
```

---

## What's Next?

### For Development (Milestone 1)

Start implementing the data pipeline:

1. **Implement data ingestion**: `src/data/ingest.py`
2. **Implement data cleaning**: `src/data/clean.py`
3. **Implement transformations**: `src/data/transform.py`
4. **Implement train/test split**: `src/data/split.py`

Each file has TODO markers and function signatures ready.

### For Exploration

```bash
# Start Jupyter notebook
jupyter notebook

# Create new notebook in notebooks/
# Load data and explore
```

### For Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## Troubleshooting

### "Command not found: conda"

**Solution**: Install Miniconda from https://docs.conda.io/en/latest/miniconda.html

### "kaggle: command not found"

**Solution**: `pip install kaggle`

### "PySpark memory error"

**Solution**: Reduce memory in `config/spark_config.py`:
```python
spark.config("spark.driver.memory", "2g")  # Reduce from 4g
```

### "Data files not found"

**Solution**: Verify files in `data/raw/`:
```bash
ls -lh data/raw/
```

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `README.md` | Comprehensive documentation |
| `cursor.md` | Implementation plan |
| `MILESTONE_0_COMPLETE.md` | Milestone 0 summary |
| `config/model_params.yaml` | Tune hyperparameters |
| `config/spark_config.py` | Adjust Spark settings |

---

## Getting Help

- **Setup issues**: See `README.md` → Troubleshooting
- **Data schema**: See `docs/data_dictionary.md`
- **Methodology**: See `docs/methodology.md`
- **PowerBI**: See `docs/powerbi_guide.md`

---

## Quick Commands Cheat Sheet

```bash
# Environment
conda activate instacart-recs          # Activate environment
conda deactivate                       # Deactivate environment

# Data
ls data/raw/*.csv                      # Check raw data
python config/paths.py                 # Verify directories

# Pipeline
bash scripts/run_all.sh                # Run complete pipeline
python scripts/run_etl.py              # Run ETL only
python scripts/export_powerbi_bundle.py # Export for Power BI

# Power BI
head -n 5 exports/powerbi/product_affinity.csv # Preview CSV (macOS)
ls -lh exports/powerbi/                # Check export files
cat exports/powerbi/data_dictionary.md  # View relationships

# Testing
pytest tests/                          # Run all tests
pytest tests/test_data_quality.py      # Run specific test

# Code Quality
black src/ scripts/ tests/             # Format code
flake8 src/ scripts/ tests/            # Check linting
pre-commit run --all-files             # Run all hooks

# Jupyter
jupyter notebook                       # Start notebook server
```

---

**Ready to build?** Start with Milestone 1 (Data Ingestion) 🚀
