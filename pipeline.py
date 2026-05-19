"""
Azure Cloud Data Pipeline
--------------------------
Generate -> Upload Raw (Azure Blob) -> Download -> Transform
-> Upload Processed (Azure Blob) -> Upload Report (Azure Blob)
"""
from datetime import datetime
from dotenv import load_dotenv

from src.generate import generate_retail_data, to_json_bytes
from src.upload import upload_blob, download_blob
from src.process import transform, to_csv_bytes, summarise
from src.report import generate_report

load_dotenv()

RAW_CONTAINER       = "raw"
PROCESSED_CONTAINER = "processed"
RUN_ID              = datetime.utcnow().strftime("%Y%m%d-%H%M%S")


def run() -> None:
    print("=" * 55)
    print("  AZURE CLOUD DATA PIPELINE")
    print(f"  Run ID: {RUN_ID}")
    print("=" * 55)

    # ── 1. Generate ───────────────────────────────────────────────────────────
    print("\n[STEP 1] Generating retail transaction data...")
    records   = generate_retail_data(n=1000)
    raw_bytes = to_json_bytes(records)
    print(f"         {len(records)} records generated ({len(raw_bytes):,} bytes)")

    # ── 2. Upload raw to Azure Blob ───────────────────────────────────────────
    print("\n[STEP 2] Uploading raw data to Azure Blob Storage...")
    raw_blob = f"transactions/{RUN_ID}/raw_transactions.json"
    raw_url  = upload_blob(RAW_CONTAINER, raw_blob, raw_bytes)

    # ── 3. Download + Transform ───────────────────────────────────────────────
    print("\n[STEP 3] Downloading and transforming data...")
    downloaded = download_blob(RAW_CONTAINER, raw_blob)
    df         = transform(downloaded)

    # ── 4. Upload processed CSV ───────────────────────────────────────────────
    print("\n[STEP 4] Uploading processed data to Azure Blob Storage...")
    csv_blob       = f"transactions/{RUN_ID}/processed_transactions.csv"
    processed_url  = upload_blob(PROCESSED_CONTAINER, csv_blob, to_csv_bytes(df))

    # ── 5. Generate + upload report ───────────────────────────────────────────
    print("\n[STEP 5] Generating and uploading run report...")
    summary      = summarise(df)
    report_bytes = generate_report(summary, raw_url, processed_url)
    report_blob  = f"transactions/{RUN_ID}/report.md"
    upload_blob(PROCESSED_CONTAINER, report_blob, report_bytes)

    print("\n" + "=" * 55)
    print("  PIPELINE COMPLETE")
    print(f"  Revenue processed: AED {summary['total_revenue']:,.2f}")
    print(f"  Top store: {summary['top_store']}")
    print("=" * 55)


if __name__ == "__main__":
    run()
