# Power BI Desktop Setup Guide (macOS + Windows VM)

**Platform**: Power BI Desktop running in Windows VM (Parallels/VMware)  
**macOS Setup**: Run PySpark locally, use VM only for Power BI Desktop

## Prerequisites

- **macOS**: Python 3.10+, PySpark environment (for data pipeline)
- **Windows VM**: Parallels Desktop or VMware Fusion with Windows installed
- **Power BI Desktop**: Free download from Microsoft (install in Windows VM)
- Completed pipeline execution (CSV files in `exports/powerbi/`)

## VM Setup (One-Time)

### Step 1: Install Power BI Desktop in Windows VM

1. Start your Windows VM (Parallels/VMware)
2. Download Power BI Desktop: https://aka.ms/pbidesktopstore
3. Install Power BI Desktop (no sign-in required for local authoring)
4. **Important**: You can use Power BI Desktop without signing in for local .pbix files

### Step 2: Configure Shared Folder

Set up folder sharing between macOS and Windows VM:

**Parallels**:
1. VM → Configure → Options → Shared Folders
2. Add `instacart-next-item-recs/exports/powerbi` folder
3. Access in Windows at `\\Mac\Home\Desktop\codeProjects\instacart-next-item-recs\exports\powerbi`

**VMware Fusion**:
1. Virtual Machine → Settings → Sharing
2. Enable folder sharing
3. Add `instacart-next-item-recs/exports/powerbi` folder
4. Access in Windows at `\\vmware-host\Shared Folders\powerbi`

---

## 1. Generate Exports (macOS)

### Step 1: Run Export Script

On your Mac, run the export script:

```bash
python scripts/export_powerbi_bundle.py
```

**Output**: CSV files in `exports/powerbi/`:
1. `product_affinity.csv` - Product pairs and affinity metrics
2. `aisle_crosssell.csv` - Aisle-level cross-sell opportunities
3. `dept_crosssell.csv` - Department-level insights
4. `top_rules.csv` - Association rules (human-readable)
5. `recommendation_examples.csv` - Example recommendations
6. `evaluation_summary.csv` - Model performance metrics
7. `data_dictionary.md` - Schema documentation with relationship suggestions

### Step 2: Verify Exports

```bash
# Check files exist
ls -lh exports/powerbi/*.csv

# Preview a file
head -n 5 exports/powerbi/product_affinity.csv
```

---

## 2. Import Data in Power BI Desktop (Windows VM)

### Step 1: Open Power BI Desktop

1. Switch to Windows VM
2. Launch Power BI Desktop
3. Skip sign-in (click "Maybe later" or close the prompt)
4. You're now in the main authoring canvas

### Step 2: Import CSV Files

Import all 6 CSV files:

1. Click **Get Data** → **Text/CSV**
2. Navigate to the shared folder:
   - Parallels: `\\Mac\Home\Desktop\codeProjects\instacart-next-item-recs\exports\powerbi`
   - VMware: `\\vmware-host\Shared Folders\powerbi`
3. Select `product_affinity.csv` → **Load**
4. Repeat for all 6 CSV files:
   - `product_affinity.csv`
   - `aisle_crosssell.csv`
   - `dept_crosssell.csv`
   - `top_rules.csv`
   - `recommendation_examples.csv`
   - `evaluation_summary.csv`

**Tip**: Power BI will auto-detect data types. Verify numeric columns are set to "Decimal Number" or "Whole Number".

---

## 3. Create Relationships (Model View)

### Step 1: Switch to Model View

1. Click the **Model** icon in the left sidebar (looks like a relationship diagram)
2. You'll see all 6 tables

### Step 2: Create Relationships

Power BI may auto-detect some relationships. Create these manually if needed:

**Recommended Relationships**:

1. **product_affinity → top_rules** (many-to-many)
   - From: `product_affinity[product_a]`
   - To: `top_rules[antecedent]`
   - Cardinality: Many-to-Many
   - Cross-filter direction: Both

2. **aisle_crosssell → top_rules** (many-to-many)
   - From: `aisle_crosssell[aisle_from]`
   - To: `top_rules[aisle_from]`
   - Cardinality: Many-to-Many

3. **dept_crosssell → top_rules** (many-to-many)
   - From: `dept_crosssell[department_from]`
   - To: `top_rules[department_from]`
   - Cardinality: Many-to-Many

**To create a relationship**:
- Click **Model** view (left sidebar)
- Drag a column from one table to the matching column in another
- Configure cardinality and cross-filter direction in the properties pane

### Step 3: Create Measures (Optional)

Add calculated measures for better reporting:

**Example Measures**:

```dax
// Total Products
Total Products = DISTINCTCOUNT(product_affinity[product_a])

// Total Rules
Total Rules = COUNTROWS(top_rules)

// Avg Confidence
Avg Confidence = AVERAGE(top_rules[confidence])

// Avg Lift
Avg Lift = AVERAGE(top_rules[lift])
```

**To create a measure**:
1. Right-click a table in the **Fields** pane (right side)
2. Select **New measure**
3. Enter the DAX formula in the formula bar
4. Press Enter

---

## 4. Build Report (Report View)

### Step 1: Switch to Report View

1. Click the **Report** icon in the left sidebar (looks like a bar chart)
2. You're now in the report canvas

### Step 2: Create Report Pages

You'll create 5 pages for the dashboard:

---

### Page 1: Executive Summary

**Purpose**: High-level KPIs and project overview

**How to Build**:

1. **Add 4 Card visuals** (top row):
   - Click blank area on canvas
   - In Visualizations pane (right), click **Card** icon
   - Drag field to the card:
     - Card 1: Drag `product_affinity[product_a]` → Change aggregation to "Count (Distinct)"
     - Card 2: Drag `top_rules[rule_id]` → Change aggregation to "Count"
     - Card 3: Drag `evaluation_summary[metric_value]` → Filter to "hit_rate_at_5" row
     - Card 4: Drag `evaluation_summary[metric_value]` → Filter to "coverage" row
   - Format cards: Select card → Format pane → Data label → Display units, decimal places

2. **Add Clustered Bar Chart** (below cards):
   - Click **Clustered bar chart** in Visualizations pane
   - Y-axis: Drag `product_affinity[product_a]` (or create calculated column for "Product A → Product B")
   - X-axis: Drag `product_affinity[lift]`
   - Sort: Click "..." on visual → Sort by lift → Descending
   - Filter: Filters pane → Top N filter → Top 10 by lift

**Layout Tip**: Use Format → Align tools in the ribbon to arrange visuals neatly

---

### Page 2: Product Affinity Analysis

**Purpose**: Explore which products are bought together

**Visuals**:
1. **Table**: Top 50 product pairs
   - Columns: `product_a`, `product_b`, `lift`, `confidence`, `support`
   - Sort: Descending by lift
   - Top N: 50
2. **Scatter Plot**: Confidence vs. Lift
   - X-axis: `product_affinity[confidence]`
   - Y-axis: `product_affinity[lift]`
   - Size: `product_affinity[support]`
   - Tooltip: Product names
3. **Slicer**: Minimum lift threshold
   - Field: `product_affinity[lift]`
   - Type: Slider (range 1.0 to 5.0)

**Interactivity**: Enable cross-filtering between visuals

---

### Page 3: Cross-Sell Opportunities by Aisle

**Purpose**: Identify aisle-level cross-sell strategies

**Visuals**:
1. **Stacked Bar Chart**: Top 10 aisle pairs
   - X-axis: `aisle_crosssell[aisle_from]` + `aisle_crosssell[aisle_to]`
   - Y-axis: `aisle_crosssell[avg_lift]`
   - Sort: Descending by avg_lift
   - Top N: 10
2. **Table**: Aisle cross-sell recommendations
   - Columns: `aisle_from`, `aisle_to`, `top_products`, `avg_lift`
   - Sort: Descending by avg_lift
3. **Slicer**: Source aisle filter
   - Field: `aisle_crosssell[aisle_from]`
   - Type: Dropdown

**Narrative Text Box**:
> "Shoppers in the 'Fresh Fruits' aisle should be recommended items from 'Yogurt' (lift=2.3)"

---

### Page 4: Department-Level Insights

**Purpose**: Strategic view for category managers

**Visuals**:
1. **Clustered Column Chart**: Avg basket size by department
   - X-axis: `dept_crosssell[department]`
   - Y-axis: `AVG(dept_crosssell[avg_basket_size])`
2. **Table**: Department cross-sell summary
   - Columns: `department_from`, `department_to`, `top_products`, `avg_lift`
   - Sort: Descending by avg_lift
3. **Slicer**: Department filter
   - Field: `dept_crosssell[department_from]`
   - Type: Dropdown

---

### Page 5: Recommendation Examples & Model Performance

**Purpose**: Show concrete examples and validate model quality

**Visuals**:
1. **Table**: Example baskets + recommendations
   - Columns: `basket_items`, `recommended_items`, `rule_used`, `confidence`
   - Top N: 20
2. **Gauge**: Hit-Rate@5 vs. target
   - Value: `evaluation_summary[hit_rate_at_5]`
   - Target: 0.15 (15%)
   - Max: 1.0
3. **Gauge**: Hit-Rate@10 vs. target
   - Value: `evaluation_summary[hit_rate_at_10]`
   - Target: 0.25 (25%)
   - Max: 1.0
4. **Clustered Bar Chart**: Model vs. baseline
   - Categories: "Rule-Based Model", "Popularity Baseline"
   - Values: `hit_rate_at_5` for each

---

### Page 2-5: Additional Report Pages

Follow the same pattern to create the remaining pages:
- **Page 2**: Product Affinity Analysis (table, scatter plot, slicer)
- **Page 3**: Cross-Sell by Aisle (bar chart, table, slicer)
- **Page 4**: Department Insights (column chart, table, slicer)
- **Page 5**: Model Performance (table, gauges, bar chart)

See the original sections below for detailed visual specifications.

---

## 5. Design Guidelines

### Color Palette

Use Instacart brand colors:
- Primary: `#43B02A` (green)
- Secondary: `#FFFFFF` (white)
- Accent: `#333333` (dark gray)

**To apply in Power BI Desktop**:
1. Click **View** tab → **Themes** dropdown
2. Select a built-in theme (e.g., "Executive")
3. Or create custom theme: View → Themes → Customize current theme
4. For individual visuals: Select visual → Format pane → Colors

### Fonts

- **Headers**: Segoe UI Bold, 16pt
- **Body**: Segoe UI, 11pt
- **Cards**: Segoe UI Semibold, 24pt

### Layout

- Use consistent spacing (20px margins)
- Align visuals to grid
- Group related visuals with containers

---

## 6. Interactivity

### Cross-Filtering

Enable cross-filtering between visuals:
1. Select visual
2. **Format** → **Edit interactions**
3. Set other visuals to **Filter** (not Highlight)

### Tooltips

Add custom tooltips:
1. Create new page (name it "Tooltip")
2. Add detailed visuals
3. Set page size to **Tooltip**
4. Reference in other visuals: **Format** → **Tooltip** → **Report page**

### Bookmarks

Create bookmarks for key insights:
1. **View** → **Bookmarks**
2. Set up view (filters, selections)
3. Click **Add** bookmark
4. Name it (e.g., "Top 5 Cross-Sell Opportunities")

---

## 7. Save Report Locally

### Save .pbix File

1. Click **File** → **Save As**
2. Choose location:
   - **Option 1**: Save to shared folder (accessible from macOS)
   - **Option 2**: Save to Windows VM, then copy to Mac
3. Filename: `instacart_recommendations_dashboard.pbix`
4. Click **Save**

**No sign-in required**: You can save and work with .pbix files locally without signing into Power BI.

### Copy .pbix to macOS (Optional)

**Parallels**:
- .pbix saved in shared folder is automatically accessible on Mac

**VMware**:
- Copy .pbix to shared folder
- Access from Mac at the shared folder location

---

## 8. Data Refresh Workflow

### Refresh Data After Pipeline Re-run

When you re-run the pipeline and want to update the report:

1. **On macOS**: Re-run the export script
   ```bash
   python scripts/export_powerbi_bundle.py
   ```

2. **In Windows VM**: Open the .pbix file in Power BI Desktop
   
3. **Refresh data**: Click **Home** → **Refresh**
   - Power BI will reload all CSV files from the shared folder
   - All visuals will update automatically

4. **Save**: Click **File** → **Save**

**Note**: Since CSV files are in a shared folder, Power BI Desktop can access them directly. No need to re-import.

---

## 9. Troubleshooting

### Cannot Access Shared Folder in VM

**Issue**: Power BI Desktop can't see the shared folder

**Solution (Parallels)**:
- Ensure Parallels Tools are installed in Windows VM
- VM → Configure → Options → Shared Folders → Enable
- Restart Windows VM

**Solution (VMware)**:
- Ensure VMware Tools are installed
- Virtual Machine → Settings → Sharing → Enable folder sharing
- Restart Windows VM

### CSV Files Not Loading

**Issue**: "File not found" or access denied

**Solution**:
- Verify files exist: `ls -lh exports/powerbi/*.csv` (on Mac)
- Check file permissions: `chmod 644 exports/powerbi/*.csv` (on Mac)
- Use full UNC path in Power BI: `\\Mac\Home\...` or `\\vmware-host\...`

### Relationships Not Working

**Issue**: Visuals show incorrect data or no data

**Solution**: 
- Go to **Model view** in the dataset
- Verify relationships are active (solid line, not dotted)
- Check cardinality settings (use Many-to-Many for most relationships)
- Ensure column names match exactly (case-sensitive)

### Visuals Showing Errors

**Issue**: "Cannot display visual" or blank visuals

**Solution**: 
- Check data types in the dataset (numeric fields should be numbers, not text)
- Verify the table/column exists in the dataset
- Check for null values that might cause issues
- Use the **Data** view to inspect the data

### Data Not Refreshing

**Issue**: Clicked Refresh but data looks stale

**Solution**:
- Verify CSV files were regenerated: `ls -lt exports/powerbi/*.csv` (check timestamps)
- Close and reopen the .pbix file
- Try **Home** → **Transform data** → **Refresh Preview**
- If still stale, remove and re-add the data source

---

## 10. Data Dictionary

See `exports/powerbi/data_dictionary.md` for detailed schema documentation.

---

## 11. Example Insights

### Insight 1: Organic Products Cluster
"Customers who buy organic bananas are 2.5x more likely to buy organic avocados"

### Insight 2: Dairy-Produce Affinity
"Dairy department has strong cross-sell with Produce (lift=1.8)"

### Insight 3: Model Performance
"Rule-based model achieves 18% hit-rate@5, outperforming baseline by 6 percentage points"

---

## 12. macOS + Windows VM Setup

### Why This Approach?

- **PySpark on macOS**: Run data pipeline natively (faster, no VM overhead)
- **Power BI Desktop in VM**: Only use VM for visualization (Power BI is Windows-only)
- **Shared folder**: Seamless data transfer between macOS and Windows
- **No cloud required**: Everything runs locally, no sign-in needed

### VM Performance Tips

1. **Allocate enough resources**:
   - RAM: 4GB minimum, 8GB recommended
   - CPU: 2 cores minimum, 4 cores recommended
   - Disk: 40GB for Windows + Power BI Desktop

2. **Optimize VM settings**:
   - Parallels: Performance → Optimize for "Productivity"
   - VMware: Settings → Processors & Memory → Adjust allocation

3. **Keep VM lean**:
   - Only install Power BI Desktop (no other software)
   - Disable Windows updates during work sessions
   - Use Windows 10/11 Home (lighter than Pro)

### Alternative: Remote Desktop

If you have access to a Windows machine (work computer, friend's PC):
1. Install Power BI Desktop on that machine
2. Use Remote Desktop (Microsoft Remote Desktop app for Mac)
3. Copy CSV files to the remote machine
4. Build report remotely, copy .pbix back to Mac

---

## Need Help?

**Documentation**:
- `docs/data_dictionary.md` - Schema details
- `docs/methodology.md` - Model explanation
- `exports/powerbi/data_dictionary.md` - Export schemas

**External Resources**:
- Power BI Desktop docs: https://docs.microsoft.com/power-bi/fundamentals/desktop-getting-started
- Power BI Community: https://community.powerbi.com
- DAX reference: https://dax.guide
- Parallels Desktop: https://www.parallels.com/products/desktop/
- VMware Fusion: https://www.vmware.com/products/fusion.html

**Troubleshooting**:
- Check `exports/powerbi/data_dictionary.md` for table schemas and relationships
- Verify files exist: `ls -lh exports/powerbi/*.csv`
- Test CSV files: `head -n 5 exports/powerbi/product_affinity.csv`
- VM shared folder issues: Check Parallels/VMware Tools installation
