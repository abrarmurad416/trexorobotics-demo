"""
Trexo Robotics Data API
Demonstrates: RESTful API design, data access patterns, and security considerations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard integration

# In production, use proper authentication
API_KEYS = {
    'demo_key_123': 'readonly',
    'admin_key_456': 'admin'
}


def require_api_key(f):
    """Decorator for API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key or api_key not in API_KEYS:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


class DataWarehouse:
    """Simulated data warehouse interface"""
    
    def __init__(self):
        # In production, this would connect to Redshift/BigQuery/Snowflake
        self.data_cache = {}
    
    def get_device_usage_stats(self, start_date=None, end_date=None, device_id=None):
        """Get device usage statistics"""
        # Simulated query - in production would query actual data warehouse
        return {
            'total_sessions': 1250,
            'total_steps': 450000,
            'total_distance_km': 320.5,
            'active_devices': 45,
            'active_patients': 120,
            'avg_session_duration_minutes': 35,
            'date_range': {
                'start': start_date or (datetime.now() - timedelta(days=30)).isoformat(),
                'end': end_date or datetime.now().isoformat()
            }
        }
    
    def get_patient_outcomes(self, patient_id=None, facility_id=None):
        """Get patient outcome metrics"""
        return {
            'total_patients': 150,
            'avg_walking_improvement': 25.5,
            'avg_mobility_improvement': 18.3,
            'high_independence_count': 45,
            'improvement_rate': 0.75
        }
    
    def get_facility_performance(self, facility_id=None):
        """Get facility performance metrics"""
        return {
            'facilities': [
                {
                    'facility_id': 'FAC001',
                    'facility_name': 'Children\'s Hospital',
                    'total_patients': 45,
                    'avg_walking_score': 68.5,
                    'success_rate': 0.82
                },
                {
                    'facility_id': 'FAC002',
                    'facility_name': 'Rehabilitation Center',
                    'total_patients': 32,
                    'avg_walking_score': 72.3,
                    'success_rate': 0.88
                }
            ]
        }
    
    def get_device_reliability(self):
        """Get device reliability metrics"""
        return {
            'total_devices': 50,
            'active_devices': 45,
            'avg_error_rate': 0.02,
            'devices_needing_attention': 2,
            'reliability_score': 0.98
        }


# Initialize data warehouse
dw = DataWarehouse()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Trexo Robotics Data API'
    })


@app.route('/api/device-usage', methods=['GET'])
@require_api_key
def get_device_usage():
    """Get device usage statistics"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        device_id = request.args.get('device_id')
        
        stats = dw.get_device_usage_stats(
            start_date=start_date,
            end_date=end_date,
            device_id=device_id
        )
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error fetching device usage: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/patient-outcomes', methods=['GET'])
@require_api_key
def get_patient_outcomes():
    """Get patient outcome metrics"""
    try:
        patient_id = request.args.get('patient_id')
        facility_id = request.args.get('facility_id')
        
        outcomes = dw.get_patient_outcomes(
            patient_id=patient_id,
            facility_id=facility_id
        )
        
        return jsonify({
            'success': True,
            'data': outcomes
        })
    except Exception as e:
        logger.error(f"Error fetching patient outcomes: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/facility-performance', methods=['GET'])
@require_api_key
def get_facility_performance():
    """Get facility performance metrics"""
    try:
        facility_id = request.args.get('facility_id')
        
        performance = dw.get_facility_performance(facility_id=facility_id)
        
        return jsonify({
            'success': True,
            'data': performance
        })
    except Exception as e:
        logger.error(f"Error fetching facility performance: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/device-reliability', methods=['GET'])
@require_api_key
def get_device_reliability():
    """Get device reliability metrics"""
    try:
        reliability = dw.get_device_reliability()
        
        return jsonify({
            'success': True,
            'data': reliability
        })
    except Exception as e:
        logger.error(f"Error fetching device reliability: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/dashboard-summary', methods=['GET'])
@require_api_key
def get_dashboard_summary():
    """Get comprehensive dashboard summary"""
    try:
        device_usage = dw.get_device_usage_stats()
        patient_outcomes = dw.get_patient_outcomes()
        device_reliability = dw.get_device_reliability()
        
        summary = {
            'device_usage': device_usage,
            'patient_outcomes': patient_outcomes,
            'device_reliability': device_reliability,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

