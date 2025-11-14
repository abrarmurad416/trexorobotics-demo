# How to Run the Trexo Robotics Data Analytics Platform

## 🚀 Quick Start (3 Simple Steps)

### Step 1: Install Python Packages
Open your terminal/command prompt and run:
```bash
pip install flask flask-cors pandas numpy
```

### Step 2: Generate Sample Data
```bash
python scripts/generate_sample_data.py
```
This creates sample data files in `data/raw/` folder.

### Step 3: Run the ETL Pipeline
```bash
python etl/data_pipeline.py
```
This processes the data and saves cleaned files to `data/processed/`.

---

## 🎯 Running Individual Components

### Option A: Run Everything with One Command
```bash
python run_demo.py
```

### Option B: Run Components Separately

#### 1. Generate Sample Data
```bash
python scripts/generate_sample_data.py
```
**What it does:** Creates 3 sample data files:
- `data/raw/patients_raw.csv` (150 patients)
- `data/raw/device_usage_raw.csv` (2000 usage records)
- `data/raw/patient_outcomes_raw.json` (300 outcome records)

#### 2. Run ETL Pipeline
```bash
python etl/data_pipeline.py
```
**What it does:** 
- Reads raw data files
- Validates and cleans the data
- Anonymizes patient information
- Saves processed data to `data/processed/`

#### 3. Start the API Server
Open a **new terminal window** and run:
```bash
python api/data_api.py
```
**What it does:** Starts a web server at `http://localhost:5000`

**Keep this terminal open!** The API needs to keep running.

#### 4. Open the Dashboard
1. Open `dashboard/index.html` in your web browser
   - **Windows:** Right-click the file → "Open with" → Choose your browser
   - Or double-click if HTML files open in your browser by default

2. The dashboard will try to connect to the API automatically

---

## 🔧 Using the CLI Tool

Analyze data from the command line:

```bash
# Analyze device usage
python scripts/data_cli.py device-usage data/raw/device_usage_raw.csv

# Analyze patient outcomes
python scripts/data_cli.py patient-outcomes data/raw/patient_outcomes_raw.json

# Generate a summary report
python scripts/data_cli.py summary data/raw/device_usage_raw.csv data/raw/patient_outcomes_raw.json -o report.json
```

---

## 📊 Viewing SQL Queries

The SQL queries are in `database/advanced_queries.sql`. You can:
- Open it in any text editor
- Copy queries to run in your SQL database (Redshift, BigQuery, Snowflake)
- Review the comments to understand each query

---

## 🐛 Troubleshooting

### Problem: "Module not found" error
**Solution:** Install missing packages:
```bash
pip install flask flask-cors pandas numpy
```

### Problem: ETL pipeline shows date errors
**Solution:** This should be fixed now. If you still see errors, make sure you're using the latest version of the code.

### Problem: Dashboard shows "API Offline"
**Solution:** 
1. Make sure the API server is running (`python api/data_api.py`)
2. Check that it's running on port 5000
3. Try refreshing the dashboard page

### Problem: "File not found" errors
**Solution:** Make sure you've run the sample data generator first:
```bash
python scripts/generate_sample_data.py
```

### Problem: Port 5000 already in use
**Solution:** Change the port in `api/data_api.py`:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

---

## 📁 Project Structure

```
trexo-robotics/
├── data/
│   ├── raw/              ← Sample data goes here
│   └── processed/        ← Cleaned data goes here
├── database/
│   ├── schema.sql        ← Database schema
│   └── advanced_queries.sql  ← SQL examples
├── etl/
│   └── data_pipeline.py  ← ETL script
├── api/
│   └── data_api.py      ← API server
├── dashboard/
│   └── index.html       ← Dashboard (open in browser)
└── scripts/
    ├── generate_sample_data.py  ← Creates sample data
    └── data_cli.py      ← Command-line tool
```

---

## ✅ Verification Checklist

After running everything, you should have:

- [ ] Sample data files in `data/raw/` (3 files)
- [ ] Processed data files in `data/processed/` (after running ETL)
- [ ] API server running on `http://localhost:5000`
- [ ] Dashboard showing metrics and charts

---

## 🎓 For the Interview

**What to demonstrate:**

1. **SQL Skills:** Open `database/advanced_queries.sql` and explain the queries
2. **ETL Process:** Show the ETL pipeline processing data
3. **Dashboard:** Open the dashboard and explain the visualizations
4. **CLI Tool:** Run a command to show command-line data processing
5. **Code Quality:** Show the anonymization, validation, and error handling

**Key talking points:**
- "This ETL pipeline handles PII/PHI by anonymizing patient IDs"
- "The SQL queries use window functions for cohort analysis"
- "The dashboard translates stakeholder questions into visual insights"
- "The API provides secure, controlled access to the data"

---

## 💡 Next Steps

Once everything is running:
1. Explore the SQL queries in `database/advanced_queries.sql`
2. Try modifying the dashboard to add new charts
3. Experiment with the CLI tool on different data files
4. Review the code to understand the architecture

Good luck with your interview! 🚀


