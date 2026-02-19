# Windows VM Power BI Desktop Update

**Date**: 2026-02-16  
**Status**: ✅ Complete

## Summary

Updated the repository to support **Power BI Desktop in Windows VM** workflow instead of Power BI Service (web), since personal email sign-up is not available.

---

## Changes Made

### 1. Documentation Updates

#### ✅ `docs/powerbi_guide.md` - Complete Rewrite
**Changes**:
- Removed all Power BI Service (web) references
- Added Power BI Desktop (Windows VM) workflow
- Added VM setup instructions (Parallels/VMware)
- Added shared folder configuration
- Updated all steps for Desktop instead of web interface
- Added CSV import instructions
- Updated relationship creation for Desktop Model view
- Added local .pbix save workflow (no sign-in required)
- Added data refresh workflow (simple: re-export → refresh in Desktop)
- Added VM performance tips and troubleshooting

**Key Sections**:
1. Prerequisites (Windows VM + Power BI Desktop)
2. VM Setup (shared folder configuration)
3. Generate Exports (macOS)
4. Import Data in Power BI Desktop (Windows VM)
5. Create Relationships (Model View)
6. Build Report (Report View)
7. Save Report Locally (.pbix)
8. Data Refresh Workflow
9. Troubleshooting (VM-specific)
10. macOS + Windows VM Setup notes

---

### 2. Export Script Updates

#### ✅ `scripts/export_powerbi_bundle.py` - Refocused
**Changes**:
- Removed Excel bundle generation focus
- Changed to CSV-only export (preferred for Power BI Desktop)
- Updated output messages for Windows VM workflow
- Added shared folder path examples (Parallels/VMware)
- Updated next steps instructions

**Output**:
- 6 CSV files (not Excel workbook)
- `data_dictionary.md` with relationship instructions

---

### 3. Source Code Updates

#### ✅ `src/exports/powerbi_export.py` - Simplified
**Changes**:
- Removed `export_excel_bundle()` function
- Kept `export_csv_files()` as primary export
- Updated docstrings to focus on CSV exports
- Updated `generate_data_dictionary()` to include Power BI Desktop relationship instructions
- Removed Excel/openpyxl dependencies from function docs

---

### 4. README Updates

#### ✅ `README.md` - Updated Workflow
**Changes**:
1. **Prerequisites**: Changed to "Windows VM + Power BI Desktop"
2. **Step 4**: Updated to "Export for Power BI Desktop" (CSV files)
3. **Step 5**: New section "Build Dashboard in Power BI Desktop (Windows VM)"
   - Start VM
   - Open Power BI Desktop
   - Import CSVs from shared folder
   - Create relationships
   - Build report
   - Save .pbix locally
4. **Power BI Dashboard Section**: Renamed to "Power BI Dashboard (Windows VM Workflow)"
   - Updated architecture description
   - Updated quick start steps
   - Updated data refresh workflow

---

### 5. Quick Start Guide Updates

#### ✅ `QUICKSTART.md` - Updated
**Changes**:
1. **Step 5**: Changed from "Upload to Power BI Service" to "Build Dashboard in Windows VM"
2. **Quick Commands**: Updated Power BI commands:
   - Changed from Excel preview to CSV preview
   - Added data dictionary viewing command

---

### 6. Data Dictionary Updates

#### ✅ `exports/powerbi/data_dictionary.md` - Updated
**Changes**:
1. **Header**: Changed from "Power BI Service" to "Power BI Desktop (Windows VM workflow)"
2. **Export Format**: Changed from Excel bundle to CSV files
3. **Data Relationships**: 
   - Updated instructions for Power BI Desktop Model view
   - Added "How" column with drag-and-drop instructions
   - Specified cardinality and cross-filter settings
   - Added "Active" status
4. **Refresh Strategy**: 
   - Changed from "manual upload" to "simple refresh"
   - Updated workflow: re-export on Mac → refresh in Desktop
   - Explained why it works (shared folder)

---

## What Was NOT Changed

### Preserved Files
- ✅ `cursor.md` - Implementation plan (unchanged)
- ✅ `environment.yml` - Conda environment (unchanged)
- ✅ `requirements.txt` - Python dependencies (openpyxl still included, not removed)
- ✅ All source code modules (only `powerbi_export.py` simplified)
- ✅ All test files
- ✅ `docs/data_dictionary.md` - Upstream data schemas
- ✅ `docs/methodology.md` - Algorithm explanation
- ✅ Folder structure

### Backward Compatibility
- ✅ CSV export functions maintained
- ✅ All original export paths in `config/paths.py`
- ✅ Script names unchanged (still `export_powerbi_bundle.py`)

---

## Workflow Comparison

### BEFORE (Power BI Service - Web)
1. Run PySpark pipeline on macOS
2. Generate Excel workbook
3. Upload to Power BI Service (web)
4. Build report in web interface
5. Share via web

**Issue**: Cannot sign up with personal email

### AFTER (Power BI Desktop - VM)
1. Run PySpark pipeline on macOS
2. Generate CSV files
3. Start Windows VM
4. Open Power BI Desktop (no sign-in)
5. Import CSVs from shared folder
6. Build report in Desktop
7. Save .pbix locally

**Benefit**: No sign-in required, full local control

---

## Implementation Status

### ✅ Complete (Documentation & Structure)
1. Power BI Desktop guide fully rewritten
2. CSV export script updated (structure)
3. README updated with VM workflow
4. QUICKSTART updated
5. Data dictionary updated
6. Source code simplified (removed Excel focus)

### 🔨 To Implement (Code)
1. `src/exports/powerbi_export.py`:
   - `export_csv_files()` - Generate 6 CSV files
   - `generate_data_dictionary()` - Update data dictionary
   - `export_all()` - Orchestrate all exports

**Note**: All function signatures and TODOs are in place. Implementation will happen in Day 5 (Milestone 5).

---

## VM Setup Requirements

### Software Needed
1. **Parallels Desktop** ($99/year) or **VMware Fusion** (free for personal use)
2. **Windows 10/11** (Home edition sufficient, ~$140 or use evaluation copy)
3. **Power BI Desktop** (free download from Microsoft)

### VM Configuration
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: 2 cores minimum, 4 cores recommended
- **Disk**: 40GB for Windows + Power BI Desktop
- **Shared Folder**: Configure `exports/powerbi` folder

### One-Time Setup
1. Install VM software (Parallels/VMware)
2. Install Windows in VM
3. Install Power BI Desktop in Windows
4. Configure shared folder
5. Test CSV import from shared folder

**Total setup time**: ~2-3 hours (one-time)

---

## Testing Checklist

When implementing the export functions, test:

### 1. CSV Generation (macOS)
```bash
python scripts/export_powerbi_bundle.py
ls -lh exports/powerbi/*.csv
head -n 5 exports/powerbi/product_affinity.csv
```

### 2. Shared Folder Access (Windows VM)
- Start Windows VM
- Navigate to shared folder:
  - Parallels: `\\Mac\Home\Desktop\codeProjects\instacart-next-item-recs\exports\powerbi`
  - VMware: `\\vmware-host\Shared Folders\powerbi`
- Verify all 6 CSV files visible

### 3. Power BI Desktop Import
- Open Power BI Desktop
- Get Data → Text/CSV
- Import all 6 CSV files
- Verify data types (numeric columns should be numbers)

### 4. Relationships
- Switch to Model view
- Create 3 relationships as documented
- Verify relationships are active (solid lines)

### 5. Data Refresh
- On macOS: Re-run export script
- In Windows VM: Open .pbix → Home → Refresh
- Verify data updates

---

## Next Milestone

**Milestone 1 (Day 1): Data Ingestion & Transformation**

Now that the repository structure is complete and VM workflow is documented, proceed with:

1. Download Instacart dataset from Kaggle
2. Implement `src/data/ingest.py` - Load CSVs into Spark
3. Implement `src/data/clean.py` - Data quality checks
4. Implement `src/data/transform.py` - Feature engineering
5. Implement `src/data/split.py` - Train/test split
6. Run `python scripts/run_etl.py`

**See `cursor.md` Section 5.1 for detailed Day 1 tasks.**

---

## Constraints Met

✅ **No Power BI Service**: Uses Power BI Desktop only  
✅ **No sign-in required**: Local .pbix authoring  
✅ **macOS + Windows VM**: PySpark on Mac, Power BI in VM  
✅ **CSV exports**: Preferred format for Power BI Desktop  
✅ **Shared folder**: Seamless data transfer  
✅ **MVP-focused**: Simple, reproducible workflow  
✅ **Local .pbix save**: No cloud dependencies

---

## Files Changed Summary

| File | Type | Description |
|------|------|-------------|
| `docs/powerbi_guide.md` | Modified | Complete rewrite for Power BI Desktop in VM |
| `scripts/export_powerbi_bundle.py` | Modified | Refocused on CSV exports |
| `src/exports/powerbi_export.py` | Modified | Removed Excel bundle, kept CSV |
| `README.md` | Modified | Updated workflow for VM |
| `QUICKSTART.md` | Modified | Updated steps for VM |
| `exports/powerbi/data_dictionary.md` | Modified | Updated for Desktop relationships |
| `WINDOWS_VM_UPDATE.md` | New | This summary document |

**Total files changed**: 7 (6 modified, 1 new)

---

## User Action Required

### Now
1. **Review changes**: All documentation updated
2. **Proceed to Milestone 1**: Start implementing data pipeline

### Before Day 5 (PowerBI Export)
1. **Set up Windows VM**: Install Parallels/VMware + Windows
2. **Install Power BI Desktop**: Download from Microsoft
3. **Configure shared folder**: Set up `exports/powerbi` folder sharing
4. **Test access**: Verify Windows VM can see macOS files

### Day 5 (When implementing exports)
1. **Implement CSV export functions**: See TODOs in `src/exports/powerbi_export.py`
2. **Test in Power BI Desktop**: Import CSVs and build sample visual
3. **Save .pbix locally**: Test complete workflow

---

**Status**: ✅ Ready for Milestone 1 implementation
