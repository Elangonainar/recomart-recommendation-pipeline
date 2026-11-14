from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String

user = Entity(name="user", join_keys=["user_id"])
product = Entity(name="product", join_keys=["product_id"])

user_stats_source = FileSource(
    name="user_stats_source",
    path="data/features/user_features.parquet",
    timestamp_field="last_active_ts",
)

user_activity_fv = FeatureView(
    name="user_activity_features",
    entities=[user],
    ttl=timedelta(days=30),
    schema=[
        Field(name="total_interactions", dtype=Int64),
        Field(name="total_purchases", dtype=Int64),
        Field(name="avg_user_rating", dtype=Float32),
    ],
    online=True,
    source=user_stats_source,
)
