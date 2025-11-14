# 🚀 START HERE - Quick Run Guide

## The Simplest Way to Run Everything

### 1️⃣ Install Packages (One Time)
```bash
pip install flask flask-cors pandas numpy
```

### 2️⃣ Generate Data
```bash
python scripts/generate_sample_data.py
```

### 3️⃣ Process Data (ETL)
```bash
python etl/data_pipeline.py
```

### 4️⃣ Start API (Keep This Running)
Open a **NEW terminal window** and run:
```bash
python api/data_api.py
```
**Don't close this window!** Leave it running.

### 5️⃣ Open Dashboard
- Find the file: `dashboard/index.html`
- Right-click it → "Open with" → Choose your web browser
- The dashboard will load automatically

---

## That's It! 🎉

You should now see:
- ✅ Sample data in `data/raw/` folder
- ✅ Processed data in `data/processed/` folder  
- ✅ API running at http://localhost:5000
- ✅ Dashboard showing charts and metrics

---

## Need More Help?

See `HOW_TO_RUN.md` for detailed instructions and troubleshooting.

## For Your Interview

1. **Show the SQL:** Open `database/advanced_queries.sql`
2. **Show the ETL:** Run `python etl/data_pipeline.py`
3. **Show the Dashboard:** Open `dashboard/index.html`
4. **Show the API:** Point to the running API server

Good luck! 🍀

