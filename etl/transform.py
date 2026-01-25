import pandas as pd
from prefect import task

### UTILITIES
def remove_duplicates(df):
    '''
    Remove duplicate rows from dataframe based on 'id' column. Keep the first occurrence.
    '''
    return df.drop_duplicates(subset=["id"], keep='first')

def remove_invalid_rows(df):
    '''
    Remove rows where the 'id' is NaN, as these IDs were identified as non-numeric.
    '''
    return df.dropna(subset='id')

def split_datetime(df):
    '''
    Split the date_time column into separate year, month, day, and time columns.
    '''
    # convert to datetime
    df['date_time'] = pd.to_datetime(df['date_time'])

    # extract year/month/day/time
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month
    df['day'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['second'] = df['date_time'].dt.second

    return df

### TRANSFORMATION LOGIC
@task
def transform_data(df):
    '''
    Apply the following transformations to the passed in dataframe:
    - deduplicate records (keep the first)
    - remove invalid rows
    - split datetime into year, month, day, and time columns
    ''' 

    df = remove_duplicates(df)

    df = remove_invalid_rows(df)

    df = split_datetime(df)

    return df
