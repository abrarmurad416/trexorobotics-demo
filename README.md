# Trexo Robotics Data Analytics Platform

A comprehensive data analytics solution demonstrating advanced SQL, data warehousing, ETL pipelines, and dashboard capabilities for healthcare robotics data.

## 🎯 Project Overview

This platform showcases production-ready data analytics skills required for a Data Analyst Intern role at Trexo Robotics. It includes:

- **Data Warehouse Schema Design** - Star schema with proper normalization
- **Advanced SQL Queries** - CTEs, window functions, complex joins
- **ETL Pipeline** - Python-based data processing with pandas
- **RESTful API** - Secure data access endpoints
- **Interactive Dashboard** - Real-time analytics visualization
- **PII/PHI Protection** - Data anonymization and privacy controls

## 🏗️ Architecture

```
trexo-robotics/
├── database/
│   ├── schema.sql              # Data warehouse schema
│   └── advanced_queries.sql    # Complex analytical queries
├── etl/
│   └── data_pipeline.py        # ETL pipeline with validation
├── api/
│   └── data_api.py            # RESTful API endpoints
├── dashboard/
│   └── index.html             # Interactive dashboard
├── scripts/
│   └── generate_sample_data.py # Sample data generator
└── data/
    ├── raw/                    # Raw data files
    └── processed/              # Processed data output
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python scripts/generate_sample_data.py
```

This creates sample CSV and JSON files in `data/raw/`:
- `patients_raw.csv` - Patient demographic data
- `device_usage_raw.csv` - Device usage metrics
- `patient_outcomes_raw.json` - Patient outcome assessments

### 3. Run ETL Pipeline

```bash
python etl/data_pipeline.py
```

This processes raw data, validates it, anonymizes PII, and outputs cleaned data to `data/processed/`.

### 4. Start API Server

```bash
python api/data_api.py
```

The API will be available at `http://localhost:5000`

### 5. Open Dashboard

Open `dashboard/index.html` in a web browser or serve it with a local server:

```bash
# Using Python
python -m http.server 8000

# Then navigate to http://localhost:8000/dashboard/
```

## 📊 Features Demonstrated

### SQL & Data Modeling
- **Star Schema Design**: Fact and dimension tables for efficient analytics
- **Advanced SQL**: CTEs, window functions (LAG, ROW_NUMBER, PARTITION BY), complex joins
- **Query Optimization**: Proper indexing strategies
- **Time Series Analysis**: Cohort analysis, moving averages, trend detection

### Data Warehousing
- **Schema Design**: Normalized relational model suitable for Redshift/BigQuery/Snowflake
- **ETL Processes**: Extract, transform, load with data validation
- **Data Quality**: Automated validation and quality scoring

### Python Data Processing
- **Pandas**: Data manipulation, transformations, aggregations
- **CLI Tools**: Command-line data processing scripts
- **Data Validation**: Automated quality checks and error handling

### API Development
- **RESTful Design**: Clean endpoint structure
- **Security**: API key authentication
- **Data Access**: Secure, controlled data retrieval

### Dashboard & Visualization
- **Interactive Charts**: Real-time data visualization using Chart.js
- **Key Metrics**: Device usage, patient outcomes, facility performance
- **Responsive Design**: Modern, professional UI

### Privacy & Security
- **PII/PHI Anonymization**: SHA-256 hashing for patient IDs
- **Data Protection**: Removal of direct identifiers
- **Security SOPs**: API authentication, access controls

## 📈 Key Metrics Tracked

1. **Device Usage**
   - Total steps, distance, active time
   - Device reliability and error rates
   - Battery usage patterns

2. **Patient Outcomes**
   - Walking independence scores
   - Mobility improvements
   - Quality of life metrics
   - GMFCS level tracking

3. **Facility Performance**
   - Patient success rates
   - Average outcomes per facility
   - Session utilization

4. **Cohort Analysis**
   - Patient progress over time
   - Enrollment cohort tracking
   - Improvement trends

## 🔒 Privacy & Security

- **Anonymization**: Patient IDs are hashed using SHA-256
- **PII Removal**: Direct identifiers (names, emails, addresses) are stripped
- **Access Control**: API endpoints require authentication
- **Data Validation**: Input validation prevents data quality issues

## 📝 SQL Query Examples

The `database/advanced_queries.sql` file includes:

1. **Patient Progress Analysis** - Window functions to track improvement over time
2. **Device Performance** - Multi-CTE queries for reliability analysis
3. **Cohort Analysis** - Time-based patient cohort tracking
4. **Facility Comparison** - Complex joins across multiple tables
5. **Usage Trends** - Time series analysis with moving averages

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask
- **Data Processing**: Pandas, NumPy
- **Database**: SQL (compatible with Redshift, BigQuery, Snowflake)
- **Frontend**: HTML5, JavaScript, Chart.js
- **Data Formats**: CSV, JSON
- **Version Control**: Git-ready structure

## 📋 API Endpoints

- `GET /api/health` - Health check
- `GET /api/device-usage` - Device usage statistics
- `GET /api/patient-outcomes` - Patient outcome metrics
- `GET /api/facility-performance` - Facility performance data
- `GET /api/device-reliability` - Device reliability metrics
- `GET /api/dashboard-summary` - Comprehensive dashboard data

All endpoints require API key authentication via `X-API-Key` header or `api_key` query parameter.

## 🎓 Skills Demonstrated

✅ SQL proficiency (joins, window functions, CTEs)  
✅ Relational data modeling  
✅ Data warehouse design and ETL  
✅ Python for data work (pandas, CLI tools)  
✅ Dashboard building  
✅ CSV/JSON handling  
✅ API development  
✅ Git/GitHub ready structure  
✅ PII/PHI handling and privacy awareness  
✅ Strong documentation and communication  

## 🔮 Future Enhancements

- Integration with actual data warehouse (Redshift/BigQuery/Snowflake)
- Real-time data streaming
- Advanced machine learning models for outcome prediction
- Automated report generation
- Multi-user authentication and role-based access

## 📞 Contact

This project demonstrates the technical skills required for the Data Analyst Intern position at Trexo Robotics, showcasing the ability to translate stakeholder questions into precise data requirements and deliver actionable insights.

---

**Built with ❤️ for Trexo Robotics - Enabling people to walk**


