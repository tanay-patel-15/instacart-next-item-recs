#!/bin/bash
# Run All Scripts - Complete Pipeline
# This script runs the entire recommendation system pipeline end-to-end

set -e  # Exit on error

echo "=========================================="
echo "INSTACART RECOMMENDATION SYSTEM"
echo "Complete Pipeline Execution"
echo "=========================================="
echo ""

# Check if conda environment is activated
if [[ -z "${CONDA_DEFAULT_ENV}" ]] || [[ "${CONDA_DEFAULT_ENV}" != "instacart-recs" ]]; then
    echo "⚠️  Warning: conda environment 'instacart-recs' is not activated"
    echo "Please run: conda activate instacart-recs"
    exit 1
fi

echo "✓ Environment: $CONDA_DEFAULT_ENV"
echo ""

# Step 1: ETL Pipeline
echo "Step 1/4: Running ETL Pipeline..."
python scripts/run_etl.py
if [ $? -eq 0 ]; then
    echo "✓ ETL Pipeline completed successfully"
else
    echo "✗ ETL Pipeline failed"
    exit 1
fi
echo ""

# Step 2: Model Training
echo "Step 2/4: Training FP-Growth Model..."
python scripts/train_model.py
if [ $? -eq 0 ]; then
    echo "✓ Model training completed successfully"
else
    echo "✗ Model training failed"
    exit 1
fi
echo ""

# Step 3: Model Evaluation
echo "Step 3/4: Evaluating Model..."
python scripts/evaluate_model.py
if [ $? -eq 0 ]; then
    echo "✓ Model evaluation completed successfully"
else
    echo "✗ Model evaluation failed"
    exit 1
fi
echo ""

# Step 4: Power BI Bundle Export
echo "Step 4/4: Exporting for Power BI Service..."
python scripts/export_powerbi_bundle.py
if [ $? -eq 0 ]; then
    echo "✓ Power BI bundle export completed successfully"
else
    echo "✗ Power BI bundle export failed"
    exit 1
fi
echo ""

echo "=========================================="
echo "PIPELINE COMPLETE"
echo "=========================================="
echo ""
echo "All outputs generated successfully!"
echo ""
echo "Next steps:"
echo "  1. Review evaluation metrics: artifacts/evaluation_metrics.json"
echo "  2. Upload powerbi_bundle.xlsx to Power BI Service (https://app.powerbi.com)"
echo "  3. Build report in Power BI web interface (see docs/powerbi_guide.md)"
echo "  4. Explore notebooks/ for detailed analysis"
echo ""
