"""
Generate Sample Data for Trexo Robotics
Creates realistic sample datasets for demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path
import random

# Create data directory
data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate sample patient data
def generate_patients(n=150):
    diagnoses = ['Cerebral Palsy', 'Spina Bifida', 'Muscular Dystrophy', 'Spinal Cord Injury']
    genders = ['Male', 'Female', 'Other']
    regions = ['North America', 'Europe', 'Asia']
    
    patients = []
    for i in range(1, n + 1):
        enrollment_date = datetime.now() - timedelta(days=random.randint(30, 365))
        patients.append({
            'patient_id': f'PAT{str(i).zfill(4)}',
            'age_at_enrollment': random.randint(3, 18),
            'gender': random.choice(genders),
            'diagnosis_category': random.choice(diagnoses),
            'enrollment_date': enrollment_date.strftime('%Y-%m-%d'),
            'region': random.choice(regions)
        })
    
    return pd.DataFrame(patients)

# Generate device usage data
def generate_device_usage(n=2000):
    device_ids = [f'DEV{str(i).zfill(3)}' for i in range(1, 51)]
    patient_ids = [f'PAT{str(i).zfill(4)}' for i in range(1, 151)]
    
    usage_data = []
    for i in range(n):
        usage_date = datetime.now() - timedelta(days=random.randint(0, 180))
        steps = random.randint(100, 5000)
        distance = steps * 0.6  # Average step length in meters
        active_time = random.randint(15, 60)
        
        usage_data.append({
            'session_id': f'SESS{str(i+1).zfill(5)}',
            'patient_id': random.choice(patient_ids),
            'device_id': random.choice(device_ids),
            'usage_date': usage_date.strftime('%Y-%m-%d'),
            'total_steps': steps,
            'distance_meters': round(distance, 2),
            'active_time_minutes': active_time,
            'average_speed_kmh': round((distance / 1000) / (active_time / 60), 2),
            'max_speed_kmh': round((distance / 1000) / (active_time / 60) * 1.5, 2),
            'battery_usage_percent': round(random.uniform(5, 25), 2),
            'error_count': random.choices([0, 0, 0, 1, 2], weights=[70, 15, 10, 4, 1])[0]
        })
    
    return pd.DataFrame(usage_data)

# Generate patient outcomes data
def generate_patient_outcomes(n=300):
    patient_ids = [f'PAT{str(i).zfill(4)}' for i in range(1, 151)]
    assessment_types = ['baseline', 'followup', 'final']
    facilities = [f'FAC{str(i).zfill(3)}' for i in range(1, 21)]
    
    outcomes = []
    for i in range(n):
        patient_id = random.choice(patient_ids)
        assessment_type = random.choice(assessment_types)
        
        # Baseline scores are typically lower
        if assessment_type == 'baseline':
            walking_score = random.uniform(20, 50)
            mobility_score = random.uniform(25, 55)
        else:
            walking_score = random.uniform(40, 85)
            mobility_score = random.uniform(45, 90)
        
        assessment_date = datetime.now() - timedelta(days=random.randint(0, 365))
        
        outcomes.append({
            'patient_id': patient_id,
            'assessment_date': assessment_date.strftime('%Y-%m-%d'),
            'facility_id': random.choice(facilities),
            'gmfcs_level': random.randint(1, 5),
            'walking_independence_score': round(walking_score, 2),
            'mobility_score': round(mobility_score, 2),
            'quality_of_life_score': round(random.uniform(50, 95), 2),
            'steps_per_day_avg': random.randint(500, 3000),
            'assessment_type': assessment_type
        })
    
    return pd.DataFrame(outcomes)

# Generate data
print("Generating sample data...")

patients_df = generate_patients(150)
patients_df.to_csv(data_dir / "patients_raw.csv", index=False)
print(f"Generated {len(patients_df)} patient records")

device_usage_df = generate_device_usage(2000)
device_usage_df.to_csv(data_dir / "device_usage_raw.csv", index=False)
print(f"Generated {len(device_usage_df)} device usage records")

patient_outcomes_df = generate_patient_outcomes(300)
patient_outcomes_df.to_json(data_dir / "patient_outcomes_raw.json", orient='records', indent=2)
print(f"Generated {len(patient_outcomes_df)} patient outcome records")

print("\nSample data generation complete!")
print(f"Data files saved to: {data_dir}")


