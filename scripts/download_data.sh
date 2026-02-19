#!/bin/bash
# Download Instacart Dataset from Kaggle
# Requires: kaggle CLI installed and configured

set -e

echo "=========================================="
echo "INSTACART DATASET DOWNLOAD"
echo "=========================================="
echo ""

# Check if kaggle is installed
if ! command -v kaggle &> /dev/null; then
    echo "❌ Kaggle CLI not found"
    echo ""
    echo "Please install kaggle CLI:"
    echo "  pip install kaggle"
    echo ""
    echo "Then configure credentials:"
    echo "  1. Go to https://www.kaggle.com/settings"
    echo "  2. Click 'Create New API Token'"
    echo "  3. Save kaggle.json to ~/.kaggle/"
    echo "  4. chmod 600 ~/.kaggle/kaggle.json"
    exit 1
fi

# Check if kaggle credentials are configured
if [ ! -f ~/.kaggle/kaggle.json ]; then
    echo "❌ Kaggle credentials not found"
    echo ""
    echo "Please configure kaggle credentials:"
    echo "  1. Go to https://www.kaggle.com/settings"
    echo "  2. Click 'Create New API Token'"
    echo "  3. Save kaggle.json to ~/.kaggle/"
    echo "  4. chmod 600 ~/.kaggle/kaggle.json"
    exit 1
fi

echo "✓ Kaggle CLI found and configured"
echo ""

# Create data/raw directory if it doesn't exist
mkdir -p data/raw

# Download dataset
echo "Downloading Instacart Market Basket Analysis dataset..."
echo "(This may take 5-10 minutes depending on your connection)"
echo ""

kaggle competitions download -c instacart-market-basket-analysis -p data/raw/

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Download complete"
else
    echo ""
    echo "❌ Download failed"
    echo ""
    echo "Manual download instructions:"
    echo "  1. Visit: https://www.kaggle.com/c/instacart-market-basket-analysis/data"
    echo "  2. Accept competition rules (if prompted)"
    echo "  3. Download all files"
    echo "  4. Place in data/raw/ directory"
    exit 1
fi

# Unzip the dataset
echo ""
echo "Extracting files..."

cd data/raw

# Check if zip file exists
if [ -f instacart-market-basket-analysis.zip ]; then
    unzip -o instacart-market-basket-analysis.zip
    echo "✓ Files extracted"
    
    # Remove zip file to save space
    rm instacart-market-basket-analysis.zip
    echo "✓ Cleaned up zip file"
else
    echo "⚠️  No zip file found, checking if files already exist..."
fi

cd ../..

# Verify all required files exist
echo ""
echo "Verifying required files..."

required_files=(
    "orders.csv"
    "order_products__prior.csv"
    "order_products__train.csv"
    "products.csv"
    "aisles.csv"
    "departments.csv"
)

all_present=true

for file in "${required_files[@]}"; do
    if [ -f "data/raw/$file" ]; then
        size=$(du -h "data/raw/$file" | cut -f1)
        echo "  ✓ $file ($size)"
    else
        echo "  ✗ $file (missing)"
        all_present=false
    fi
done

echo ""

if [ "$all_present" = true ]; then
    echo "=========================================="
    echo "✅ DATASET DOWNLOAD COMPLETE"
    echo "=========================================="
    echo ""
    echo "All 6 required CSV files are present in data/raw/"
    echo ""
    echo "Next step: python scripts/run_etl.py"
else
    echo "=========================================="
    echo "❌ DATASET INCOMPLETE"
    echo "=========================================="
    echo ""
    echo "Some files are missing. Please download manually:"
    echo "  https://www.kaggle.com/c/instacart-market-basket-analysis/data"
    exit 1
fi
