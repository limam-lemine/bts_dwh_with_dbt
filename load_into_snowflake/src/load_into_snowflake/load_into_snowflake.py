import os
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

def load_data(conn, csv_buff):
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
    print(cur.fetchone())
    
    df = pd.read_csv(csv_buff, dtype=str)

    # clean columns
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df.columns = [c.upper() for c in df.columns]

    # load into Snowflake
    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name="BTS_DATA",
        auto_create_table=True
    )

    print(f"{success}, rows loaded: {nrows}")
    cur.close()
