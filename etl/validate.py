from datetime import datetime
from collections import Counter
import pandas as pd
from prefect import task

### UTILITIES
def check_valid_schema(df):
    '''
    Check whether the DataFrame content contains the expected columns for the Cambridge Police dataset. 
    Otherwise, raise an error.
    '''
    SCHEMA_COLS = ['date_time', 'id', 'type', 'subtype', 'location', 'last_updated', 'description']
    if Counter(df.columns) != Counter(SCHEMA_COLS):
        raise ValueError("Schema does not match with the expected schema.")
    
def check_numeric_id(df):
    '''
    Convert 'id' values to numeric.
    If any 'id' values are non-numeric, replace them with NaN, so they can be removed downstream in the data transformations.
    '''
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    return df

def verify_datetime(df):
    '''
    Verify 'date_time' values follow ISO 8601 format (https://www.iso.org/iso-8601-date-and-time-format.html).
    Raise a ValueError if any of the 'date_time' values are invalid.
    '''
    df.apply(lambda row: datetime.fromisoformat(row['date_time']), axis=1) 
    
def check_missing_values(df):
    '''
    Check whether there are any missing values in columns that require data.
    For police logs, each incident should have a datetime, ID, incident type, and location.
    '''
    REQUIRED_COLS = ['date_time', 'id', 'type', 'location']
    for col in REQUIRED_COLS:
        if df[col].isnull().sum() > 0:
            raise ValueError(f"Missing values are present in the '{col}' attribute.")

### VALIDATION LOGIC
@task
def validate_data(df):
    """
    Check the data satisfies the following data quality checks:
    - schema is valid
    - IDs are numeric
    - datetime follows ISO 8601 format
    - no missing values in columns that require data

    TODO: Use Great Expectations (https://greatexpectations.io/) or similar alternative?
    """
    check_valid_schema(df)

    df = check_numeric_id(df)

    verify_datetime(df)
    
    check_missing_values(df)
        
    return df