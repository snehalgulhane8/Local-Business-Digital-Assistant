from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"

FILES = {
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "translation": "product_category_name_translation.csv",
}


def load_csv(filename):
    path = DATASET_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    return pd.read_csv(path)


def load_all_data():
    return {
        key: load_csv(filename)
        for key, filename in FILES.items()
    }


def prepare_sales_data(data):
    orders = data["orders"].copy()
    items = data["order_items"].copy()
    products = data["products"].copy()
    translation = data["translation"].copy()

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"],
        errors="coerce"
    )

    merged = items.merge(
        orders[
            [
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp"
            ]
        ],
        on="order_id",
        how="left"
    )

    merged = merged.merge(
        products[
            [
                "product_id",
                "product_category_name"
            ]
        ],
        on="product_id",
        how="left"
    )

    merged = merged.merge(
        translation,
        on="product_category_name",
        how="left"
    )

    merged["category"] = merged[
        "product_category_name_english"
    ].fillna(
        merged["product_category_name"].fillna("Unknown")
    )

    return merged
