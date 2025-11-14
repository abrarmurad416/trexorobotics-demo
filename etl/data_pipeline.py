"""
Trexo Robotics ETL Pipeline
Demonstrates: Python data processing, pandas, ETL best practices, and data validation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataAnonymizer:
    """Handles PII/PHI anonymization for sensitive healthcare data"""
    
    @staticmethod
    def generate_anonymized_id(patient_id: str) -> str:
        """Generate consistent anonymized ID for patient"""
        return hashlib.sha256(patient_id.encode()).hexdigest()[:16]
    
    @staticmethod
    def anonymize_patient_data(df: pd.DataFrame) -> pd.DataFrame:
        """Remove or anonymize PII/PHI from patient data"""
        df_anon = df.copy()
        
        # Generate anonymized IDs
        if 'patient_id' in df_anon.columns:
            df_anon['anonymized_id'] = df_anon['patient_id'].apply(
                DataAnonymizer.generate_anonymized_id
            )
        
        # Remove direct identifiers
        columns_to_remove = ['patient_name', 'email', 'phone', 'address', 'ssn']
        for col in columns_to_remove:
            if col in df_anon.columns:
                df_anon = df_anon.drop(columns=[col])
        
        return df_anon


class DataValidator:
    """Validates data quality and integrity"""
    
    @staticmethod
    def validate_device_usage(df: pd.DataFrame) -> pd.DataFrame:
        """Validate device usage data"""
        logger.info(f"Validating {len(df)} device usage records")
        
        # Remove invalid records
        if 'total_steps' in df.columns:
            df = df[df['total_steps'] >= 0]
        if 'distance_meters' in df.columns:
            df = df[df['distance_meters'] >= 0]
        if 'battery_usage_percent' in df.columns:
            df = df[df['battery_usage_percent'].between(0, 100)]
        if 'active_time_minutes' in df.columns:
            df = df[df['active_time_minutes'] >= 0]
        
        # Validate date ranges (ensure date is already converted)
        if 'usage_date' in df.columns:
            max_date = datetime.now().date()
            min_date = datetime(2020, 1, 1).date()
            # Ensure usage_date is date type, not string
            if df['usage_date'].dtype == 'object':
                df['usage_date'] = pd.to_datetime(df['usage_date']).dt.date
            df = df[df['usage_date'] >= min_date]
            df = df[df['usage_date'] <= max_date]
        
        logger.info(f"After validation: {len(df)} valid records")
        return df
    
    @staticmethod
    def validate_patient_outcomes(df: pd.DataFrame) -> pd.DataFrame:
        """Validate patient outcome data"""
        logger.info(f"Validating {len(df)} patient outcome records")
        
        # Validate score ranges (0-100)
        score_columns = ['walking_independence_score', 'mobility_score', 'quality_of_life_score']
        for col in score_columns:
            if col in df.columns:
                df = df[df[col].between(0, 100)]
        
        # Validate GMFCS level (1-5)
        if 'gmfcs_level' in df.columns:
            df = df[df['gmfcs_level'].between(1, 5)]
        
        # Validate date if present
        if 'assessment_date' in df.columns:
            max_date = datetime.now().date()
            min_date = datetime(2020, 1, 1).date()
            # Ensure assessment_date is date type, not string
            if df['assessment_date'].dtype == 'object':
                df['assessment_date'] = pd.to_datetime(df['assessment_date']).dt.date
            df = df[df['assessment_date'] >= min_date]
            df = df[df['assessment_date'] <= max_date]
        
        logger.info(f"After validation: {len(df)} valid records")
        return df


class ETLPipeline:
    """Main ETL pipeline for processing Trexo Robotics data"""
    
    def __init__(self, input_dir: str = "data/raw", output_dir: str = "data/processed"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.anonymizer = DataAnonymizer()
        self.validator = DataValidator()
    
    def extract_csv(self, filename: str) -> pd.DataFrame:
        """Extract data from CSV file"""
        filepath = self.input_dir / filename
        logger.info(f"Extracting data from {filepath}")
        
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Extracted {len(df)} records from {filename}")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error extracting {filename}: {str(e)}")
            raise
    
    def extract_json(self, filename: str) -> pd.DataFrame:
        """Extract data from JSON file"""
        filepath = self.input_dir / filename
        logger.info(f"Extracting data from {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.json_normalize(data)
            
            logger.info(f"Extracted {len(df)} records from {filename}")
            return df
        except Exception as e:
            logger.error(f"Error extracting {filename}: {str(e)}")
            raise
    
    def transform_device_usage(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform device usage data"""
        logger.info("Transforming device usage data")
        
        df = df.copy()
        
        # Convert date columns
        if 'usage_date' in df.columns:
            df['usage_date'] = pd.to_datetime(df['usage_date']).dt.date
        
        # Calculate derived metrics
        if 'distance_meters' in df.columns and 'active_time_minutes' in df.columns:
            df['average_speed_kmh'] = (
                df['distance_meters'] / 1000 / (df['active_time_minutes'] / 60)
            ).fillna(0)
            df['average_speed_kmh'] = df['average_speed_kmh'].replace([np.inf, -np.inf], 0)
        
        # Add data quality flags
        df['data_quality_score'] = (
            (df['total_steps'] > 0).astype(int) * 0.3 +
            (df['distance_meters'] > 0).astype(int) * 0.3 +
            (df['battery_usage_percent'].between(0, 100)).astype(int) * 0.2 +
            (df['error_count'] == 0).astype(int) * 0.2
        )
        
        # Validate data
        df = self.validator.validate_device_usage(df)
        
        return df
    
    def transform_patient_outcomes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform patient outcome data"""
        logger.info("Transforming patient outcome data")
        
        df = df.copy()
        
        # Anonymize patient data
        df = self.anonymizer.anonymize_patient_data(df)
        
        # Convert date columns
        if 'assessment_date' in df.columns:
            df['assessment_date'] = pd.to_datetime(df['assessment_date']).dt.date
        
        # Calculate improvement metrics (if baseline exists)
        if 'baseline_walking_score' in df.columns and 'walking_independence_score' in df.columns:
            df['walking_improvement'] = (
                df['walking_independence_score'] - df['baseline_walking_score']
            )
        
        # Validate data
        df = self.validator.validate_patient_outcomes(df)
        
        return df
    
    def load_to_warehouse(self, df: pd.DataFrame, table_name: str):
        """Load transformed data to data warehouse (simulated)"""
        output_file = self.output_dir / f"{table_name}_processed.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Loaded {len(df)} records to {output_file}")
        
        # Generate summary statistics
        summary = {
            'table_name': table_name,
            'record_count': len(df),
            'columns': list(df.columns),
            'date_range': {
                'min': str(df.select_dtypes(include=['datetime64', 'object']).min().min()),
                'max': str(df.select_dtypes(include=['datetime64', 'object']).max().max())
            } if len(df) > 0 else None,
            'processed_at': datetime.now().isoformat()
        }
        
        summary_file = self.output_dir / f"{table_name}_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def run_pipeline(self, source_files: Dict[str, str]):
        """Run complete ETL pipeline"""
        logger.info("Starting ETL pipeline")
        
        results = {}
        
        for table_name, filename in source_files.items():
            try:
                # Extract
                if filename.endswith('.csv'):
                    df = self.extract_csv(filename)
                elif filename.endswith('.json'):
                    df = self.extract_json(filename)
                else:
                    logger.warning(f"Unsupported file type: {filename}")
                    continue
                
                # Transform
                if 'device_usage' in table_name:
                    df = self.transform_device_usage(df)
                elif 'patient_outcome' in table_name:
                    df = self.transform_patient_outcomes(df)
                
                # Load
                summary = self.load_to_warehouse(df, table_name)
                results[table_name] = summary
                
            except Exception as e:
                logger.error(f"Error processing {table_name}: {str(e)}")
                results[table_name] = {'error': str(e)}
        
        logger.info("ETL pipeline completed")
        return results


if __name__ == "__main__":
    # Example usage
    pipeline = ETLPipeline()
    
    source_files = {
        'device_usage': 'device_usage_raw.csv',
        'patient_outcomes': 'patient_outcomes_raw.json'
    }
    
    try:
        results = pipeline.run_pipeline(source_files)
        print("\n" + "="*50)
        print("ETL Pipeline Results")
        print("="*50)
        print(json.dumps(results, indent=2))
        print("="*50)
        
        # Check for errors
        has_errors = any('error' in str(v) for v in results.values())
        if has_errors:
            print("\n⚠ Some files had errors. Check the logs above for details.")
        else:
            print("\n✓ ETL pipeline completed successfully!")
            print(f"Processed data saved to: {pipeline.output_dir}")
    except Exception as e:
        print(f"\n❌ ETL Pipeline Error: {str(e)}")
        print("Make sure you've generated sample data first:")
        print("  python scripts/generate_sample_data.py")

