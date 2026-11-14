import os
import glob
import json
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_data():
    os.makedirs("docs", exist_ok=True)
    report_lines = [
        "# RecoMart Automated Data Quality Report",
        f"**Generated At:** {datetime.utcnow().isoformat()} UTC\n",
        "## 1. Clickstream Interactions Validation"
    ]

    csv_files = glob.glob("data/raw/source=clickstream/**/*.csv", recursive=True)
    if not csv_files:
        logger.warning("No clickstream files found.")
        return

    df_clicks = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    total_rows = len(df_clicks)
    null_counts = df_clicks.isnull().sum().to_dict()
    duplicates = df_clicks.duplicated(subset=['event_id']).sum()
    invalid_ratings = df_clicks[(df_clicks['rating'] < 1.0) | (df_clicks['rating'] > 5.0)].shape[0]

    report_lines.extend([
        f"- **Total Records Checked:** {total_rows}",
        f"- **Duplicate Event IDs:** {duplicates}",
        f"- **Null Counts per Column:** {null_counts}",
        f"- **Out-of-Range Ratings (outside 1.0 - 5.0):** {invalid_ratings}",
        f"- **Validation Status:** {'PASSED' if duplicates == 0 and invalid_ratings == 0 else 'WARNING'}\n"
    ])

    report_lines.append("## 2. Product Catalog API Validation")
    json_files = glob.glob("data/raw/source=catalog_api/**/*.json", recursive=True)
    if json_files:
        products = []
        for jf in json_files:
            with open(jf, 'r') as f:
                products.extend(json.load(f))
        df_prod = pd.DataFrame(products).drop_duplicates(subset=['product_id'])
        invalid_prices = df_prod[df_prod['price'] <= 0].shape[0]
        report_lines.extend([
            f"- **Unique Products Validated:** {len(df_prod)}",
            f"- **Invalid Prices (<= 0):** {invalid_prices}",
            f"- **Validation Status:** {'PASSED' if invalid_prices == 0 else 'FAILED'}\n"
        ])

    report_path = "docs/data_quality_report.md"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
    logger.info(f"Data quality report written to {report_path}")

if __name__ == "__main__":
    validate_data()
