import os
import pickle
import logging
import numpy as np
import pandas as pd
import mlflow
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
from evaluate import precision_at_k, recall_at_k, ndcg_at_k

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_svd_model(n_components=10):
    os.makedirs("models/artifacts", exist_ok=True)
    ui_df = pd.read_parquet("data/features/user_item_interactions.parquet")

    # Build user-item utility matrix
    utility_matrix = ui_df.pivot(index='user_id', columns='product_id', values='interaction_score').fillna(0)
    matrix_values = utility_matrix.values

    mlflow.set_experiment("RecoMart_Recommendation_SVD")
    with mlflow.start_run():
        n_comp = min(n_components, min(matrix_values.shape) - 1)
        svd = TruncatedSVD(n_components=max(1, n_comp), random_state=42)
        user_factors = svd.fit_transform(matrix_values)
        item_factors = svd.components_
        reconstructed = np.dot(user_factors, item_factors)

        # Evaluate reconstruction RMSE on non-zero entries
        mask = matrix_values > 0
        rmse = np.sqrt(mean_squared_error(matrix_values[mask], reconstructed[mask]))

        # Evaluate ranking metrics (Precision@5, Recall@5, NDCG@5)
        precisions, recalls, ndcgs = [], [], []
        products = list(utility_matrix.columns)

        for idx, user_id in enumerate(utility_matrix.index):
            actual_ratings = matrix_values[idx]
            relevant = [products[i] for i, r in enumerate(actual_ratings) if r >= 3.0]
            if not relevant:
                continue
            pred_scores = reconstructed[idx]
            ranked_indices = np.argsort(pred_scores)[::-1]
            recommended = [products[i] for i in ranked_indices]

            precisions.append(precision_at_k(recommended, relevant, k=5))
            recalls.append(recall_at_k(recommended, relevant, k=5))
            ndcgs.append(ndcg_at_k(recommended, relevant, k=5))

        avg_p5 = float(np.mean(precisions)) if precisions else 0.0
        avg_r5 = float(np.mean(recalls)) if recalls else 0.0
        avg_ndcg5 = float(np.mean(ndcgs)) if ndcgs else 0.0

        mlflow.log_param("n_components", n_comp)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("precision_at_5", avg_p5)
        mlflow.log_metric("recall_at_5", avg_r5)
        mlflow.log_metric("ndcg_at_5", avg_ndcg5)

        model_path = "models/artifacts/svd_model.pkl"
        with open(model_path, "wb") as f:
            pickle.dump({"model": svd, "users": list(utility_matrix.index), "products": products, "predictions": reconstructed}, f)
        mlflow.log_artifact(model_path)

        logger.info(f"Training Complete | RMSE: {rmse:.4f} | P@5: {avg_p5:.4f} | R@5: {avg_r5:.4f} | NDCG@5: {avg_ndcg5:.4f}")

if __name__ == "__main__":
    train_svd_model()
