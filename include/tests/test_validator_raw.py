import pytest
import pandas as pd
from validator.schema import DailyEngagement
from validator.validator import EngagementValidator

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'user_id': ['user1', 'user2', ''],
        'video_id': ['video1', 'video2', 'video3'],
        'category': ['cat1', 'cat2', 'cat3'],
        'view_start_time': [None, None, None],
        'view_end_time': [None, None, None],
        'region': ['US', 'BR', 'XXL']
    })

def test_validation(sample_data):
    validator = EngagementValidator(sample_data)
    results = validator.validate()
    # Count how many times "Value error" appears in the error message
    error_count = validator.errors[0]['error'].count("Value error")
    assert len(results) == 2
    assert error_count == 2

def test_region_validation(sample_data):
    validator = EngagementValidator(sample_data)
    validator.validate()
    
    # Check that region error exists
    region_errors = [e for e in validator.errors if "Region must be 2 uppercase" in e['error']]
    assert len(region_errors) == 1
    assert region_errors[0]['row'] == 2