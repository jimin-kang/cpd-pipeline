import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv
import os
from prefect import task

@task(retries=3, retry_delay_seconds=[10, 10, 10]) # retry API request in case of failure
def extract_data():
    '''
    Extract incident data reported to the Cambridge Police Department using the Socrata Open Data API.
    Return the incident data as a Pandas DataFrame.
    '''
    # fetch Socrata app token from .env
    # include this app token when interacting with the Socrata API to avoid request throttling, so we can fetch all the incidents
    load_dotenv()
    APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN") 

    # create Socrata client to interact with the Socrata API (https://github.com/afeld/sodapy)
    client = Socrata(
        "data.cambridgema.gov", 
        APP_TOKEN, 
        timeout=30 # increase timeout from the default - sometimes, it takes longer to fetch all the results
    )

    # fetch all data, paginating over results
    DATASET_ID = "3gki-wyrb" # unique identifier for Cambridge Police Log data (https://data.cambridgema.gov/Public-Safety/Daily-Police-Log/3gki-wyrb/about_data)
    results = client.get_all(DATASET_ID)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    return results_df
