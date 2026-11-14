import numpy as np

def precision_at_k(recommended_items, relevant_items, k=5):
    rec_k = recommended_items[:k]
    if not rec_k:
        return 0.0
    hits = len(set(rec_k) & set(relevant_items))
    return hits / k

def recall_at_k(recommended_items, relevant_items, k=5):
    if not relevant_items:
        return 0.0
    rec_k = recommended_items[:k]
    hits = len(set(rec_k) & set(relevant_items))
    return hits / len(relevant_items)

def ndcg_at_k(recommended_items, relevant_items, k=5):
    rec_k = recommended_items[:k]
    dcg = 0.0
    for idx, item in enumerate(rec_k):
        if item in relevant_items:
            dcg += 1.0 / np.log2(idx + 2)
    idcg = sum(1.0 / np.log2(i + 2) for i in range(min(len(relevant_items), k)))
    return dcg / idcg if idcg > 0 else 0.0
