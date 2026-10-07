import pandas as pd
from data_loader import prepare_sales_data

def dashboard_summary(data):
    orders = data["orders"]
    items = data["order_items"]
    customers = data["customers"]

    total_orders = int(len(orders))
    total_revenue = float(items["price"].sum())
    total_customers = int(len(customers))
    avg_order = total_revenue / total_orders if total_orders else 0

    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "total_customers": total_customers,
        "average_order_value": round(avg_order, 2),
    }

def monthly_sales(data):
    orders = data["orders"].copy()
    items = data["order_items"].copy()
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )
    df = items.merge(
        orders[["order_id", "order_purchase_timestamp"]],
        on="order_id", how="left"
    )
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    out = df.groupby("month", as_index=False)["price"].sum()
    out.columns = ["month", "sales"]
    return out.to_dict(orient="records")

def category_sales(data, limit=15):
    df = prepare_sales_data(data)
    out = (
        df.groupby("category", as_index=False)["price"]
        .sum()
        .rename(columns={"price": "sales"})
        .sort_values("sales", ascending=False)
        .head(limit)
    )
    return out.to_dict(orient="records")

def top_products(data, limit=10):
    df = prepare_sales_data(data)
    out = (
        df.groupby(["product_id", "category"], as_index=False)
        .agg(revenue=("price", "sum"), quantity=("order_item_id", "count"))
        .sort_values("revenue", ascending=False)
        .head(limit)
    )
    return out.to_dict(orient="records")

def customer_analysis(data, limit=10):
    orders = data["orders"][["order_id", "customer_id"]]
    items = data["order_items"][["order_id", "price"]]
    df = items.merge(orders, on="order_id", how="left")
    out = (
        df.groupby("customer_id", as_index=False)
        .agg(total_spent=("price", "sum"), orders=("order_id", "nunique"))
        .sort_values("total_spent", ascending=False)
        .head(limit)
    )
    return out.to_dict(orient="records")

def order_status_analysis(data):
    out = data["orders"]["order_status"].value_counts().reset_index()
    out.columns = ["status", "count"]
    return out.to_dict(orient="records")

def review_analysis(data):
    reviews = data["reviews"]
    average = float(reviews["review_score"].mean())
    dist = reviews["review_score"].value_counts().sort_index().reset_index()
    dist.columns = ["score", "count"]
    return {
        "average_score": round(average, 2),
        "distribution": dist.to_dict(orient="records"),
    }

def delivery_analysis(data):
    orders = data["orders"].copy()
    for col in ["order_purchase_timestamp", "order_delivered_customer_date"]:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")
    delivered = orders.dropna(
        subset=["order_purchase_timestamp", "order_delivered_customer_date"]
    ).copy()
    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400
    return {
        "average_delivery_days": round(float(delivered["delivery_days"].mean()), 2)
        if not delivered.empty else 0,
        "delivered_orders": int(len(delivered)),
    }

def business_insights(data):
    summary = dashboard_summary(data)
    categories = category_sales(data, 3)
    review = review_analysis(data)
    delivery = delivery_analysis(data)

    insights = []
    if categories:
        insights.append(
            f"{categories[0]['category']} is the highest-revenue category."
        )
    insights.append(
        f"Average order value is R$ {summary['average_order_value']:,.2f}."
    )
    insights.append(
        f"Average customer review score is {review['average_score']}/5."
    )
    if delivery["delivered_orders"]:
        insights.append(
            f"Average delivery time is {delivery['average_delivery_days']} days."
        )
    return insights
