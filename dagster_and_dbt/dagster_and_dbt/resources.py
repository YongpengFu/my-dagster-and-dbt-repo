from dagster_and_dbt.project import dbt_project
from dagster_dbt import DbtCliResource
import os

import boto3
import dagster as dg
from dagster_duckdb import DuckDBResource

database_resource = DuckDBResource(
    database=dg.EnvVar("DUCKDB_DATABASE"),
)

if os.getenv("DAGSTER_ENVIRONMENT") == "prod":
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    smart_open_config = {"client": session.client("s3")}
else:
    smart_open_config = {}


# the import lines go at the top of the file

# this can be defined anywhere below the imports
dbt_resource = DbtCliResource(
    project_dir=dbt_project,
)
