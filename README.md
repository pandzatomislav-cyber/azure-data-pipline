# ☁️ Azure Cloud Data Pipeline

A serverless-style data pipeline that ingests retail transaction data, stores it in **Azure Blob Storage**, transforms it, and uploads enriched outputs back to the cloud. Fully automated via **GitHub Actions**.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions (CI)                      │
│                  Triggers on push / schedule                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      pipeline.py                             │
│                                                              │
│  [1] Generate       Retail transaction records (JSON)        │
│         │                                                    │
│         ▼                                                    │
│  [2] Upload Raw  ──────────────────► Azure Blob Storage      │
│                                      Container: raw/         │
│         │                                                    │
│         ▼                                                    │
│  [3] Download + Transform            Enrich, calculate KPIs  │
│         │                                                    │
│         ▼                                                    │
│  [4] Upload Processed ─────────────► Azure Blob Storage      │
│                                      Container: processed/   │
│         │                                                    │
│         ▼                                                    │
│  [5] Upload Report ────────────────► Azure Blob Storage      │
│                                      Container: processed/   │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

- **Azure Blob Storage** — dual-container pattern (raw / processed) mimicking a data lake architecture
- **Automated ingestion** — 1,000 retail transactions generated per run across 5 Dubai malls
- **Data transformation** — revenue, profit margin, store tier classification, temporal enrichment
- **Run reports** — markdown summary uploaded to Azure Blob on every pipeline run
- **GitHub Actions CI** — runs on every push and every Monday at 7am UTC
- **Secrets management** — Azure credentials stored as GitHub repository secrets, never in code

---

## Tech Stack

| Layer | Tool |
|---|---|
| Cloud Storage | Azure Blob Storage |
| Language | Python 3.11 |
| Azure SDK | azure-storage-blob |
| Data processing | Pandas, NumPy |
| CI/CD | GitHub Actions |
| Config | python-dotenv |

---

## Project Structure

```
azure-data-pipeline/
├── pipeline.py                  # Main orchestrator
├── requirements.txt
├── .env.example                 # Credential template (never commit .env)
├── .github/
│   └── workflows/
│       └── pipeline.yml         # GitHub Actions workflow
└── src/
    ├── generate.py              # Retail data generation
    ├── upload.py                # Azure Blob upload/download
    ├── process.py               # Transform + summarise
    └── report.py                # Markdown report generation
```

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/pandzatomislav-cyber/azure-data-pipeline
cd azure-data-pipeline

# Install dependencies
pip install -r requirements.txt

# Set your Azure credentials
cp .env.example .env
# Edit .env and paste your Azure Storage connection string

# Run the pipeline
python pipeline.py
```

---

## GitHub Actions Setup

To run the pipeline automatically in CI, add your connection string as a GitHub secret:

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `AZURE_STORAGE_CONNECTION_STRING`
4. Value: your Azure Storage connection string
5. Click **Add secret**

The pipeline will now run on every push and every Monday automatically.

---

## Pipeline Output (Azure Blob Storage)

Each run creates a timestamped folder in Azure:

```
raw/
  transactions/
    20250519-071000/
      raw_transactions.json

processed/
  transactions/
    20250519-071000/
      processed_transactions.csv
      report.md
```

---

## Author

**Tomislav Pandza**
Dubai, UAE | [pandza.tomislav@gmail.com](mailto:pandza.tomislav@gmail.com) | [GitHub](https://github.com/pandzatomislav-cyber)

*Studying Microsoft Azure (AZ-900) and Google Cloud Associate Cloud Engineer certifications.*
