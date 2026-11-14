# Problem Formulation & Architecture Specification

## 1. Business Problem
RecoMart is an e-commerce platform seeking to increase customer conversion rates, average order value, and cross-selling efficiency through personalized product recommendations.

## 2. Data Sources
1. **Web & Mobile Clickstream Logs:** Captures user interactions (`view`, `add_to_cart`, `purchase`, `rating`) partitioned by date.
2. **Product Metadata & Sentiment API:** Provides product catalog attributes (`category`, `price`) alongside external sentiment and popularity indices.

## 3. Pipeline Outputs
- **Clean EDA Datasets:** Deduplicated, schema-validated interaction and product records (`data/processed/`).
- **Engineered Features:** User activity metrics, item popularity statistics, and utility matrices stored in both Parquet and a relational star schema (`data/features/`).
- **Deployable Recommendation Model:** Serialized Truncated SVD collaborative filtering model tracked with MLflow (`models/artifacts/`).

## 4. Evaluation Metrics
- **RMSE:** Reconstruction accuracy on explicit/implicit ratings.
- **Precision@5 & Recall@5:** Top-K recommendation relevance coverage.
- **NDCG@5:** Rank-aware recommendation quality metric.
