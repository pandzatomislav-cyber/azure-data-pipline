import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json


def generate_retail_data(n: int = 1000, seed: int = 42) -> list[dict]:
    """Generate retail transaction records as JSON-serialisable dicts."""
    np.random.seed(seed)
    random.seed(seed)

    stores = ["Dubai Mall", "Mall of Emirates", "City Centre Deira", "Dubai Festival City", "Ibn Battuta Mall"]
    categories = {
        "Electronics":  [("iPhone Case", 25), ("Screen Protector", 15), ("Bluetooth Speaker", 80), ("Power Bank", 45)],
        "Fashion":      [("T-Shirt", 30), ("Jeans", 75), ("Sneakers", 120), ("Watch", 200)],
        "Grocery":      [("Organic Milk", 8), ("Bread", 5), ("Coffee Beans", 35), ("Olive Oil", 22)],
        "Sports":       [("Protein Shake", 55), ("Gym Bag", 65), ("Running Shoes", 110), ("Yoga Mat", 40)],
        "Home":         [("Scented Candle", 20), ("Picture Frame", 35), ("Cushion Set", 60), ("Storage Box", 25)],
    }

    start_date = datetime(2024, 1, 1)
    date_range = (datetime(2025, 12, 31) - start_date).days

    records = []
    for i in range(n):
        category = random.choice(list(categories.keys()))
        product, base_price = random.choice(categories[category])
        store = random.choice(stores)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 12, 8, 5])[0]
        price = round(base_price * np.random.normal(1.0, 0.05), 2)
        date = start_date + timedelta(days=random.randint(0, date_range))
        payment = random.choices(["Card", "Cash", "Apple Pay", "Samsung Pay"], weights=[50, 20, 20, 10])[0]

        records.append({
            "transaction_id": f"TXN-{100000 + i}",
            "timestamp":      date.strftime("%Y-%m-%dT%H:%M:%S"),
            "store":          store,
            "category":       category,
            "product":        product,
            "quantity":       quantity,
            "unit_price":     price,
            "total":          round(price * quantity, 2),
            "payment_method": payment,
        })

    return records


def to_json_bytes(records: list[dict]) -> bytes:
    return json.dumps(records, indent=2).encode("utf-8")
