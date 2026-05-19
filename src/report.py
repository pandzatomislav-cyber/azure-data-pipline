from datetime import datetime


def generate_report(summary: dict, raw_url: str, processed_url: str) -> bytes:
    """Generate a markdown pipeline run report."""
    lines = [
        "# Azure Data Pipeline — Run Report",
        f"*Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*",
        "",
        "---",
        "",
        "## Pipeline Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Transactions | {summary['total_transactions']:,} |",
        f"| Total Revenue | AED {summary['total_revenue']:,.2f} |",
        f"| Total Gross Profit | AED {summary['total_profit']:,.2f} |",
        f"| Avg. Order Value | AED {summary['avg_order_value']:,.2f} |",
        f"| Top Store | {summary['top_store']} |",
        f"| Top Category | {summary['top_category']} |",
        f"| Top Product | {summary['top_product']} |",
        f"| Top Payment Method | {summary['top_payment']} |",
        "",
        "---",
        "",
        "## Azure Blob Storage",
        "",
        f"| Layer | Blob URL |",
        "|---|---|",
        f"| Raw (JSON) | `{raw_url}` |",
        f"| Processed (CSV) | `{processed_url}` |",
        "",
        "---",
        "",
        "*Pipeline built by Tomislav Pandza | github.com/pandzatomislav-cyber*",
    ]
    return "\n".join(lines).encode("utf-8")
