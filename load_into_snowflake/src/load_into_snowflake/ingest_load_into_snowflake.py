import os
import snowflake.connector
from dotenv import load_dotenv
from .download_data import download_bts_data
from .load_into_snowflake import load_data

load_dotenv()

YEAR1 = 2025
YEAR2 = 2026
MONTH1 = 1
MONTH2 = 12

def runner(conn, year1, year2, month1, month2):
    for y, m, csv_buffer in download_bts_data(year1, year2, month1, month2):
        load_data(conn, csv_buffer)
        print(f"loaded BTS_{m}_{y}")


def main():
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

    try:
        runner(conn, 2025, 2026, 1, 12)
    finally:
        conn.close()


if __name__ == "__main__":
    main()