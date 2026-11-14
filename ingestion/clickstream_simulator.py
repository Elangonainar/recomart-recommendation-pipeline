import os
import json
import random
import logging
from datetime import datetime
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_clickstream_data(num_records=500):
    now = datetime.utcnow()
    partition_path = f"data/raw/source=clickstream/type=interactions/year={now.year}/month={now.month:02d}/day={now.day:02d}"
    os.makedirs(partition_path, exist_ok=True)

    event_types = ['view', 'add_to_cart', 'purchase', 'rating']
    records = []

    for i in range(num_records):
        event = random.choices(event_types, weights=[0.5, 0.25, 0.15, 0.1])[0]
        rating = round(random.uniform(1.0, 5.0), 1) if event == 'rating' else (5.0 if event == 'purchase' else (3.0 if event == 'add_to_cart' else 1.0))
        records.append({
            "event_id": f"evt_{now.strftime('%Y%m%d%H%M%S')}_{i}",
            "user_id": f"user_{random.randint(1, 50):03d}",
            "product_id": f"prod_{random.randint(1, 30):03d}",
            "event_type": event,
            "rating": rating,
            "timestamp": now.isoformat()
        })

    output_file = os.path.join(partition_path, f"clickstream_{now.strftime('%H%M%S')}.csv")
    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    logger.info(f"Successfully ingested {len(df)} clickstream records to {output_file}")
    return output_file

if __name__ == "__main__":
    generate_clickstream_data()
