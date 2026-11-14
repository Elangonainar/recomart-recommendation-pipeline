import os
import glob
import json
import logging
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def prepare_datasets():
    os.makedirs("data/processed", exist_ok=True)

    # Load clickstream
    csv_files = glob.glob("data/raw/source=clickstream/**/*.csv", recursive=True)
    df_clicks = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    df_clicks = df_clicks.drop_duplicates(subset=['event_id']).dropna(subset=['user_id', 'product_id', 'rating'])
    df_clicks['rating'] = df_clicks['rating'].clip(1.0, 5.0)

    # Load product catalog
    json_files = glob.glob("data/raw/source=catalog_api/**/*.json", recursive=True)
    products = []
    for jf in json_files:
        with open(jf, 'r') as f:
            products.extend(json.load(f))
    df_prod = pd.DataFrame(products).drop_duplicates(subset=['product_id'], keep='last')

    # Encode categorical & normalize numerical
    le = LabelEncoder()
    df_prod['category_encoded'] = le.fit_transform(df_prod['category'])

    scaler = MinMaxScaler()
    df_prod['price_normalized'] = scaler.fit_transform(df_prod[['price']])

    df_clicks.to_csv("data/processed/clean_interactions.csv", index=False)
    df_prod.to_csv("data/processed/clean_products.csv", index=False)
    logger.info("Saved cleaned interactions and product datasets to data/processed/")

if __name__ == "__main__":
    prepare_datasets()
