#!/usr/bin/env python3
"""
Trexo Robotics Data CLI Tool
Demonstrates: Command-line data processing, CSV/JSON handling, and data analysis
"""

import argparse
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys


def analyze_device_usage(csv_path, output_format='table'):
    """Analyze device usage data from CSV"""
    print(f"📊 Analyzing device usage data from {csv_path}...")
    
    try:
        df = pd.read_csv(csv_path)
        
        # Basic statistics
        stats = {
            'total_records': len(df),
            'date_range': {
                'start': df['usage_date'].min() if 'usage_date' in df.columns else 'N/A',
                'end': df['usage_date'].max() if 'usage_date' in df.columns else 'N/A'
            },
            'total_steps': int(df['total_steps'].sum()) if 'total_steps' in df.columns else 0,
            'total_distance_km': round(df['distance_meters'].sum() / 1000, 2) if 'distance_meters' in df.columns else 0,
            'unique_devices': df['device_id'].nunique() if 'device_id' in df.columns else 0,
            'unique_patients': df['patient_id'].nunique() if 'patient_id' in df.columns else 0,
            'avg_steps_per_session': int(df['total_steps'].mean()) if 'total_steps' in df.columns else 0,
            'total_errors': int(df['error_count'].sum()) if 'error_count' in df.columns else 0
        }
        
        if output_format == 'json':
            print(json.dumps(stats, indent=2))
        else:
            print("\n" + "="*50)
            print("Device Usage Statistics")
            print("="*50)
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("="*50)
        
        return stats
        
    except Exception as e:
        print(f"❌ Error analyzing data: {str(e)}", file=sys.stderr)
        sys.exit(1)


def analyze_patient_outcomes(json_path, output_format='table'):
    """Analyze patient outcomes from JSON"""
    print(f"📊 Analyzing patient outcomes from {json_path}...")
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        
        stats = {
            'total_assessments': len(df),
            'unique_patients': df['patient_id'].nunique() if 'patient_id' in df.columns else 0,
            'avg_walking_score': round(df['walking_independence_score'].mean(), 2) if 'walking_independence_score' in df.columns else 0,
            'avg_mobility_score': round(df['mobility_score'].mean(), 2) if 'mobility_score' in df.columns else 0,
            'avg_quality_of_life': round(df['quality_of_life_score'].mean(), 2) if 'quality_of_life_score' in df.columns else 0,
            'high_independence_count': len(df[df['walking_independence_score'] >= 70]) if 'walking_independence_score' in df.columns else 0,
            'baseline_count': len(df[df['assessment_type'] == 'baseline']) if 'assessment_type' in df.columns else 0,
            'final_assessment_count': len(df[df['assessment_type'] == 'final']) if 'assessment_type' in df.columns else 0
        }
        
        if output_format == 'json':
            print(json.dumps(stats, indent=2))
        else:
            print("\n" + "="*50)
            print("Patient Outcomes Statistics")
            print("="*50)
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("="*50)
        
        return stats
        
    except Exception as e:
        print(f"❌ Error analyzing data: {str(e)}", file=sys.stderr)
        sys.exit(1)


def export_summary(csv_path, json_path, output_path):
    """Export combined summary report"""
    print("📝 Generating summary report...")
    
    device_stats = analyze_device_usage(csv_path, output_format='dict')
    outcome_stats = analyze_patient_outcomes(json_path, output_format='dict')
    
    summary = {
        'generated_at': datetime.now().isoformat(),
        'device_usage': device_stats,
        'patient_outcomes': outcome_stats
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Summary exported to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Trexo Robotics Data CLI - Analyze device usage and patient outcomes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/data_cli.py device-usage data/raw/device_usage_raw.csv
  python scripts/data_cli.py patient-outcomes data/raw/patient_outcomes_raw.json --format json
  python scripts/data_cli.py summary data/raw/device_usage_raw.csv data/raw/patient_outcomes_raw.json -o report.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Device usage command
    device_parser = subparsers.add_parser('device-usage', help='Analyze device usage data')
    device_parser.add_argument('csv_file', help='Path to device usage CSV file')
    device_parser.add_argument('--format', choices=['table', 'json'], default='table',
                              help='Output format (default: table)')
    
    # Patient outcomes command
    outcomes_parser = subparsers.add_parser('patient-outcomes', help='Analyze patient outcomes')
    outcomes_parser.add_argument('json_file', help='Path to patient outcomes JSON file')
    outcomes_parser.add_argument('--format', choices=['table', 'json'], default='table',
                                 help='Output format (default: table)')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Generate combined summary report')
    summary_parser.add_argument('csv_file', help='Path to device usage CSV file')
    summary_parser.add_argument('json_file', help='Path to patient outcomes JSON file')
    summary_parser.add_argument('-o', '--output', default='summary_report.json',
                                help='Output file path (default: summary_report.json)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'device-usage':
        analyze_device_usage(args.csv_file, args.format)
    elif args.command == 'patient-outcomes':
        analyze_patient_outcomes(args.json_file, args.format)
    elif args.command == 'summary':
        export_summary(args.csv_file, args.json_file, args.output)


if __name__ == '__main__':
    main()


