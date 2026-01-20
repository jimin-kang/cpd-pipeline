# CPD Data Pipeline & Visualization
## Overview
This project consists of a data pipeline that extracts Cambridge Police Department (CPD) incident data from the Socrata Open Data Portal, and ends with visualizing this data in Metabase.

More information about the data can be found [here](https://data.cambridgema.gov/Public-Safety/Daily-Police-Log/3gki-wyrb/about_data).

The data pipeline (roughly) follows the following architecture:
* Extract from Socrata API -> Data Validation & Transformation -> Load into PostgreSQL -> Visualize in Metabase  

The goal of this project was to build a tool that can monitor crime & safety trends in Cambridge, MA. Ideally, this project can serve as a general template for other projects looking to achieve similar goals. Additionally, any projects that involve writing pipelines consisting of API extracts, simple data transformations, and visualizations using BI tools may use this code as reference.

## Tooling
Development was done in python 3.12. The required dependencies are listed in *requirements.txt*. 
* For more info on recreating the dev environment from the requirements file, click [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#using-a-requirements-file).

[Prefect] was used to orchestrate & schedule pipeline execution. Originally, I tried to use Airflow for this, but I ran into lots of difficulty trying to install the dependencies my code required into the Airflow environment, even after following the documentation [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file) and [here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#special-case-adding-dependencies-via-requirements-txt-file). Prefect makes defining pipelines extremely simple with minimal setup - you can define your workflows very easily using basic python, and you don't have to worry about dependency mismatches between your local development environment and the environment where your pipeline is executed. For this project, I used [Prefect Cloud](https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud) - it takes care of the infrastructure where your pipeline is executed.

[Pandas](https://pandas.pydata.org/docs/index.html) was used for data validation and transformation, as the data that we're working with is quite small (< 10k rows). Thus, in memory data manipulation/transformation is not a huge concern. We may consider using a distributed data processing platform (ex: Apache Spark) if the dataset size increases drastically, but for now that's not really necessary. 

[PostgreSQL] is the database used to store the transformed data. I spun up a local instance of Postgres by defining it as a service in the *compose.yaml*. 

[Metabase](https://www.metabase.com/) was used as the BI tool to analyze the transformed CPD data, for the following reasons:
* Relatively simple [setup](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker)
* Lots of built-in visualization/analytical capabilities without requiring code. Other tools may be needed for heavy customized visuals, but this does the job to get some basic analysis/visuals up and running quickly. 

## File Information
**Pipeline development:**
* *extract.py* - extract CPD data from Socrata API
* *validate.py* - data quality checks for extracted data
* *transform.py* - data transformations to execute on validated data
* *load.py* - import transformed data into Postgres
* *etl_pipeline.py* - pipeline that orchestrates the ETL process
* *testing.ipynb* - used during development to test out individual components

**Architecture/Configuration**
* *compose.yaml* - configuration of services

**Dependencies**
* *requirements.txt* - dependencies required for python development

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

