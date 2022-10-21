# Databricks notebook source
# MAGIC %run ./_common

# COMMAND ----------

@DBAcademyHelper.monkey_patch
def update_user_grants(self, username: str):
    schema_name = self.to_schema_name(username)
    
    if schema_name not in self.workspace.existing_databases:
        print(f"Skipping update of grants for {username}, database {schema_name} not found.")
    else:
        spark.sql(f"GRANT ALL PRIVILEGES ON DATABASE `{schema_name}` TO `{username}`")
        spark.sql(f"GRANT ALL PRIVILEGES ON ANY FILE TO `{username}`")
        spark.sql(f"ALTER DATABASE {schema_name} OWNER TO `{username}`")
    

# COMMAND ----------

lesson_config.create_schema = False
lesson_config.installing_datasets = False

DA = DBAcademyHelper(course_config, lesson_config)

# We only need the DA object, not any
DA.workspace.do_for_all_users(DA.update_user_grants)

