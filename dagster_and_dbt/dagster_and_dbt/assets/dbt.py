import dagster as dg
from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets

from dagster_and_dbt.project import dbt_project
from dagster_and_dbt.partitions import daily_partition
import json
INCREMENTAL_SELECTOR = "config.materialized:incremental"


class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            # print out the resource type and name
            asset_key = dg.AssetKey(f"taxi_{name}")
            # Print the asset key for debugging
            dg.get_dagster_logger().info(f"Generated asset key: {asset_key}")
            return asset_key
        else:
            return super().get_asset_key(dbt_resource_props)

    def get_group_name(self, dbt_resource_props):
        return dbt_resource_props["fqn"][1]


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    exclude=INCREMENTAL_SELECTOR,  # Add this here
)
def dbt_analytics(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    # Print a message when the asset is materialized
    context.log.info("Materializing dbt asset in Dagster UI...")
    yield from dbt.cli(["build"], context=context).stream()
    context.log.info("Finished materializing dbt asset.")


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    select=INCREMENTAL_SELECTOR,     # select only models with INCREMENTAL_SELECTOR
    partitions_def=daily_partition   # partition those models using daily_partition
)
def incremental_dbt_models(
    context: dg.AssetExecutionContext,
    dbt: DbtCliResource
):
    time_window = context.partition_time_window
    dbt_vars = {
        "min_date": time_window.start.strftime('%Y-%m-%d'),
        "max_date": time_window.end.strftime('%Y-%m-%d')
    }

    yield from dbt.cli(["build", "--vars", json.dumps(dbt_vars)], context=context).stream()
