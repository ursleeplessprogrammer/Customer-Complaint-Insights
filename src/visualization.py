from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def save_monthly_chart(monthly, path: Path):
    """Save a chart of complaints received per month."""
    if monthly.empty:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 5))
    plt.plot(
        monthly["month"],
        monthly["complaint_count"],
        marker="o",
        linewidth=2,
    )
    plt.title("Consumer Complaints by Month")
    plt.xlabel("Month")
    plt.ylabel("Number of complaints")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def save_top_products_chart(products, path: Path, top_n=10):
    """Save a horizontal bar chart of the most frequently reported products."""
    if products.empty:
        return

    chart_data = products.head(top_n).sort_values("complaint_count")

    path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.barh(chart_data["product"].astype(str), chart_data["complaint_count"])
    plt.title(f"Top {min(top_n, len(products))} Products by Complaint Count")
    plt.xlabel("Number of complaints")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
