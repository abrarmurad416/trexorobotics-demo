-- Trexo Robotics Data Warehouse Schema
-- Demonstrates: Relational data modeling, proper normalization, and data warehouse design

-- Dimension Tables
CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(50) PRIMARY KEY,
    anonymized_id VARCHAR(50) UNIQUE NOT NULL, -- For PII protection
    age_at_enrollment INTEGER,
    gender VARCHAR(10),
    diagnosis_category VARCHAR(100),
    enrollment_date DATE,
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS devices (
    device_id VARCHAR(50) PRIMARY KEY,
    device_serial_number VARCHAR(100) UNIQUE NOT NULL,
    device_model VARCHAR(50),
    firmware_version VARCHAR(20),
    manufacturing_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS healthcare_facilities (
    facility_id VARCHAR(50) PRIMARY KEY,
    facility_name VARCHAR(200),
    facility_type VARCHAR(50), -- hospital, clinic, home
    city VARCHAR(100),
    state_province VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clinical_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    device_id VARCHAR(50) REFERENCES devices(device_id),
    facility_id VARCHAR(50) REFERENCES healthcare_facilities(facility_id),
    therapist_id VARCHAR(50), -- Anonymized
    session_date DATE NOT NULL,
    session_type VARCHAR(50), -- training, therapy, assessment
    duration_minutes INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fact Tables (Star Schema Design)
CREATE TABLE IF NOT EXISTS device_usage_facts (
    fact_id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(50) REFERENCES clinical_sessions(session_id),
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    device_id VARCHAR(50) REFERENCES devices(device_id),
    facility_id VARCHAR(50) REFERENCES healthcare_facilities(facility_id),
    usage_date DATE NOT NULL,
    total_steps INTEGER,
    distance_meters DECIMAL(10, 2),
    active_time_minutes INTEGER,
    average_speed_kmh DECIMAL(5, 2),
    max_speed_kmh DECIMAL(5, 2),
    battery_usage_percent DECIMAL(5, 2),
    error_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patient_outcomes_facts (
    outcome_id BIGSERIAL PRIMARY KEY,
    patient_id VARCHAR(50) REFERENCES patients(patient_id),
    assessment_date DATE NOT NULL,
    facility_id VARCHAR(50) REFERENCES healthcare_facilities(facility_id),
    gmfcs_level INTEGER, -- Gross Motor Function Classification System
    walking_independence_score DECIMAL(5, 2), -- 0-100 scale
    mobility_score DECIMAL(5, 2), -- 0-100 scale
    quality_of_life_score DECIMAL(5, 2), -- 0-100 scale
    steps_per_day_avg INTEGER,
    assessment_type VARCHAR(50), -- baseline, followup, final
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for query optimization
CREATE INDEX idx_device_usage_date ON device_usage_facts(usage_date);
CREATE INDEX idx_device_usage_patient ON device_usage_facts(patient_id);
CREATE INDEX idx_device_usage_device ON device_usage_facts(device_id);
CREATE INDEX idx_outcomes_patient ON patient_outcomes_facts(patient_id);
CREATE INDEX idx_outcomes_date ON patient_outcomes_facts(assessment_date);
CREATE INDEX idx_sessions_date ON clinical_sessions(session_date);

