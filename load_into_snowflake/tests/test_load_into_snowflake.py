import io
import pandas as pd
from unittest.mock import MagicMock, patch
from load_into_snowflake.load_into_snowflake import load_data


def test_load_data_cleans_columns_and_writes_to_snowflake():
    conn = MagicMock()
    conn.cursor.return_value.fetchone.return_value = (
        "ROLE",
        "WAREHOUSE",
        "DATABASE",
        "SCHEMA",
    )
    csv_buffer = io.BytesIO(b"id,name,Unnamed: 2\n1,test,ignored\n")

    with patch(
        "load_into_snowflake.load_into_snowflake.write_pandas",
        return_value=(True, 1, 1, None),
    ) as mock_write_pandas:
        load_data(conn, csv_buffer)

    conn.cursor.return_value.execute.assert_called_once_with(
        "SELECT CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
    )
    conn.cursor.return_value.close.assert_called_once()

    mock_write_pandas.assert_called_once()
    write_args, write_kwargs = mock_write_pandas.call_args

    assert write_args[0] is conn
    pd.testing.assert_frame_equal(
        write_args[1],
        pd.DataFrame({"ID": ["1"], "NAME": ["test"]}),
    )
    assert write_kwargs == {
        "table_name": "BTS_DATA",
        "auto_create_table": True,
    }
