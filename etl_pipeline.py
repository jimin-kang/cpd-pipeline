from extract import extract_data
from validate import validate_data
from transform import transform_data
from load import load_into_postgres
from prefect import flow

@flow(name="cpd_incident_etl", log_prints=True)
def etl():
    '''
    Execute the ETL pipeline:
    - Extract CPD incident data from the Socrata API
    - Validate and transform the extracted data to prepare it for storage
    - Import the transformed data into Postgres 
    '''
    print("Extracting data...")
    extracted_df = extract_data()
    print("Extracted data successfully!")

    print("Performing data quality checks...")
    validated_df = validate_data(extracted_df)
    print("Data quality checks completed!")

    print("Performing data transformations...")
    transformed_df = transform_data(validated_df)
    print("Data transformations completed!")

    print("Importing data into Postgres...")
    load_into_postgres(transformed_df)
    print("Data importing complete!")

if __name__ == "__main__":
    # CPD data is expected to be updated daily (https://data.cambridgema.gov/Public-Safety/Daily-Police-Log/3gki-wyrb/about_data)
    # Thus, we'll execute our pipeline on a daily basis (at midnight)
    etl.serve(name="cpd-pipeline-deployment", cron="0 0 * * *") 