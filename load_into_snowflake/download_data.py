import os
import zipfile
import requests

OUT_DIR = "./data"
os.makedirs(OUT_DIR, exist_ok=True)

BASE = ("https://transtats.bts.gov/PREZIP/"
        "On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{y}_{m}.zip")

# 2025 full year + 2026 from January (months not published yet are skipped automatically)
periods = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 13)]

for y, m in periods:
    target = os.path.join(OUT_DIR, f"BTS_{y}_{m:02d}.csv")
    if os.path.exists(target):
        print(f"skip {y}-{m:02d} (already downloaded)")
        continue

    url = BASE.format(y=y, m=m)
    r = requests.get(url, stream=True, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code == 404:
        print(f"not published yet: {y}-{m:02d}")
        continue
    r.raise_for_status()

    zip_path = os.path.join(OUT_DIR, f"{y}_{m:02d}.zip")
    with open(zip_path, "wb") as fh:
        for chunk in r.iter_content(chunk_size=1 << 20):
            fh.write(chunk)

    with zipfile.ZipFile(zip_path) as z:
        csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        with z.open(csv_name) as src, open(target, "wb") as dst:
            dst.write(src.read())
    os.remove(zip_path)
    print(f"downloaded {y}-{m:02d}")