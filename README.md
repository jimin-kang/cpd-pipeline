# CPD Data Pipeline & Visualization
## Overview
This project consists of a data pipeline that extracts Cambridge Police Department (CPD) incident data from the Socrata Open Data Portal, and ends with visualizing this data in Metabase.

More information about the data can be found [here](https://data.cambridgema.gov/Public-Safety/Daily-Police-Log/3gki-wyrb/about_data).

The data pipeline (roughly) follows the following architecture:
* Extract from Socrata API -> Data Validation & Transformation -> Load into PostgreSQL -> Visualize in Metabase  

The goal of this project was to build a tool that can monitor crime & safety trends in Cambridge, MA. Ideally, this project can serve as a general template for other projects looking to achieve similar goals. Additionally, any projects that involve writing pipelines consisting of API extracts, simple data transformations, and visualizations using BI tools may use this code as reference.

The associated article for this project can be found [here](https://medium.com/data-engineer-things/creating-a-data-pipeline-to-monitor-local-crime-trends-e2493c20da39).

## Tooling
Development was done in python 3.12. The required dependencies are listed in *requirements.txt*. 
* For more info on recreating the dev environment, click [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-a-requirements-file).

[Prefect](https://www.prefect.io/) was used to orchestrate pipeline execution. Originally I tried to use Airflow, but I ran into difficulties trying to install my required dependencies into the Airflow environment (where the pipeline is executed), even after following the documentation [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file) and [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file). Prefect allows you to [define pipelines](https://docs.prefect.io/v3/concepts/flows) by simply adding decorators to python functions, and [deployment](https://docs.prefect.io/v3/how-to-guides/deployments/create-deployments) is really easy. For this project, I used [Prefect Cloud](https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud), which takes care of the infrastructure where your pipeline is executed.

[Pandas](https://pandas.pydata.org/docs/index.html) is used for data validation & transformation. It makes data manipulation easy, and the data that we're working with is quite small (< 10k rows). If the size of the data increases drastically, we may consider using more powerful tools (ex: [Polars](https://pola.rs/), [Spark](https://spark.apache.org/docs/latest/api/python/index.html)), but that's really not necessary right now for this data.

[PostgreSQL](https://www.postgresql.org/) is the database used to store the transformed data. I spun up a local instance of Postgres by defining it as a service in the *compose.yaml*. 

[Metabase](https://www.metabase.com/) was used as the BI tool to analyze the transformed CPD data, for the following reasons:
* Relatively simple [setup](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)
* Lots of built-in visualization/analytical capabilities without requiring code. Other tools may be needed for heavy customized visuals, but this does the job to get some basic analysis/visuals up and running quickly. 

## File Information
**Pipeline development:**
* *etl/extract.py* - extract CPD data via Socrata API
* *etl/validate.py* - data quality checks
* *etl/transform.py* - data transformations
* *etl/load.py* - load data into Postgres
* *etl_pipeline.py* - ETL pipeline that defines our workflow
* *testing.ipynb* - notebook used during development to test out individual components

**Architecture/Configuration**
* *compose.yaml* - defines/configures all the required components of our project

**Dependencies**
* *requirements.txt* - list of all python dependencies

**Diagrams**
* *metabase-dashboard.pdf* - Metabase dashboard visualizing recent & historical crime trends
* *data-flow.pdf* - diagram illustrating data flow from ETL to Metabase

**Miscellaneous**
* sample_env.txt - sample .env file required to run this project

## Running the Project
### Requirements
- python 3.x
- Docker
- Docker Desktop (if you're on Windows/MacOS)
- [Prefect Cloud account](https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud)
- [Socrata API token](https://dev.socrata.com/docs/app-tokens.html)

### How to Run the Pipeline
1. Clone the repo and recreate the dev environment from requirements.txt.
   Read [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-a-requirements-file) for more info.
2. Create your own .env file and place it in the root directory of the project. It should have values for the following variables:
   * SOCRATA_APP_TOKEN (this should be your app token for the Socrata API)
   * POSTGRES_USER
   * POSTGRES_PASSWORD
   * POSTGRES_DB=cpd_db (this should be fixed)
   * PGADMIN_DEFAULT_EMAIL
   * PGADMIN_DEFAULT_PASSWORD
   * METABASE_DB_USER
   * METABASE_DB_PASSWORD
   * METABASE_DB_NAME
   Check out sample_env.txt for an example .env file.
3. Log into Prefect Cloud by following [these instructions](https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud).
4. Start up docker, open up your terminal to the project root directory and execute the following command to start up all the services: 
   * docker compose up -d
5. Activate your virtual environment and run the pipeline. In the terminal, run the following command in the project root directory: 
   * python etl_pipeline.py
6. Go to Metabase and connect to your PostgreSQL instance.
7. Create whatever dashboards/analytical figures you want. For inspiration, check out the [docs](https://www.metabase.com/learn/metabase-basics/overview/tour-of-metabase).

## Resources  
**Prefect:**
- example pipeline: https://docs.prefect.io/v3/examples/run-api-sourced-etl
- deployment: https://docs.prefect.io/v3/how-to-guides/deployments/create-deployments

**Metabase:**
- overview: https://www.metabase.com/learn/metabase-basics/overview/tour-of-metabase
- setup: https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker
- architecture: https://www.metabase.com/learn/metabase-basics/administration/administration-and-operation/metabase-and-your-db?use_case=bi

**Docker:**
- Compose reference: https://docs.docker.com/reference/compose-file
- Volumes: https://docs.docker.com/engine/storage/volumes/

**Airflow:**
- https://towardsdatascience.com/airflow-prefect-and-dagster-an-inside-look-6074781c9b77/
- https://airflow.apache.org/docs/docker-stack/build.html
- https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/

