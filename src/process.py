import pandas as pd
import json


def transform(raw_bytes: bytes) -> pd.DataFrame:
    """Transform raw JSON transaction data into an enriched DataFrame."""
    records = json.loads(raw_bytes.decode("utf-8"))
    df = pd.DataFrame(records)

    # ── Type enforcement ──────────────────────────────────────────────────────
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["year"]      = df["timestamp"].dt.year
    df["month"]     = df["timestamp"].dt.month
    df["quarter"]   = df["timestamp"].dt.quarter
    df["day_name"]  = df["timestamp"].dt.day_name()

    # ── Revenue metrics ───────────────────────────────────────────────────────
    df["revenue"]        = (df["unit_price"] * df["quantity"]).round(2)
    df["cost"]           = (df["revenue"] * 0.60).round(2)
    df["gross_profit"]   = (df["revenue"] - df["cost"]).round(2)
    df["margin_pct"]     = ((df["gross_profit"] / df["revenue"]) * 100).round(1)

    # ── Store tier classification ─────────────────────────────────────────────
    premium = ["Dubai Mall", "Mall of Emirates"]
    df["store_tier"] = df["store"].apply(lambda s: "Premium" if s in premium else "Standard")

    print(f"[PROCESS] Transformed {len(df)} records | Revenue: AED {df['revenue'].sum():,.2f}")
    return df


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def summarise(df: pd.DataFrame) -> dict:
    return {
        "total_transactions": len(df),
        "total_revenue":      round(df["revenue"].sum(), 2),
        "total_profit":       round(df["gross_profit"].sum(), 2),
        "avg_order_value":    round(df["revenue"].mean(), 2),
        "top_store":          df.groupby("store")["revenue"].sum().idxmax(),
        "top_category":       df.groupby("category")["revenue"].sum().idxmax(),
        "top_product":        df.groupby("product")["revenue"].sum().idxmax(),
        "top_payment":        df["payment_method"].value_counts().idxmax(),
    }
