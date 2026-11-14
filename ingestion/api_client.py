import os
import json
import random
import logging
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_product_catalog():
    logger.info("Fetching product catalog and external sentiment scores from API...")
    categories = ['Electronics', 'Home & Kitchen', 'Fashion', 'Books', 'Sports']
    products = []

    for i in range(1, 31):
        products.append({
            "product_id": f"prod_{i:03d}",
            "product_name": f"RecoMart Item {i}",
            "category": random.choice(categories),
            "price": round(random.uniform(10.0, 500.0), 2),
            "external_sentiment_score": round(random.uniform(0.1, 1.0), 3),
            "popularity_index": random.randint(1, 100)
        })
    return products

def save_catalog_data():
    now = datetime.utcnow()
    partition_path = f"data/raw/source=catalog_api/type=products/year={now.year}/month={now.month:02d}/day={now.day:02d}"
    os.makedirs(partition_path, exist_ok=True)

    try:
        products = fetch_product_catalog()
        output_file = os.path.join(partition_path, f"catalog_{now.strftime('%H%M%S')}.json")
        with open(output_file, 'w') as f:
            json.dump(products, f, indent=2)
        logger.info(f"Successfully saved {len(products)} product records to {output_file}")
    except Exception as e:
        logger.error(f"Failed to ingest product catalog: {e}")
        raise

if __name__ == "__main__":
    save_catalog_data()
