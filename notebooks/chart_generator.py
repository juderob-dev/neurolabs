import matplotlib.pyplot as plt
import os

def save_plot(fig, name):
    os.makedirs("outputs/charts", exist_ok=True)
    fig.savefig(f"outputs/charts/{name}.png", dpi=300, bbox_inches="tight")

def chart_top_products(df_products, top_n=10):
    top_products = df_products["name"].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(12,6))
    top_products.plot(kind="bar", ax=ax)
    ax.set_title("Top Products")
    save_plot(fig, "top_products")

def chart_confidence_hist(df_products):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.hist(df_products["score"].dropna(), bins=20)
    ax.set_title("Confidence Distribution")
    save_plot(fig, "confidence_hist")


