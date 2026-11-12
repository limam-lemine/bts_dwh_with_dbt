import requests
import zipfile
import io
import shutil

def download_bts_data(year1, year2, month1=1, month2=12):

    BASE = (
        "https://transtats.bts.gov/PREZIP/"
        "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{y}_{m}.zip"
    )

    periods = ((y, m) for y in range(year1, year2 + 1) for m in range(month1, month2 + 1))
    for y, m in periods:
        url = BASE.format(y=y, m=m)
        with requests.get(
            url,
            stream=True,
            timeout=120,
            headers={"User-Agent": "Mozilla/5.0"}
        ) as r:
            if r.status_code == 404:
                print(f"not published yet: {y}-{m:02d}")
                continue
            r.raise_for_status()
            # buffer the downloaded ZIP
            zip_buffer = io.BytesIO()

            for chunk in r.iter_content(chunk_size=1 << 20):
                if chunk:
                    zip_buffer.write(chunk)
        zip_buffer.seek(0)

        # extract CSV into another buffer
        with zipfile.ZipFile(zip_buffer) as z:
            csv_name = next(
                n for n in z.namelist()
                if n.lower().endswith(".csv")
            )
            csv_buffer = io.BytesIO()

            with z.open(csv_name) as src:
                shutil.copyfileobj(src, csv_buffer)

        zip_buffer.close()

        # reset pointer before reading
        csv_buffer.seek(0)
        print(f"downloaded {y}-{m:02d}")
        yield y, m, csv_buffer