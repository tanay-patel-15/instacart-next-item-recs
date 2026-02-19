# Changes Checklist - Windows VM Power BI Desktop Update

## ✅ Completed Changes

### Documentation Updates

- [x] **`docs/powerbi_guide.md`** - Complete rewrite for Power BI Desktop in Windows VM
  - Removed Power BI Service (web) workflow
  - Added VM setup instructions (Parallels/VMware)
  - Added shared folder configuration
  - Added CSV import workflow
  - Added Desktop Model view relationship creation
  - Added local .pbix save (no sign-in required)
  - Added simple refresh workflow
  - Added VM performance tips and troubleshooting

### Script Updates

- [x] **`scripts/export_powerbi_bundle.py`** - Refocused on CSV exports
  - Removed Excel bundle generation focus
  - Updated to CSV-only export
  - Updated output messages for VM workflow
  - Added shared folder path examples

### Source Code Updates

- [x] **`src/exports/powerbi_export.py`** - Simplified for CSV
  - Removed `export_excel_bundle()` function
  - Kept `export_csv_files()` as primary export
  - Updated docstrings for CSV focus
  - Updated `generate_data_dictionary()` for Desktop relationships

### User-Facing Documentation

- [x] **`README.md`** - Updated for VM workflow
  - Changed prerequisites (Windows VM + Power BI Desktop)
  - Updated Step 4: Export for Power BI Desktop
  - Added Step 5: Build Dashboard in Windows VM
  - Updated Power BI Dashboard section (VM workflow)
  - Updated data refresh instructions

- [x] **`QUICKSTART.md`** - Updated quick start
  - Changed Step 5 to Windows VM workflow
  - Updated Power BI commands (CSV preview instead of Excel)

### Data Documentation

- [x] **`exports/powerbi/data_dictionary.md`** - Updated for Desktop
  - Changed from Power BI Service to Power BI Desktop
  - Updated export format (CSV files)
  - Added detailed relationship instructions for Desktop
  - Updated refresh strategy (simple refresh in Desktop)

### Summary Documents

- [x] **`WINDOWS_VM_UPDATE.md`** - Detailed change summary
  - Complete list of changes
  - Workflow comparison
  - VM setup requirements
  - Testing checklist
  - Next milestone guidance

- [x] **`VM_CHANGES_CHECKLIST.md`** - This checklist

---

## 📋 Key Changes Summary

### Workflow Change

**BEFORE (Power BI Service)**:
- Run PySpark on macOS
- Generate Excel workbook
- Upload to Power BI Service (web)
- Build report in browser
- **Issue**: Cannot sign up with personal email

**AFTER (Power BI Desktop in VM)**:
- Run PySpark on macOS
- Generate CSV files
- Open Power BI Desktop in Windows VM
- Import CSVs from shared folder
- Build report in Desktop
- Save .pbix locally (no sign-in)

### Export Format Change

**BEFORE**: `powerbi_bundle.xlsx` (Excel workbook with 6 sheets)  
**AFTER**: 6 individual CSV files

### Platform Change

**BEFORE**: Power BI Service (web-based)  
**AFTER**: Power BI Desktop (Windows VM)

---

## 🔨 Implementation TODOs (For Day 5)

When you reach Milestone 5 (Day 5: PowerBI Export), implement:

### `src/exports/powerbi_export.py`

```python
# TODO: Implement these 3 functions

1. export_csv_files(spark)
   - Load artifacts (rules, recommendations, metrics)
   - Transform to appropriate schemas
   - Generate 6 CSV files:
     * product_affinity.csv
     * aisle_crosssell.csv
     * dept_crosssell.csv
     * top_rules.csv
     * recommendation_examples.csv
     * evaluation_summary.csv
   - Ensure proper headers and data types

2. generate_data_dictionary(output_path)
   - Update data_dictionary.md
   - Include table schemas
   - Include relationship instructions for Power BI Desktop
   - Include cardinality and cross-filter settings
   - Include sample values

3. export_all(spark)
   - Orchestrate both functions above
   - Handle errors gracefully
   - Print progress messages
```

---

## 🧪 Testing Steps (For Day 5)

### 1. Test CSV Generation (macOS)

```bash
# Run export script
python scripts/export_powerbi_bundle.py

# Verify files exist
ls -lh exports/powerbi/*.csv

# Check file contents
head -n 5 exports/powerbi/product_affinity.csv
wc -l exports/powerbi/*.csv
```

### 2. Test Shared Folder Access (Windows VM)

1. Start Windows VM (Parallels/VMware)
2. Open File Explorer
3. Navigate to shared folder:
   - Parallels: `\\Mac\Home\Desktop\codeProjects\instacart-next-item-recs\exports\powerbi`
   - VMware: `\\vmware-host\Shared Folders\powerbi`
4. Verify all 6 CSV files are visible
5. Try opening one in Notepad to verify access

### 3. Test Power BI Desktop Import

1. Open Power BI Desktop in Windows VM
2. Click **Get Data** → **Text/CSV**
3. Navigate to shared folder
4. Import `product_affinity.csv`
5. Verify:
   - Data loads successfully
   - Column names are correct
   - Numeric columns are detected as numbers (not text)
6. Repeat for all 6 CSV files

### 4. Test Relationships

1. Switch to **Model** view (left sidebar)
2. Drag `top_rules[aisle_from]` to `aisle_crosssell[aisle_from]`
3. Set cardinality to Many-to-Many
4. Set cross-filter to Both
5. Verify relationship appears as solid line
6. Repeat for other relationships

### 5. Test Data Refresh

1. On macOS: Modify a CSV file (e.g., change a value)
2. In Windows VM: Open .pbix file
3. Click **Home** → **Refresh**
4. Verify data updates in visuals

---

## 🎯 Next Milestone

### Milestone 1 (Day 1): Data Ingestion & Transformation

**Goal**: Load and transform Instacart dataset

**Tasks**:
1. Download Instacart dataset from Kaggle
2. Implement `src/data/ingest.py`
3. Implement `src/data/clean.py`
4. Implement `src/data/transform.py`
5. Implement `src/data/split.py`
6. Run `python scripts/run_etl.py`

**Exit Criteria**:
- All 6 CSV files loaded into Spark
- Data quality checks pass
- Processed parquet files created
- Train/test split created

**See `cursor.md` Section 5.1 for detailed Day 1 implementation plan.**

---

## 💻 VM Setup (Before Day 5)

### Required Software

1. **VM Software** (choose one):
   - Parallels Desktop ($99/year, best performance)
   - VMware Fusion (free for personal use)

2. **Windows**:
   - Windows 10 Home (~$140)
   - Windows 11 Home (~$140)
   - Or use Windows evaluation copy (free, 90 days)

3. **Power BI Desktop** (free):
   - Download: https://aka.ms/pbidesktopstore
   - Install in Windows VM
   - No sign-in required for local .pbix files

### VM Configuration

**Minimum**:
- RAM: 4GB
- CPU: 2 cores
- Disk: 40GB

**Recommended**:
- RAM: 8GB
- CPU: 4 cores
- Disk: 60GB

### Shared Folder Setup

**Parallels**:
1. VM → Configure → Options → Shared Folders
2. Enable "Share Mac folders with Windows"
3. Add `instacart-next-item-recs/exports/powerbi` folder
4. Access in Windows: `\\Mac\Home\Desktop\codeProjects\instacart-next-item-recs\exports\powerbi`

**VMware Fusion**:
1. Virtual Machine → Settings → Sharing
2. Enable folder sharing
3. Add `instacart-next-item-recs/exports/powerbi` folder
4. Access in Windows: `\\vmware-host\Shared Folders\powerbi`

---

## 📊 Summary Statistics

### Changes Made
- **Files Modified**: 6
- **Files Created**: 2
- **Lines Changed**: ~300+
- **Functions Removed**: 1 (export_excel_bundle)
- **Functions Updated**: 3 (with new TODOs)

### Backward Compatibility
- ✅ CSV export functions maintained
- ✅ Script names unchanged
- ✅ No breaking changes to existing code

### Platform Support
- ✅ PySpark on macOS (native)
- ✅ Power BI Desktop in Windows VM
- ✅ Shared folder for data transfer
- ✅ No sign-in required
- ✅ Local .pbix save

---

## 🚀 Ready to Proceed

All documentation and structure changes are complete. You can now:

1. **Start Milestone 1** (Data Ingestion) - Implement the data pipeline
2. **Set up Windows VM** (before Day 5) - Install VM, Windows, Power BI Desktop
3. **Continue to Day 5** when ready - Implement CSV export functions
4. **Build dashboard in VM** after pipeline runs

**No blockers!** All changes are MVP-focused and reproducible.

---

## 📖 Key Documentation

| Document | Purpose |
|----------|---------|
| `cursor.md` | Full implementation plan (unchanged) |
| `docs/powerbi_guide.md` | Power BI Desktop in VM setup |
| `README.md` | Project overview and VM workflow |
| `QUICKSTART.md` | 5-minute quick start |
| `WINDOWS_VM_UPDATE.md` | Detailed change summary |
| `VM_CHANGES_CHECKLIST.md` | This checklist |

---

**Status**: ✅ All changes complete - Ready for Milestone 1
