from analytics import (
    dashboard_summary, category_sales, review_analysis, delivery_analysis
)

def generate_recommendations(data):
    summary = dashboard_summary(data)
    categories = category_sales(data, 5)
    review = review_analysis(data)
    delivery = delivery_analysis(data)

    recs = []

    if categories:
        recs.append({
            "type": "success",
            "title": "Top category",
            "message": f"{categories[0]['category']} generates the most revenue."
        })

    if review["average_score"] < 4:
        recs.append({
            "type": "warning",
            "title": "Customer satisfaction",
            "message": "Review scores are below 4/5. Investigate low-rated orders and products."
        })
    else:
        recs.append({
            "type": "success",
            "title": "Customer satisfaction",
            "message": f"Average review score is {review['average_score']}/5."
        })

    if delivery["average_delivery_days"] > 15:
        recs.append({
            "type": "warning",
            "title": "Delivery",
            "message": f"Average delivery time is {delivery['average_delivery_days']} days. Review logistics performance."
        })
    elif delivery["average_delivery_days"]:
        recs.append({
            "type": "info",
            "title": "Delivery",
            "message": f"Average delivery time is {delivery['average_delivery_days']} days."
        })

    recs.append({
        "type": "info",
        "title": "Business scale",
        "message": f"{summary['total_orders']:,} orders and {summary['total_customers']:,} customers are available for analysis."
    })
    return recs
