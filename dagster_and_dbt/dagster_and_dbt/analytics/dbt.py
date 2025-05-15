# import dagster as dg
# from dagster_dbt import DagsterDbtTranslator, DbtCliResource, dbt_assets

# from dagster_and_dbt.project import dbt_project


# class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
#     def get_asset_key(self, dbt_resource_props):
#         resource_type = dbt_resource_props["resource_type"]
#         name = dbt_resource_props["name"]
#         if resource_type == "source":
#             # print out the resource type and name
#             asset_key = dg.AssetKey(f"taxi_{name}")
#             # Print the asset key for debugging
#             dg.get_dagster_logger().info(f"Generated asset key: {asset_key}")
#             return asset_key
#         else:
#             return super().get_asset_key(dbt_resource_props)

#     def get_group_name(self, dbt_resource_props):
#         return dbt_resource_props["fqn"][1]


# @dbt_assets(
#     manifest=dbt_project.manifest_path,
#     dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
# )
# def dbt_analytics(context: dg.AssetExecutionContext, dbt: DbtCliResource):
#     # Print a message when the asset is materialized
#     context.log.info("Materializing dbt asset in Dagster UI...")
#     yield from dbt.cli(["build"], context=context).stream()
#     context.log.info("Finished materializing dbt asset.")
