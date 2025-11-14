-- Advanced SQL Queries Demonstrating CTEs, Window Functions, and Complex Joins
-- These queries showcase analytical capabilities for Trexo Robotics data

-- Query 1: Patient Progress Analysis using Window Functions
-- Shows improvement over time for each patient
WITH patient_progress AS (
    SELECT 
        p.anonymized_id,
        p.diagnosis_category,
        pof.assessment_date,
        pof.walking_independence_score,
        pof.mobility_score,
        LAG(pof.walking_independence_score) OVER (
            PARTITION BY pof.patient_id 
            ORDER BY pof.assessment_date
        ) AS previous_walking_score,
        LAG(pof.mobility_score) OVER (
            PARTITION BY pof.patient_id 
            ORDER BY pof.assessment_date
        ) AS previous_mobility_score,
        ROW_NUMBER() OVER (
            PARTITION BY pof.patient_id 
            ORDER BY pof.assessment_date DESC
        ) AS assessment_rank
    FROM patient_outcomes_facts pof
    JOIN patients p ON pof.patient_id = p.patient_id
    WHERE pof.assessment_date >= CURRENT_DATE - INTERVAL '12 months'
)
SELECT 
    anonymized_id,
    diagnosis_category,
    assessment_date,
    walking_independence_score,
    mobility_score,
    walking_independence_score - previous_walking_score AS walking_improvement,
    mobility_score - previous_mobility_score AS mobility_improvement,
    CASE 
        WHEN walking_independence_score - previous_walking_score > 10 THEN 'Significant Improvement'
        WHEN walking_independence_score - previous_walking_score > 0 THEN 'Moderate Improvement'
        WHEN walking_independence_score - previous_walking_score = 0 THEN 'No Change'
        ELSE 'Decline'
    END AS improvement_category
FROM patient_progress
WHERE previous_walking_score IS NOT NULL
ORDER BY assessment_date DESC, walking_improvement DESC;

-- Query 2: Device Performance Analysis with Multiple CTEs
-- Analyzes device reliability and usage patterns
WITH device_usage_stats AS (
    SELECT 
        d.device_id,
        d.device_model,
        COUNT(DISTINCT duf.session_id) AS total_sessions,
        COUNT(DISTINCT duf.patient_id) AS unique_patients,
        SUM(duf.total_steps) AS total_steps,
        SUM(duf.distance_meters) AS total_distance,
        AVG(duf.battery_usage_percent) AS avg_battery_usage,
        SUM(duf.error_count) AS total_errors,
        AVG(duf.error_count) AS avg_errors_per_session
    FROM device_usage_facts duf
    JOIN devices d ON duf.device_id = d.device_id
    WHERE duf.usage_date >= CURRENT_DATE - INTERVAL '6 months'
    GROUP BY d.device_id, d.device_model
),
device_reliability AS (
    SELECT 
        device_id,
        device_model,
        total_sessions,
        unique_patients,
        total_steps,
        total_distance,
        avg_battery_usage,
        total_errors,
        avg_errors_per_session,
        CASE 
            WHEN total_errors = 0 THEN 'Excellent'
            WHEN avg_errors_per_session < 0.1 THEN 'Good'
            WHEN avg_errors_per_session < 0.5 THEN 'Fair'
            ELSE 'Needs Attention'
        END AS reliability_rating,
        RANK() OVER (ORDER BY avg_errors_per_session ASC) AS reliability_rank
    FROM device_usage_stats
)
SELECT 
    device_model,
    COUNT(*) AS device_count,
    AVG(total_sessions) AS avg_sessions_per_device,
    AVG(unique_patients) AS avg_patients_per_device,
    SUM(total_steps) AS total_steps_all_devices,
    AVG(avg_errors_per_session) AS avg_error_rate,
    COUNT(CASE WHEN reliability_rating = 'Excellent' THEN 1 END) AS excellent_devices,
    COUNT(CASE WHEN reliability_rating = 'Needs Attention' THEN 1 END) AS devices_needing_attention
FROM device_reliability
GROUP BY device_model
ORDER BY avg_error_rate ASC;

-- Query 3: Cohort Analysis - Patient Outcomes by Enrollment Cohort
-- Uses window functions to track cohorts over time
WITH enrollment_cohorts AS (
    SELECT 
        patient_id,
        DATE_TRUNC('month', enrollment_date) AS cohort_month,
        enrollment_date
    FROM patients
),
monthly_outcomes AS (
    SELECT 
        pof.patient_id,
        DATE_TRUNC('month', pof.assessment_date) AS outcome_month,
        AVG(pof.walking_independence_score) AS avg_walking_score,
        AVG(pof.mobility_score) AS avg_mobility_score
    FROM patient_outcomes_facts pof
    GROUP BY pof.patient_id, DATE_TRUNC('month', pof.assessment_date)
),
cohort_analysis AS (
    SELECT 
        ec.cohort_month,
        mo.outcome_month,
        DATE_PART('month', AGE(mo.outcome_month, ec.cohort_month)) AS months_since_enrollment,
        COUNT(DISTINCT mo.patient_id) AS active_patients,
        AVG(mo.avg_walking_score) AS cohort_avg_walking,
        AVG(mo.avg_mobility_score) AS cohort_avg_mobility,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mo.avg_walking_score) AS median_walking_score
    FROM enrollment_cohorts ec
    JOIN monthly_outcomes mo ON ec.patient_id = mo.patient_id
    WHERE mo.outcome_month >= ec.cohort_month
    GROUP BY ec.cohort_month, mo.outcome_month
)
SELECT 
    cohort_month,
    months_since_enrollment,
    active_patients,
    ROUND(cohort_avg_walking, 2) AS avg_walking_score,
    ROUND(cohort_avg_mobility, 2) AS avg_mobility_score,
    ROUND(median_walking_score, 2) AS median_walking_score,
    LAG(cohort_avg_walking) OVER (
        PARTITION BY cohort_month 
        ORDER BY months_since_enrollment
    ) AS prev_month_walking,
    cohort_avg_walking - LAG(cohort_avg_walking) OVER (
        PARTITION BY cohort_month 
        ORDER BY months_since_enrollment
    ) AS walking_improvement
FROM cohort_analysis
WHERE months_since_enrollment <= 12
ORDER BY cohort_month DESC, months_since_enrollment;

-- Query 4: Facility Performance Comparison
-- Complex joins across multiple tables with aggregations
SELECT 
    hf.facility_name,
    hf.facility_type,
    hf.city,
    hf.state_province,
    COUNT(DISTINCT cs.patient_id) AS total_patients,
    COUNT(DISTINCT cs.session_id) AS total_sessions,
    COUNT(DISTINCT cs.device_id) AS devices_used,
    AVG(cs.duration_minutes) AS avg_session_duration,
    SUM(duf.total_steps) AS total_steps,
    AVG(pof.walking_independence_score) AS avg_walking_score,
    AVG(pof.mobility_score) AS avg_mobility_score,
    COUNT(DISTINCT CASE 
        WHEN pof.walking_independence_score >= 70 THEN pof.patient_id 
    END) AS patients_high_independence,
    ROUND(
        COUNT(DISTINCT CASE 
            WHEN pof.walking_independence_score >= 70 THEN pof.patient_id 
        END)::NUMERIC / 
        NULLIF(COUNT(DISTINCT pof.patient_id), 0) * 100, 
        2
    ) AS high_independence_percentage
FROM healthcare_facilities hf
LEFT JOIN clinical_sessions cs ON hf.facility_id = cs.facility_id
LEFT JOIN device_usage_facts duf ON cs.session_id = duf.session_id
LEFT JOIN patient_outcomes_facts pof ON cs.patient_id = pof.patient_id 
    AND pof.assessment_type = 'final'
WHERE cs.session_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY hf.facility_id, hf.facility_name, hf.facility_type, hf.city, hf.state_province
HAVING COUNT(DISTINCT cs.patient_id) > 0
ORDER BY total_patients DESC, avg_walking_score DESC;

-- Query 5: Device Usage Trends with Time Series Analysis
-- Window functions for time-based analysis
SELECT 
    DATE_TRUNC('week', usage_date) AS week,
    COUNT(DISTINCT patient_id) AS active_patients,
    COUNT(DISTINCT device_id) AS active_devices,
    SUM(total_steps) AS weekly_total_steps,
    AVG(total_steps) AS avg_steps_per_session,
    SUM(distance_meters) AS weekly_total_distance,
    AVG(active_time_minutes) AS avg_active_time,
    SUM(total_steps) - LAG(SUM(total_steps)) OVER (ORDER BY DATE_TRUNC('week', usage_date)) AS steps_change,
    ROUND(
        (SUM(total_steps) - LAG(SUM(total_steps)) OVER (ORDER BY DATE_TRUNC('week', usage_date)))::NUMERIC /
        NULLIF(LAG(SUM(total_steps)) OVER (ORDER BY DATE_TRUNC('week', usage_date)), 0) * 100,
        2
    ) AS steps_change_percentage,
    AVG(SUM(total_steps)) OVER (
        ORDER BY DATE_TRUNC('week', usage_date) 
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ) AS moving_avg_4_weeks
FROM device_usage_facts
WHERE usage_date >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY DATE_TRUNC('week', usage_date)
ORDER BY week DESC;

