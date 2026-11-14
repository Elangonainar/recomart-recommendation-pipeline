import os
import sqlite3
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def transform_and_load():
    os.makedirs("data/features", exist_ok=True)
    df_clicks = pd.read_csv("data/processed/clean_interactions.csv")
    df_prod = pd.read_csv("data/processed/clean_products.csv")

    # User-level features
    user_features = df_clicks.groupby('user_id').agg(
        total_interactions=('event_id', 'count'),
        total_purchases=('event_type', lambda x: (x == 'purchase').sum()),
        avg_user_rating=('rating', 'mean'),
        last_active_ts=('timestamp', 'max')
    ).reset_index()

    # Item-level features
    item_stats = df_clicks.groupby('product_id').agg(
        avg_item_rating=('rating', 'mean'),
        interaction_count=('event_id', 'count')
    ).reset_index()

    product_features = pd.merge(df_prod, item_stats, on='product_id', how='left').fillna({
        'avg_item_rating': 3.0,
        'interaction_count': 0
    })

    # User-Item Interaction Matrix values
    ui_features = df_clicks.groupby(['user_id', 'product_id']).agg(
        interaction_score=('rating', 'mean'),
        event_timestamp=('timestamp', 'max')
    ).reset_index()

    # Save to parquet for Feast & ML training
    user_features.to_parquet("data/features/user_features.parquet", index=False)
    product_features.to_parquet("data/features/product_features.parquet", index=False)
    ui_features.to_parquet("data/features/user_item_interactions.parquet", index=False)

    # Also store in SQLite Data Warehouse
    conn = sqlite3.connect("data/features/recomart_dw.db")
    with open("transformation/sql/create_feature_tables.sql", "r") as f:
        conn.executescript(f.read())

    user_features.to_sql("dim_users", conn, if_exists="replace", index=False)
    product_features[['product_id', 'product_name', 'category', 'category_encoded', 'price',
                      'price_normalized', 'external_sentiment_score', 'avg_item_rating',
                      'interaction_count']].to_sql("dim_products", conn, if_exists="replace", index=False)
    ui_features.to_sql("fact_user_item_features", conn, if_exists="replace", index=False)
    conn.close()

    logger.info("Feature engineering complete. Saved to Parquet and SQLite Data Warehouse.")

if __name__ == "__main__":
    transform_and_load()
