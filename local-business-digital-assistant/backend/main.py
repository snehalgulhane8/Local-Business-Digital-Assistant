from pathlib import Path
from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from data_loader import load_all_data
from analytics import (
    dashboard_summary,
    monthly_sales,
    category_sales,
    top_products,
    customer_analysis,
    order_status_analysis,
    review_analysis,
    delivery_analysis,
    business_insights,
)
from recommendations import generate_recommendations
from models import BusinessQuestion


app = FastAPI(
    title="Local Business Digital Assistant",
    description="Olist e-commerce business analytics API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_data():
    return load_all_data()


@app.get("/api/health")
def health():
    return {
        "status": "success",
        "message": "API is running"
    }


@app.get("/api/dashboard")
def dashboard():
    return dashboard_summary(get_data())


@app.get("/api/sales/monthly")
def sales_monthly():
    return monthly_sales(get_data())


@app.get("/api/categories")
def categories():
    return category_sales(get_data())


@app.get("/api/products/top")
def products():
    return top_products(get_data())


@app.get("/api/customers/top")
def customers():
    return customer_analysis(get_data())


@app.get("/api/orders/status")
def order_status():
    return order_status_analysis(get_data())


@app.get("/api/reviews")
def reviews():
    return review_analysis(get_data())


@app.get("/api/delivery")
def delivery():
    return delivery_analysis(get_data())


@app.get("/api/insights")
def insights():
    return {
        "insights": business_insights(get_data())
    }


@app.get("/api/recommendations")
def recommendations():
    return generate_recommendations(get_data())


@app.post("/api/ask")
def ask_business(payload: BusinessQuestion):
    data = get_data()
    q = payload.question.lower()
    summary = dashboard_summary(data)

    if any(word in q for word in ["revenue", "sales", "earning"]):
        return {
            "answer": f"Total product revenue is R$ {summary['total_revenue']:,.2f}."
        }

    if "order" in q:
        return {
            "answer": f"There are {summary['total_orders']:,} orders in the dataset."
        }

    if "customer" in q:
        return {
            "answer": f"There are {summary['total_customers']:,} customers in the dataset."
        }

    if "review" in q or "rating" in q:
        r = review_analysis(data)
        return {
            "answer": f"The average review score is {r['average_score']}/5."
        }

    if "delivery" in q:
        d = delivery_analysis(data)
        return {
            "answer": f"Average delivery time is {d['average_delivery_days']} days."
        }

    if any(
        word in q
        for word in ["top category", "best category", "category"]
    ):
        cats = category_sales(data, 1)

        if cats:
            return {
                "answer": f"The highest-revenue category is {cats[0]['category']}."
            }

    if "product" in q or "best seller" in q:
        products = top_products(data, 1)

        if products:
            return {
                "answer": (
                    "The highest-revenue product in the dataset is "
                    f"{products[0]['product_id']}."
                )
            }

    return {
        "answer": (
            "Try asking about revenue, sales, orders, customers, "
            "products, categories, reviews, or delivery."
        )
    }


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/{page_name}.html")
def page(page_name: str):
    allowed = {
        "dashboard",
        "customers",
        "products",
        "orders",
        "recommendations",
    }

    if page_name in allowed:
        return FileResponse(
            FRONTEND_DIR / f"{page_name}.html"
        )

    return FileResponse(FRONTEND_DIR / "index.html")
