import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    private_key_file=os.getenv("PRIVATE_KEY_PATH"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
print(cur.fetchone())

data_dir = "./data"
files = sorted(f for f in os.listdir(data_dir) if f.endswith(".csv"))

for i ,f in enumerate(files):
    f_path = os.path.join(data_dir, f)
    df = pd.read_csv(f_path, dtype=str)
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df.columns = [ c.upper() for c in df.columns]
    success, _, _, _ = write_pandas(conn, df, table_name="BTS_DATA", auto_create_table=True)
    print(success)

conn.close()



# df = pd.read_csv("/data/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2026_1.csv",
#                  dtype=str)

# df = df.loc[:, ~df.columns.str.startswith("Unnamed")]   # BTS files end with a trailing comma
# df.columns = [ c.upper() for c in df.columns]
# write_pandas(conn, df, table_name="BTS_DATA", auto_create_table=True, overwrite=True)

# conn.close()