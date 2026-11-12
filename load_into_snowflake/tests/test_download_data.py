import io
import zipfile
from unittest.mock import MagicMock, patch

from load_into_snowflake.download_data import download_bts_data


def make_zip():
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("data.csv", "id,name\n1,test\n")

    return buffer.getvalue()


def test_download_bts_data():
    response = MagicMock()
    response.status_code = 200
    response.iter_content.return_value = [make_zip()]
    response.__enter__.return_value = response

    with patch(
        "load_into_snowflake.download_data.requests.get",
        return_value=response,
    ) as mock_get:
        result = list(download_bts_data(2025, 2025, 1, 1))

    assert len(result) == 1

    year, month, csv_buffer = result[0]

    assert year == 2025
    assert month == 1
    assert csv_buffer.read() == b"id,name\n1,test\n"

    mock_get.assert_called_once()