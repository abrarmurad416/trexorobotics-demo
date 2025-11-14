"""
Quick Start Script for Trexo Robotics Data Analytics Platform
Run this to set up and demonstrate the entire system
"""

import subprocess
import sys
import time
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr}")
        return False

def main():
    print_header("Trexo Robotics Data Analytics Platform - Demo Setup")
    
    # Check Python version
    print("Checking Python version...")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("✗ Python 3.8+ required")
        sys.exit(1)
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Install dependencies
    print_header("Installing Dependencies")
    if not run_command("pip install -r requirements.txt", "Installing packages"):
        print("⚠ Warning: Some packages may not have installed. Continuing anyway...")
    
    # Generate sample data
    print_header("Generating Sample Data")
    if not run_command("python scripts/generate_sample_data.py", "Creating sample datasets"):
        print("✗ Failed to generate sample data")
        sys.exit(1)
    
    # Run ETL pipeline
    print_header("Running ETL Pipeline")
    if not run_command("python etl/data_pipeline.py", "Processing data through ETL"):
        print("⚠ Warning: ETL pipeline had issues. Check logs for details.")
    
    print_header("Setup Complete!")
    print("\nNext steps:")
    print("1. Start the API server: python api/data_api.py")
    print("2. Open dashboard/index.html in your browser")
    print("3. Review database/advanced_queries.sql for SQL examples")
    print("\nFor full documentation, see README.md")

if __name__ == "__main__":
    main()

